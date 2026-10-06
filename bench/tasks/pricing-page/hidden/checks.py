"""What a short, ambitious brief asks for, one test per expectation. Kept outside the agent's repository.

Static checks on the delivered file: they see structure and CSS, not rendered pixels.
"""
import os
import re
import unittest
from html.parser import HTMLParser

PATH = os.path.join(os.getcwd(), "site", "pricing.html")
VOID = {"meta", "link", "br", "hr", "img", "input", "source"}


class Node:
    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.parent, self.children, self.own = tag, dict(attrs), parent, [], []

    def walk(self):
        for child in self.children:
            yield child
            yield from child.walk()

    def find(self, *tags):
        return [n for n in self.walk() if n.tag in tags]

    @property
    def text(self):
        parts = []
        for item in self.own:
            parts.append(item.text if isinstance(item, Node) else item)
        return " ".join(" ".join(parts).split())


class Tree(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.root = self.at = Node("#root", [], None)
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.at)
        self.at.children.append(node)
        self.at.own.append(node)
        if tag not in VOID:
            self.at = node

    handle_startendtag = lambda self, tag, attrs: (self.handle_starttag(tag, attrs), tag in VOID or self.handle_endtag(tag))

    def handle_endtag(self, tag):
        node = self.at
        while node is not self.root and node.tag != tag:
            node = node.parent
        if node is not self.root:
            self.at = node.parent

    def handle_data(self, data):
        self.at.own.append(data)


