"""One test per requirement of task.md. Kept outside the repository the agent works in."""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser

STAMP = "2026-10-05T12:00:00+00:00"
VOID = {"meta", "link", "br", "hr", "img", "input"}


def svc(name, state, **extra):
    return {"name": name, "state": state, **extra}


MIXED = [
    svc("Web app", "operational", url="https://app.example.com", uptime=99.982),
    svc("Payments API", "outage", note="Card payments are failing.", uptime=97.5),
    svc("Email", "degraded", note="Delivery is delayed."),
    svc("Reports", "maintenance", url="/reports"),
]


class Node:
    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.parent, self.children, self.own = tag, dict(attrs), parent, [], []

    def walk(self):
        for child in self.children:
            yield child
            yield from child.walk()

    def find(self, tag=None, cls=None):
        return [n for n in self.walk() if (tag is None or n.tag == tag) and (cls is None or cls in (n.attrs.get("class") or "").split())]

    @property
    def text(self):
        return " ".join("".join(self.own_text()).split())

    def own_text(self):
        for item in self.own:
            if isinstance(item, Node):
                yield from item.own_text()
            else:
                yield item


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

    def handle_startendtag(self, tag, attrs):
        node = Node(tag, attrs, self.at)
        self.at.children.append(node)
        self.at.own.append(node)

    def handle_endtag(self, tag):
        node = self.at
        while node is not self.root and node.tag != tag:
            node = node.parent
        if node is not self.root:
            self.at = node.parent

    def handle_data(self, data):
        self.at.own.append(data)


def page(services, stamp=STAMP):
    from app.page import render
    html = render(services, stamp)
    return html, Tree(html).root


def css(services=MIXED):
    return "\n".join("".join(t for t in n.own if isinstance(t, str)) for n in page(services)[1].find("style"))


def rules(text):
    """Innermost `selector { body }` pairs, whatever at-rule they sit in."""
    return [(s.strip(), b) for s, b in re.findall(r"([^{}]+)\{([^{}]*)\}", text)]


def block(text, pattern):
    """Body of the first at-rule whose prelude matches pattern."""
    found = re.search(r"@media[^{]*" + pattern + r"[^{]*\{", text)
    if not found:
        return None
    depth, start = 1, found.end()
    for index in range(start, len(text)):
        depth += {"{": 1, "}": -1}.get(text[index], 0)
        if depth == 0:
            return text[start:index]
    return None


def item(root, name):
    return next(li for li in root.find("li", "service") if li.find("h2") and li.find("h2")[0].text == name)


