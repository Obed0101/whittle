"""Breadth of a "complete product" delivered from an open brief. Kept outside the agent's repository.

Held-out fixture: this rubric was written before any agent output for this brief was seen, and after
the skill under test was frozen. Detection is static (patterns in the delivered HTML, CSS and
JavaScript): it measures whether something was built, not whether it works well.
"""
import os
import re
import unittest

APP = os.path.join(os.getcwd(), "notes")


def read(*extensions):
    parts = []
    for folder, _, names in os.walk(APP):
        for name in sorted(names):
            if name.endswith(extensions):
                with open(os.path.join(folder, name), encoding="utf-8", errors="replace") as handle:
                    parts.append(handle.read())
    return "\n".join(parts)


class Breadth(unittest.TestCase):
    def setUp(self):
        self.assertTrue(os.path.exists(os.path.join(APP, "index.html")), "notes/index.html missing")
        self.all = read(".html", ".css", ".js")
        self.low = self.all.lower()

    def has(self, pattern):
        self.assertRegex(self.low, pattern)

    def test_n01_opens_without_network_or_build(self):
        self.assertNotRegex(self.all, r"(src|href)=[\"']https?://|@import\s+url\(\s*[\"']?https?:|from\s+[\"']https?://|\brequire\(")

    def test_n02_create_note(self):
        self.has(r"new note|add note|create note|newnote|addnote|createnote")

    def test_n03_title_and_body(self):
        self.has(r"title")
        self.has(r"<textarea|contenteditable")

    def test_n04_delete_note(self):
        self.has(r"delete|remove")

    def test_n05_saved_between_visits(self):
        self.has(r"localstorage|indexeddb")

    def test_n06_saves_as_you_type(self):
        self.has(r"addeventlistener\(\s*[\"']input[\"']|oninput")
        self.has(r"debounce|settimeout|autosave|saved")

    def test_n07_search(self):
        self.has(r"search")

    def test_n08_tags_or_folders(self):
        self.has(r"\btags?\b|label|folder|notebook|categor")

    def test_n09_filter_by_tag_or_folder(self):
        self.has(r"filter")

    def test_n10_pin_or_favorite(self):
        self.has(r"\bpin|favorite|favourite|\bstar")

    def test_n11_sort(self):
        self.has(r"\bsort")

    def test_n12_dates_shown(self):
        self.has(r"updated|modified|created|edited")
        self.has(r"tolocale|intl\.datetimeformat|relativetimeformat|todatestring|ago\b")

    def test_n13_formatting_or_markdown(self):
        self.has(r"markdown|preview|\bbold\b|<strong|execcommand|checklist")

    def test_n14_trash_or_archive(self):
        self.has(r"trash|archive|restore")

    def test_n15_undo_or_confirmation(self):
        self.has(r"\bundo\b|confirm\(|are you sure|<dialog")

    def test_n16_export(self):
        self.has(r"export|download|backup")

    def test_n17_import(self):
        self.has(r"import|type=[\"']file|filereader")

    def test_n18_keyboard_shortcuts(self):
        self.has(r"keydown")
        self.has(r"ctrlkey|metakey|shortcut|<kbd")

    def test_n19_escape_closes_things(self):
        self.has(r"escape|<dialog")

    def test_n20_dark_mode(self):
        self.has(r"prefers-color-scheme|data-theme|dark-mode|theme-toggle|\.dark\b|color-scheme")

    def test_n21_works_on_phones(self):
        self.has(r"name=[\"']viewport")
        self.has(r"@media[^{]*\((max|min)-width|@container")

    def test_n22_labelled_controls(self):
        self.has(r"aria-label|<label")

    def test_n23_status_announced(self):
        self.has(r"aria-live|role=[\"'](status|alert)")

    def test_n24_visible_focus(self):
        self.has(r":focus-visible|:focus\b")

    def test_n25_motion_with_reduced_motion_respected(self):
        self.has(r"transition|animation")
        self.has(r"prefers-reduced-motion")

    def test_n26_empty_state(self):
        self.has(r"no notes|nothing here|empty|first note|get started")

    def test_n27_no_results_state(self):
        self.has(r"no (results|matches|notes match|notes found|matching)|nothing (found|matches)|no notes match")

    def test_n28_word_or_character_count(self):
        self.has(r"word|character|chars\b")
        self.has(r"count|\.length")

    def test_n29_user_text_is_not_injected_as_html(self):
        self.has(r"textcontent|createtextnode|innertext|escapehtml|escape\(|sanitize")

    def test_n30_survives_bad_saved_data(self):
        self.has(r"try\s*\{[\s\S]{0,400}json\.parse|json\.parse[\s\S]{0,400}catch")

    def test_n31_tabs_stay_in_sync(self):
        self.has(r"addeventlistener\(\s*[\"']storage[\"']|onstorage|broadcastchannel")

    def test_n32_saved_data_has_a_version(self):
        self.has(r"version|schema|migrat")

    def test_n33_more_than_a_single_file(self):
        files = [n for _, _, names in os.walk(APP) for n in names if n.endswith((".html", ".css", ".js"))]
        self.assertGreaterEqual(len(files), 2)

    def test_n34_list_and_editor_layout(self):
        self.has(r"<aside|sidebar|note-list|notelist|notes-list")

    def test_n35_duplicate_note(self):
        self.has(r"duplicate|make a copy|copy note|clone")

    def test_n36_storage_failure_handled(self):
        self.has(r"quota|try\s*\{[\s\S]{0,300}setitem[\s\S]{0,300}catch|storage (is )?full|could not save|couldn't save|failed to save")
