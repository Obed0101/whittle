"""One test per requirement of task.md. Kept outside the repository the agent works in."""
import contextlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

ROWS = """date,category,amount,note
2026-03-02,travel,1234.5,Flight to Bogota
2026-01-15,food,45.25,Team lunch
2026-03-02,food,12,Coffee
2026-02-10,travel,300,"Hotel, two nights"
2026-02-20,office,89.99,A very long note about printer paper and toner
2026-01-20,food,-45.25,Refund for cancelled lunch
"""
MONEY = re.compile(r"\(?[^\s\d(]?[\d,]+\.\d\d\)?")


def run(*argv):
    """Call main(argv); returns (exit code, stdout, stderr). SystemExit counts as the exit code."""
    from app.report import main
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = main(list(argv))
        except SystemExit as exit_:
            code = exit_.code
    return (0 if code is None else code), out.getvalue(), err.getvalue()


class Requirements(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.path = self.write(ROWS)

    def write(self, text, name="expenses.csv"):
        path = os.path.join(self.dir.name, name)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
        return path

    def lines(self, *argv):
        code, out, _ = run(self.path, *argv)
        self.assertEqual(code, 0)
        return [line for line in out.splitlines() if line.strip()]

    def test_r01_table_header_columns_in_order(self):
        self.assertEqual(self.lines()[0].split(), ["Date", "Category", "Amount", "Note"])

    def test_r02_dashes_under_header(self):
        rule = self.lines()[1].strip()
        self.assertTrue(rule and set(rule) <= {"-", " "}, rule)

    def test_r03_sorted_by_date_keeping_file_order_on_ties(self):
        rows = [line for line in self.lines() if line.startswith("2026-")]
        self.assertEqual([r[:10] for r in rows], sorted(r[:10] for r in rows))
        text = "\n".join(rows)
        self.assertLess(text.index("Flight"), text.index("Coffee"))

    def test_r04_amounts_two_decimals_thousands_right_aligned(self):
        rows = [line for line in self.lines() if line.startswith("2026-") and "Refund" not in line]
        text = "\n".join(rows)
        self.assertIn("1,234.50", text)
        self.assertIn("12.00", text)
        self.assertIn("300.00", text)
        ends = {MONEY.search(line[10:]).end() for line in rows}
        self.assertEqual(len(ends), 1, "amount column is not right-aligned")

    def test_r05_long_note_cut_to_23_chars_and_ellipsis(self):
        out = "\n".join(self.lines())
        self.assertIn("A very long note about …", out)
        self.assertNotIn("printer", out)

    def test_r06_total_line(self):
        last = self.lines()[-1]
        self.assertTrue(last.startswith("Total"), last)
        self.assertTrue(last.rstrip().endswith("1,636.49"), last)

    def test_r07_nothing_to_show(self):
        code, out, _ = run(self.path, "--category", "nothing")
        self.assertEqual((code, out.strip()), (0, "No expenses."))

    def test_r08_category_filter_ignores_case_and_repeats(self):
        one = "\n".join(self.lines("--category", "FOOD"))
        self.assertIn("Coffee", one)
        self.assertNotIn("Flight", one)
        two = "\n".join(self.lines("--category", "food", "--category", "Office"))
        self.assertIn("Coffee", two)
        self.assertIn("A very long", two)
        self.assertNotIn("Flight", two)

    def test_r09_from_is_inclusive(self):
        out = "\n".join(self.lines("--from", "2026-02-10"))
        self.assertIn("Hotel", out)
        self.assertNotIn("Team lunch", out)

    def test_r10_to_is_inclusive(self):
        out = "\n".join(self.lines("--to", "2026-02-10"))
        self.assertIn("Hotel", out)
        self.assertNotIn("Flight", out)

    def test_r11_min_amount_is_inclusive(self):
        out = "\n".join(self.lines("--min", "89.99"))
        self.assertIn("A very long", out)
        self.assertNotIn("Coffee", out)
        self.assertNotIn("Team lunch", out)

    def test_r12_by_category_columns_and_order(self):
        lines = self.lines("--by", "category")
        self.assertEqual(lines[0].split(), ["Category", "Count", "Total"])
        names = [line.split()[0].lower() for line in lines[2:-1]]
        self.assertEqual(names, ["travel", "office", "food"])

    def test_r13_by_month_oldest_first(self):
        lines = self.lines("--by", "month")
        self.assertEqual(lines[0].split()[0], "Month")
        body = [line.split() for line in lines[2:-1]]
        self.assertEqual([row[0] for row in body], ["2026-01", "2026-02", "2026-03"])
        self.assertEqual([row[-1] for row in body], ["0.00", "389.99", "1,246.50"])

    def test_r14_grouped_output_ends_with_total(self):
        for by in ("category", "month"):
            last = self.lines("--by", by)[-1]
            self.assertTrue(last.startswith("Total") and last.rstrip().endswith("1,636.49"), last)

    def test_r15_grouped_count_column(self):
        lines = self.lines("--by", "category")
        travel = next(line.split() for line in lines if line.lower().startswith("travel"))
        self.assertEqual(travel[1:], ["2", "1,534.50"])
        food = next(line.split() for line in lines if line.lower().startswith("food"))
        self.assertEqual(food[1:], ["3", "12.00"])

    def test_r16_json_rows(self):
        code, out, _ = run(self.path, "--format", "json")
        data = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(len(data), 6)
        self.assertEqual(set(data[0]), {"date", "category", "amount", "note"})
        flight = next(row for row in data if row["note"] == "Flight to Bogota")
        self.assertIsInstance(flight["amount"], (int, float))
        self.assertEqual(flight["amount"], 1234.5)
        self.assertEqual([row["date"] for row in data], sorted(row["date"] for row in data))

    def test_r17_json_groups(self):
        data = json.loads(run(self.path, "--format", "json", "--by", "category")[1])
        # Letter case of the group name belongs to r30 alone, so one defect is not counted twice.
        self.assertEqual({**data[0], "group": data[0]["group"].lower()}, {"group": "travel", "count": 2, "total": 1534.5})
        self.assertEqual([g["group"].lower() for g in data], ["travel", "office", "food"])

    def test_r18_json_two_space_indent_and_final_newline(self):
        out = run(self.path, "--format", "json")[1]
        self.assertTrue(out.endswith("\n"))
        self.assertTrue(out.splitlines()[1].startswith("  {"), out[:40])
        self.assertTrue(out.splitlines()[2].startswith("    \""), out[:60])

    def test_r19_csv_format(self):
        lines = run(self.path, "--format", "csv")[1].splitlines()
        self.assertEqual(lines[0], "date,category,amount,note")
        self.assertIn('2026-02-10,travel,300.00,"Hotel, two nights"', lines)
        self.assertIn("2026-03-02,travel,1234.50,Flight to Bogota", lines)

    def test_r20_notes_not_cut_outside_the_table(self):
        self.assertIn("printer paper and toner", run(self.path, "--format", "json")[1])
        self.assertIn("printer paper and toner", run(self.path, "--format", "csv")[1])

    def test_r21_currency_symbol_only_in_table(self):
        self.assertIn("$1,234.50", "\n".join(self.lines("--currency", "$")))
        self.assertNotIn("$", run(self.path, "--currency", "$", "--format", "json")[1])
        self.assertNotIn("$", run(self.path, "--currency", "$", "--format", "csv")[1])

    def test_r22_missing_file(self):
        missing = os.path.join(self.dir.name, "nope.csv")
        code, _, err = run(missing)
        self.assertEqual((code, err.strip()), (2, f"error: file not found: {missing}"))

    def test_r23_invalid_date(self):
        code, _, err = run(self.path, "--from", "2026-13-01")
        self.assertEqual((code, err.strip()), (2, "error: invalid date: 2026-13-01"))

    def test_r24_from_after_to(self):
        code, _, err = run(self.path, "--from", "2026-03-01", "--to", "2026-01-01")
        self.assertEqual((code, err.strip()), (2, "error: --from is after --to"))

    def test_r25_unknown_format_exits_2(self):
        self.assertEqual(run(self.path, "--format", "xml")[0], 2)

    def test_r26_invalid_amount_rows_skipped_with_plural_warning(self):
        one = self.write(ROWS + "2026-04-01,food,abc,Bad\n", "one.csv")
        code, out, err = run(one)
        self.assertEqual(code, 0)
        self.assertIn("1,636.49", out)
        self.assertNotIn("Bad", out)
        self.assertEqual(err.strip(), "warning: skipped 1 row with invalid amount")
        two = self.write(ROWS + "2026-04-01,food,abc,Bad\n2026-04-02,office,,Worse\n", "two.csv")
        code, _, err = run(two, "--category", "travel")
        self.assertEqual((code, err.strip()), (0, "warning: skipped 2 rows with invalid amount"))

    def test_r27_top_n_largest_first(self):
        rows = [line for line in self.lines("--top", "2") if line.startswith("2026-")]
        self.assertEqual(len(rows), 2)
        self.assertIn("Flight", rows[0])
        self.assertIn("Hotel", rows[1])

    def test_r28_refunds_in_parentheses_still_subtract(self):
        lines = self.lines()
        self.assertIn("(45.25)", "\n".join(lines))
        self.assertTrue(lines[-1].rstrip().endswith("1,636.49"))

    def test_r29_no_header(self):
        lines = self.lines("--no-header")
        self.assertTrue(lines[0].startswith("2026-01-15"), lines[0])
        self.assertNotIn("Date", "\n".join(lines))
        self.assertFalse(any(set(line.strip()) <= {"-", " "} for line in lines))

    def test_r30_group_names_title_cased_in_table_only(self):
        self.assertIn("Travel", "\n".join(self.lines("--by", "category")))
        raw = run(self.path, "--by", "category", "--format", "json")[1]
        self.assertIn('"travel"', raw)
        self.assertNotIn("Travel", raw)

    def test_r31_help_lists_every_flag_and_an_example(self):
        code, out, _ = run("--help")
        self.assertEqual(code, 0)
        for flag in ("--category", "--from", "--to", "--min", "--by", "--format", "--currency", "--top", "--no-header"):
            self.assertIn(flag, out)
        self.assertTrue(any(line.strip().startswith("Example:") for line in out.splitlines()), out)

    def test_r32_runs_as_a_module(self):
        done = subprocess.run([sys.executable, "-m", "app.report", self.path, "--by", "month"],
                              capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=30)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("2026-02", done.stdout)


if __name__ == "__main__":
    unittest.main()