class Brief(unittest.TestCase):
    def setUp(cls):
        with open(PATH, encoding="utf-8") as handle:
            cls.html = handle.read()
        cls.root = Tree(cls.html).root
        cls.css = "\n".join("".join(t for t in n.own if isinstance(t, str)) for n in cls.root.find("style"))
        cls.js = "\n".join("".join(t for t in n.own if isinstance(t, str)) for n in cls.root.find("script"))
        body = cls.root.find("body")
        cls.visible = body[0].text if body else ""

    def test_b01_document_basics(self):
        self.assertTrue(self.html.lstrip().lower().startswith("<!doctype html>"))
        self.assertTrue(self.root.find("html")[0].attrs.get("lang"))
        self.assertTrue(self.root.find("title")[0].text)

    def test_b02_viewport_meta(self):
        self.assertTrue(any(m.attrs.get("name") == "viewport" and "width=device-width" in m.attrs.get("content", "") for m in self.root.find("meta")))

    def test_b03_nothing_loaded_from_the_network(self):
        self.assertFalse(any(n.attrs.get("src") for n in self.root.find("script", "img", "iframe", "video", "source")
                             if not n.attrs.get("src", "").startswith("data:")))
        self.assertFalse(any((n.attrs.get("rel") or "").lower() in ("stylesheet", "preconnect", "preload") for n in self.root.find("link")))
        self.assertNotRegex(self.css, r"@import|url\(\s*[\"']?(https?:)?//")
        self.assertNotRegex(self.js, r"\bfetch\(|XMLHttpRequest|import\s*\(")

    def test_b04_three_plans_as_headings(self):
        headings = [h.text.lower() for h in self.root.find("h2", "h3", "h4")]
        for plan in ("free", "team", "business"):
            self.assertTrue(any(re.search(rf"\b{plan}\b", h) for h in headings), plan)

    def test_b05_monthly_prices(self):
        for price in (r"\$\s*0\b", r"\$\s*8\b", r"\$\s*15\b"):
            self.assertRegex(self.html, price)

    def test_b06_yearly_prices_are_20_percent_cheaper(self):
        both = self.html
        self.assertTrue(re.search(r"\b6\.40?\b", both) or re.search(r"0\.8\b|\b0?\.2\b|\b20\b\s*/\s*100|\b80\b\s*/\s*100", self.js), "no yearly Team price or 20% computation")
        self.assertTrue(re.search(r"\b12(\.00)?\b", both) or re.search(r"0\.8\b|\b0?\.2\b|\b20\b\s*/\s*100|\b80\b\s*/\s*100", self.js))

    def test_b07_billing_switch_is_a_real_control(self):
        controls = self.root.find("button", "input", "select")
        words = " ".join(" ".join([c.text, c.attrs.get("aria-label", ""), c.attrs.get("value", ""), c.attrs.get("id", ""), c.attrs.get("name", "")]) for c in controls).lower()
        labels = " ".join(l.text for l in self.root.find("label")).lower()
        self.assertRegex(words + " " + labels, r"year|annual")
        self.assertRegex(self.js, r"addEventListener|onchange|onclick|oninput")

    def test_b08_switch_state_reaches_assistive_tech(self):
        controls = self.root.find("button", "input")
        self.assertTrue(any("aria-pressed" in c.attrs or "aria-checked" in c.attrs or c.attrs.get("type") in ("checkbox", "radio") or c.attrs.get("role") in ("switch", "tab", "radio") for c in controls))

    def test_b09_price_change_is_announced(self):
        self.assertTrue(any("aria-live" in n.attrs or n.attrs.get("role") in ("status", "alert") for n in self.root.walk()) or self.root.find("output"))

    def test_b10_team_plan_stands_out(self):
        marked = [n for n in self.root.walk() if re.search(r"featured|popular|recommend|highlight|best|primary|accent|emphas", " ".join([n.attrs.get("class", ""), n.attrs.get("data-featured", "x" if "data-featured" in n.attrs else ""), n.attrs.get("aria-label", "")]).lower())]
        self.assertTrue(any(re.search(r"\bteam\b", n.text.lower()) for n in marked) or re.search(r"most popular|recommended|best value", self.visible.lower()))

    def test_b11_each_plan_has_a_feature_list(self):
        lists = [l for l in self.root.find("ul", "ol") if len([c for c in l.children if c.tag == "li"]) >= 3 and not l.find("h2", "h3", "h4")]
        self.assertGreaterEqual(len(lists), 3)

    def test_b12_call_to_action_per_plan(self):
        actions = [n for n in self.root.find("a", "button") if re.search(r"start|get|try|contact|choose|sign|talk|buy|upgrade|join", n.text.lower())]
        self.assertGreaterEqual(len(actions), 3)

    def test_b13_comparison_table(self):
        tables = self.root.find("table")
        self.assertTrue(tables)
        table = max(tables, key=lambda t: len(t.find("tr")))
        self.assertGreaterEqual(len(table.find("tr")), 5)
        head = " ".join(th.text.lower() for th in table.find("th"))
        for plan in ("free", "team", "business"):
            self.assertIn(plan, head)

    def test_b14_table_is_readable_by_screen_readers(self):
        table = max(self.root.find("table"), key=lambda t: len(t.find("tr")))
        self.assertTrue(any(th.attrs.get("scope") for th in table.find("th")))
        self.assertTrue(table.find("caption") or table.attrs.get("aria-label") or table.attrs.get("aria-labelledby"))

    def test_b15_faq_with_four_questions_that_open_and_close(self):
        native = self.root.find("details")
        custom = [b for b in self.root.find("button") if "aria-expanded" in b.attrs]
        self.assertGreaterEqual(max(len(native), len(custom)), 4)

    def test_b16_phone_layout(self):
        self.assertRegex(self.css, r"@media[^{]*\((max|min)-width|@container|auto-fit|auto-fill")

    def test_b17_table_does_not_break_small_screens(self):
        self.assertRegex(self.css, r"overflow(-x)?\s*:\s*(auto|scroll)")

    def test_b18_dark_mode(self):
        self.assertRegex(self.css, r"prefers-color-scheme\s*:\s*dark|color-scheme\s*:\s*light dark|light-dark\(")

    def test_b19_colors_as_custom_properties(self):
        self.assertGreaterEqual(len(set(re.findall(r"(--[\w-]+)\s*:", self.css))), 4)

    def test_b20_motion(self):
        self.assertRegex(self.css, r"transition\s*:|transition-property|animation\s*:|@keyframes")

    def test_b21_reduced_motion_respected(self):
        self.assertRegex(self.css + self.js, r"prefers-reduced-motion")

    def test_b22_hover_states(self):
        self.assertRegex(self.css, r":hover")

    def test_b23_visible_keyboard_focus(self):
        self.assertRegex(self.css, r":focus-visible|:focus\b")
        self.assertNotRegex(self.css, r"outline\s*:\s*(none|0)\s*;?\s*\}(?![\s\S]*:focus-visible)")

    def test_b24_landmarks_and_one_h1(self):
        self.assertEqual(len(self.root.find("h1")), 1)
        self.assertTrue(self.root.find("main"))
        self.assertTrue(self.root.find("header") or self.root.find("footer"))

    def test_b25_controls_are_real_buttons_and_links(self):
        self.assertFalse(any("onclick" in n.attrs for n in self.root.find("div", "span", "li", "p")))
        self.assertFalse(any(not a.attrs.get("href") for a in self.root.find("a")))

    def test_b26_premium_finish(self):
        self.assertRegex(self.css, r"box-shadow|gradient\(")
        self.assertRegex(self.css, r"border-radius")
        self.assertRegex(self.css, r"letter-spacing|font-weight|clamp\(")


if __name__ == "__main__":
    unittest.main()
