"""Breadth of a "complete product" delivered from an open brief. Kept outside the agent's repository.

The brief lists no features, so this is a rubric, not a specification: each test looks for one thing a
daily-use kanban board has. Detection is static (patterns in the delivered HTML, CSS and JavaScript),
so it measures whether something was built, not whether it works well. Read the score as breadth.
"""
import os
import re
import unittest

BOARD = os.path.join(os.getcwd(), "board")


def read(*extensions):
    parts = []
    for folder, _, names in os.walk(BOARD):
        for name in sorted(names):
            if name.endswith(extensions):
                with open(os.path.join(folder, name), encoding="utf-8", errors="replace") as handle:
                    parts.append(handle.read())
    return "\n".join(parts)


class Breadth(unittest.TestCase):
    def setUp(self):
        self.assertTrue(os.path.exists(os.path.join(BOARD, "index.html")), "board/index.html missing")
        self.all = read(".html", ".css", ".js")
        self.low = self.all.lower()

    def has(self, pattern, text=None):
        self.assertRegex(self.low if text is None else text, pattern)

    def test_k01_opens_without_network_or_build(self):
        self.assertNotRegex(self.all, r"(src|href)=[\"']https?://|@import\s+url\(\s*[\"']?https?:|from\s+[\"']https?://|\brequire\(")

    def test_k02_three_default_columns(self):
        self.has(r"to ?do|backlog")
        self.has(r"in progress|doing")
        self.has(r"done|complete")

    def test_k03_add_card(self):
        self.has(r"add (a )?(card|task)|new (card|task)|addcard|addtask|createcard|createtask")

    def test_k04_edit_card(self):
        self.has(r"edit|rename|updatecard|updatetask|contenteditable|savecard|savetask")

    def test_k05_delete_card(self):
        self.has(r"delete|remove")

    def test_k06_drag_and_drop(self):
        self.has(r"dragstart|pointerdown")
        self.has(r"\bdrop\b|ondrop|pointerup|dragend")

    def test_k07_move_without_a_mouse(self):
        self.has(r"keydown|keyup")
        self.has(r"arrow(left|right|up|down)|move (left|right|to)|moveleft|moveright|movecard|movetask")

    def test_k08_saved_between_visits(self):
        self.has(r"localstorage|indexeddb")

    def test_k09_add_columns(self):
        self.has(r"add (a )?(column|list)|new (column|list)|addcolumn|addlist|createcolumn")

    def test_k10_rename_or_delete_columns(self):
        self.has(r"(rename|delete|remove|edit)[ -]?(this )?(column|list)|renamecolumn|deletecolumn|removecolumn")

    def test_k11_card_description(self):
        self.has(r"description|notes|details|<textarea")

    def test_k12_due_dates(self):
        self.has(r"due|deadline|type=[\"']date")

    def test_k13_labels_or_priority(self):
        self.has(r"label|tag|priority")

    def test_k14_search_or_filter(self):
        self.has(r"search|filter")

    def test_k15_export_or_import(self):
        self.has(r"export|import|download|backup")

    def test_k16_undo_or_confirmation_before_losing_work(self):
        self.has(r"undo|confirm\(|are you sure|restore|trash|archive")

    def test_k17_empty_state(self):
        self.has(r"no (cards|tasks)|nothing here|empty|drop (a )?(card|task)s? here|:empty")

    def test_k18_card_counts_or_limits(self):
        self.has(r"count|\.length|wip|limit")
        self.has(r"count|wip|limit|badge")

    def test_k19_dark_mode(self):
        self.has(r"prefers-color-scheme|data-theme|dark-mode|theme-toggle|\.dark\b")

    def test_k20_works_on_phones(self):
        self.has(r"name=[\"']viewport")
        self.has(r"@media[^{]*\((max|min)-width|overflow-x\s*:\s*(auto|scroll)|scroll-snap")

    def test_k21_screen_reader_support(self):
        self.has(r"aria-label|aria-labelledby")
        self.has(r"aria-live|role=[\"'](status|alert|dialog|list|region)|<dialog")

    def test_k22_visible_focus(self):
        self.has(r":focus-visible|:focus\b")

    def test_k23_motion_with_reduced_motion_respected(self):
        self.has(r"transition|animation")
        self.has(r"prefers-reduced-motion")

    def test_k24_keyboard_shortcuts_or_help(self):
        self.has(r"shortcut|press |\bkbd\b|<kbd|ctrl|metakey|cmd\+|key === [\"'](n|/|\?)[\"']")

    def test_k25_escape_closes_things(self):
        self.has(r"escape|<dialog|\besc\b")

    def test_k26_survives_bad_saved_data(self):
        self.has(r"try\s*\{[\s\S]{0,400}json\.parse|json\.parse[\s\S]{0,400}catch")

    def test_k27_user_text_is_not_injected_as_html(self):
        self.has(r"textcontent|createtextnode|innertext|escapehtml|escape\(|sanitize")

    def test_k29_checklists_or_subtasks(self):
        self.has(r"checklist|subtask|sub-task")

    def test_k30_work_in_progress_limits(self):
        self.has(r"\bwip\b|wip[-_ ]?limit|card limit|max(imum)? cards|\blimit\b")

    def test_k31_reorder_columns(self):
        self.has(r"(move|reorder|drag)[\w -]{0,20}(column|list)|movecolumn|reordercolumn|column[\w -]{0,12}(left|right)")

    def test_k32_archive_or_trash(self):
        self.has(r"archive|trash")

    def test_k33_undo(self):
        self.has(r"\bundo\b")

    def test_k34_tabs_stay_in_sync(self):
        self.has(r"addeventlistener\(\s*[\"']storage[\"']|onstorage|broadcastchannel")

    def test_k35_feedback_messages(self):
        self.has(r"toast|snackbar|notif|role=[\"']status|aria-live")

    def test_k36_card_editor_dialog(self):
        self.has(r"<dialog|role=[\"']dialog|modal")

    def test_k37_overdue_is_visible(self):
        self.has(r"overdue|past due|is-late|due-soon|duesoon")

    def test_k38_sort_cards(self):
        self.has(r"\bsort(ed| by|by)?\b[\w -]{0,20}(due|priority|date|title|name)|sortby|sort-by")

    def test_k39_saved_data_has_a_version(self):
        self.has(r"version|schema|migrat")

    def test_k40_reset_or_clear_board(self):
        self.has(r"reset|clear (the )?(board|all|done|completed)|clearboard|cleardone|start over")

    def test_k28_more_than_a_single_script_blob(self):
        files = [n for _, _, names in os.walk(BOARD) for n in names if n.endswith((".html", ".css", ".js"))]
        self.assertGreaterEqual(len(files), 2)
