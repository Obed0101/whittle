"""Everything asked across the four turns: the 32 checks of the first request plus the later additions."""
import importlib.util
import os

_first = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "expense-report", "hidden", "checks.py")
_spec = importlib.util.spec_from_file_location("_first_request", _first)
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)


class OverTime(base.Requirements):
    def test_r33_exclude_ignores_case(self):
        out = "\n".join(self.lines("--exclude", "FOOD"))
        self.assertIn("Flight", out)
        self.assertNotIn("Coffee", out)
        self.assertNotIn("Team lunch", out)

    def test_r34_exclude_repeats(self):
        out = "\n".join(self.lines("--exclude", "food", "--exclude", "Office"))
        self.assertIn("Hotel", out)
        self.assertNotIn("A very long", out)
        self.assertNotIn("Coffee", out)

    def test_r35_exclude_changes_the_total(self):
        self.assertTrue(self.lines("--exclude", "food")[-1].rstrip().endswith("1,624.49"))

    def test_r36_exclude_in_help(self):
        self.assertIn("--exclude", base.run("--help")[1])

    def test_r37_markdown_header_and_alignment_row(self):
        lines = self.lines("--format", "markdown")
        self.assertEqual(lines[0].strip(), "| Date | Category | Amount | Note |")
        self.assertEqual(lines[1].strip(), "| --- | --- | ---: | --- |")

    def test_r38_markdown_rows(self):
        lines = [line.strip() for line in self.lines("--format", "markdown")]
        self.assertIn("| 2026-03-02 | travel | 1,234.50 | Flight to Bogota |", lines)
        self.assertIn("| 2026-03-02 | food | 12.00 | Coffee |", lines)
        self.assertEqual(len(lines), 9)

    def test_r39_markdown_total_row(self):
        self.assertEqual(self.lines("--format", "markdown")[-1].strip(), "| Total | | 1,636.49 | |")

    def test_r40_markdown_notes_not_cut(self):
        self.assertIn("A very long note about printer paper and toner", "\n".join(self.lines("--format", "markdown")))