class Requirements(unittest.TestCase):
    def test_r01_doctype_and_lang(self):
        html, root = page(MIXED)
        self.assertTrue(html.lstrip().lower().startswith("<!doctype html>"), html[:40])
        self.assertEqual(root.find("html")[0].attrs.get("lang"), "en")

    def test_r02_meta_charset(self):
        head = page(MIXED)[1].find("head")[0]
        self.assertTrue(any((m.attrs.get("charset") or "").lower() == "utf-8" for m in head.find("meta")))

    def test_r03_viewport_meta(self):
        head = page(MIXED)[1].find("head")[0]
        content = next(m.attrs.get("content", "") for m in head.find("meta") if m.attrs.get("name") == "viewport")
        self.assertEqual(content.replace(" ", ""), "width=device-width,initial-scale=1")

    def test_r04_title_counts_operational(self):
        self.assertEqual(page(MIXED)[1].find("title")[0].text, "Status · 1 of 4 operational")
        three = [svc("A", "operational"), svc("B", "operational"), svc("C", "operational"), svc("D", "degraded")]
        self.assertEqual(page(three)[1].find("title")[0].text, "Status · 3 of 4 operational")

    def test_r05_one_style_element_nothing_external_or_inline(self):
        root = page(MIXED)[1]
        self.assertEqual(len(root.find("style")), 1)
        self.assertEqual(root.find("link"), [])
        self.assertFalse(any("style" in n.attrs for n in root.walk()))
        self.assertNotIn("@import", css())

    def test_r06_no_scripts(self):
        self.assertEqual(page(MIXED)[1].find("script"), [])

    def test_r07_data_is_escaped(self):
        html, root = page([svc("R&D <beta>", "degraded", note='Use "x" & <y>')])
        self.assertIn("R&amp;D &lt;beta&gt;", html)
        self.assertNotIn("<beta>", html)
        self.assertNotIn("<y>", html)
        self.assertEqual(root.find("h2")[0].text, "R&D <beta>")

    def test_r08_header_h1(self):
        header = page(MIXED)[1].find("header")[0]
        self.assertEqual(header.find("h1")[0].text, "System status")

    def test_r09_banner_all_operational_with_role(self):
        banner = page([svc("A", "operational"), svc("B", "operational")])[1].find(cls="banner")[0]
        self.assertEqual(banner.text, "All systems operational")
        self.assertEqual(banner.attrs.get("role"), "status")

    def test_r10_banner_plural(self):
        four = [svc("A", "outage"), svc("B", "degraded"), svc("C", "operational"), svc("D", "operational")]
        self.assertEqual(page(four)[1].find(cls="banner")[0].text, "2 of 4 services need attention")

    def test_r11_banner_singular(self):
        four = [svc("A", "degraded"), svc("B", "operational"), svc("C", "operational"), svc("D", "operational")]
        self.assertEqual(page(four)[1].find(cls="banner")[0].text, "1 of 4 services needs attention")

    def test_r12_maintenance_not_attention_but_appended(self):
        calm = [svc("A", "operational"), svc("B", "maintenance"), svc("C", "maintenance")]
        self.assertEqual(page(calm)[1].find(cls="banner")[0].text, "All systems operational · 2 under maintenance")
        self.assertEqual(page(MIXED)[1].find(cls="banner")[0].text, "2 of 4 services need attention · 1 under maintenance")

    def test_r13_banner_modifier_class(self):
        def modifiers(services):
            return [c for c in page(services)[1].find(cls="banner")[0].attrs["class"].split() if c.startswith("banner--")]
        self.assertEqual(modifiers(MIXED), ["banner--down"])
        self.assertEqual(modifiers([svc("A", "degraded"), svc("B", "maintenance")]), ["banner--warn"])
        self.assertEqual(modifiers([svc("A", "operational"), svc("B", "maintenance")]), ["banner--ok"])

    def test_r14_list_inside_main(self):
        main = page(MIXED)[1].find("main")[0]
        lists = main.find("ul", "services")
        self.assertEqual(len(lists), 1)
        self.assertEqual([c.tag for c in lists[0].children], ["li"] * 4)
        self.assertEqual(len(lists[0].find("li", "service")), 4)

    def test_r15_order_by_severity_then_name_ignoring_case(self):
        services = [svc("zeta", "operational"), svc("Beta", "operational"), svc("alpha", "operational"), svc("Maint", "maintenance"),
                    svc("Slow b", "degraded"), svc("slow A", "degraded"), svc("Down", "outage")]
        names = [li.find("h2")[0].text for li in page(services)[1].find("li", "service")]
        self.assertEqual(names, ["Down", "slow A", "Slow b", "Maint", "alpha", "Beta", "zeta"])

    def test_r16_data_state(self):
        root = page(MIXED)[1]
        self.assertEqual({li.find("h2")[0].text: li.attrs.get("data-state") for li in root.find("li", "service")},
                         {"Web app": "operational", "Payments API": "outage", "Email": "degraded", "Reports": "maintenance"})

    def test_r17_decorative_dot(self):
        for li in page(MIXED)[1].find("li", "service"):
            dots = li.find("span", "dot")
            self.assertEqual(len(dots), 1)
            self.assertEqual(dots[0].attrs.get("aria-hidden"), "true")
            self.assertEqual(dots[0].text, "")

    def test_r18_name_in_h2(self):
        names = sorted(h.text for h in page(MIXED)[1].find("h2"))
        self.assertEqual(names, ["Email", "Payments API", "Reports", "Web app"])

    def test_r19_links_and_noopener_only_for_other_sites(self):
        root = page(MIXED)[1]
        external = item(root, "Web app").find("h2")[0].find("a")[0]
        self.assertEqual(external.attrs.get("href"), "https://app.example.com")
        self.assertIn("noopener", (external.attrs.get("rel") or "").split())
        relative = item(root, "Reports").find("h2")[0].find("a")[0]
        self.assertEqual(relative.attrs.get("href"), "/reports")
        self.assertNotIn("noopener", (relative.attrs.get("rel") or "").split())
        self.assertEqual(item(root, "Email").find("a"), [])

    def test_r20_state_in_words(self):
        root = page(MIXED)[1]
        self.assertEqual({li.find("h2")[0].text: li.find("span", "state")[0].text for li in root.find("li", "service")},
                         {"Web app": "Operational", "Payments API": "Major outage", "Email": "Degraded performance", "Reports": "Under maintenance"})

    def test_r21_note_only_when_present(self):
        root = page(MIXED)[1]
        self.assertEqual(item(root, "Email").find("p", "note")[0].text, "Delivery is delayed.")
        self.assertEqual(item(root, "Web app").find(cls="note"), [])
        self.assertEqual(item(root, "Reports").find(cls="note"), [])

    def test_r22_uptime_two_decimals_only_when_present(self):
        root = page(MIXED)[1]
        self.assertEqual(item(root, "Web app").find("span", "uptime")[0].text, "99.98% uptime")
        self.assertEqual(item(root, "Payments API").find("span", "uptime")[0].text, "97.50% uptime")
        self.assertEqual(item(root, "Email").find(cls="uptime"), [])

    def test_r23_item_id_slug(self):
        root = page(MIXED + [svc("R&D <beta>", "operational"), svc("Web app (EU)", "operational")])[1]
        self.assertEqual(item(root, "Payments API").attrs.get("id"), "service-payments-api")
        self.assertEqual(item(root, "R&D <beta>").attrs.get("id"), "service-r-d-beta")
        self.assertEqual(item(root, "Web app (EU)").attrs.get("id"), "service-web-app-eu")

    def test_r24_no_services(self):
        root = page([])[1]
        self.assertEqual(root.find(cls="banner"), [])
        self.assertEqual(root.find(cls="services"), [])
        self.assertEqual(root.find("p", "empty")[0].text, "No services configured.")
        self.assertEqual(root.find("title")[0].text, "Status · no services")

    def test_r25_footer_time(self):
        time = page(MIXED)[1].find("footer")[0].find("time")[0]
        self.assertEqual(time.attrs.get("datetime"), STAMP)
        self.assertEqual(time.text, f"Updated {STAMP}")

    def test_r26_unknown_state_raises(self):
        from app.page import render
        with self.assertRaises(ValueError) as caught:
            render([svc("A", "operational"), svc("B", "broken")], STAMP)
        self.assertEqual(str(caught.exception), "unknown state: broken")

    def test_r27_runs_as_a_module_with_utc_now(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "services.json")
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(MIXED, handle)
            done = subprocess.run([sys.executable, "-m", "app.page", path], capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=30)
        self.assertEqual(done.returncode, 0, done.stderr)
        root = Tree(done.stdout).root
        self.assertEqual(len(root.find("li", "service")), 4)
        stamp = datetime.fromisoformat(root.find("time")[0].attrs["datetime"].replace("Z", "+00:00"))
        if stamp.tzinfo is None:
            stamp = stamp.replace(tzinfo=timezone.utc)
        self.assertLess(abs(datetime.now(timezone.utc) - stamp), timedelta(minutes=5))

    def test_r28_color_custom_properties_on_root(self):
        bodies = [body for selector, body in rules(css()) if selector.split("{")[-1].strip() == ":root"]
        wanted = ("--bg", "--text", "--ok", "--warn", "--down", "--maint")
        self.assertTrue(any(all(re.search(re.escape(name) + r"\s*:", body) for name in wanted) for body in bodies), bodies)

    def test_r29_dark_mode_redefines_bg_and_text(self):
        dark = block(css(), r"prefers-color-scheme\s*:\s*dark")
        self.assertIsNotNone(dark)
        self.assertRegex(dark, r"--bg\s*:")
        self.assertRegex(dark, r"--text\s*:")

    def test_r30_dot_color_rule_per_state(self):
        found = rules(css())
        for state in ("operational", "degraded", "outage", "maintenance"):
            pattern = r"\[data-state=[\"']?" + state + r"[\"']?\]\s*\.dot"
            self.assertTrue(any(re.search(pattern, selector) and re.search(r"background|color", body) for selector, body in found), state)

    def test_r31_pulse_animation_on_outage_dot_only(self):
        text = css()
        self.assertRegex(text, r"@keyframes\s+pulse\b")
        animated = [selector for selector, body in rules(text) if re.search(r"animation[^;]*\bpulse\b", body)]
        self.assertTrue(animated)
        for selector in animated:
            for part in selector.split(","):
                self.assertRegex(part, r"outage[\"']?\]\s*\.dot")

    def test_r32_reduced_motion_turns_animation_off(self):
        calm = block(css(), r"prefers-reduced-motion\s*:\s*reduce")
        self.assertIsNotNone(calm)
        self.assertRegex(calm, r"animation\s*:\s*none")

    def test_r33_centered_column_640(self):
        centered = [body for selector, body in rules(css()) if re.search(r"max-width\s*:\s*640px", body)]
        self.assertTrue(centered)
        self.assertTrue(any(re.search(r"margin[^;]*\bauto\b", body) for body in centered), centered)

    def test_r34_phone_layout_stacks(self):
        phone = block(css(), r"max-width\s*:\s*480px")
        self.assertIsNotNone(phone)
        self.assertRegex(phone, r"flex-direction\s*:\s*column")

    def test_r35_focus_visible_outline(self):
        bodies = [body for selector, body in rules(css()) if re.search(r"\ba:focus-visible", selector)]
        self.assertTrue(bodies)
        self.assertTrue(any(re.search(r"outline\s*:\s*(?!none|0\b)", body) for body in bodies), bodies)

    def test_r36_system_font(self):
        self.assertRegex(css(), r"font-family\s*:\s*system-ui\s*,\s*sans-serif")


if __name__ == "__main__":
    unittest.main()
