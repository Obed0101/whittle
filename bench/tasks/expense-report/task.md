# Expense report command

Finance wants a command that turns our expense CSV into a report they can paste into an email or feed to other tools. Please build it.

Put it in `app/report.py` as `main(argv: list[str]) -> int`, where `argv` excludes the program name and the return value is the exit code. `python -m app.report expenses.csv` has to work too. The report goes to stdout and problems go to stderr. Read the file with the existing `app.expenses.load`.

`python -m app.report PATH [options]`

## The table

With no options it prints a table with the columns Date, Category, Amount and Note, in that order, under a header row, with a line of dashes below the header. Rows are sorted by date, oldest first; rows that share a date stay in file order.

Amounts always show two decimals and a comma as thousands separator (`1,234.50`), and the Amount column is right-aligned. A note longer than 24 characters is cut to its first 23 characters followed by `…`. The last line starts with `Total` and ends with the sum of the rows shown.

If there is nothing to show, print just `No expenses.` and exit 0.

## Filters

- `--category NAME` keeps one category. Matching ignores case, and the flag can be given several times to keep several categories.
- `--from DATE` and `--to DATE` (YYYY-MM-DD) bound the dates, both inclusive.
- `--min AMOUNT` keeps expenses of at least that amount.

## Grouping

`--by category` prints one line per category instead of one per expense, with the columns Category, Count and Total: how many expenses and their subtotal. Largest subtotal first; equal subtotals in alphabetical order. `--by month` does the same per month (`2026-03`), with the first column named Month, oldest month first. Grouped output also ends with the `Total` line.

In the table, category names in grouped output should be title-cased (`travel` becomes `Travel`). JSON keeps them as they are in the file.

## Other formats

`--format json` prints an array of objects with `date`, `category`, `amount` (a number, not a string) and `note`, indented with two spaces, ending in a newline. With `--by` the objects are `{"group", "count", "total"}` instead.

`--format csv` prints the header `date,category,amount,note` and one line per expense, amounts with two decimals and no thousands separator, quoted properly when a note contains a comma.

Notes are only cut in the table, never in JSON or CSV.

`--currency SYMBOL` puts the symbol in front of amounts in the table (`$1,234.50`). JSON and CSV are not affected.

## When things go wrong

- File does not exist: `error: file not found: PATH` on stderr, exit 2.
- A date that is not a real date: `error: invalid date: VALUE`, exit 2.
- `--from` later than `--to`: `error: --from is after --to`, exit 2.
- An unknown `--format` value: exit 2.
- A row whose amount is not a number is left out of the report. After the report, print `warning: skipped 1 row with invalid amount` on stderr (or `skipped 3 rows with invalid amount`; get the plural right) and still exit 0. Count every such row in the file, whatever the filters.

## A few more things

- It would be good if `--top N` showed only the N largest expenses, largest first.
- Ideally refunds (negative amounts) show in parentheses in the table, like `(45.00)`, and still subtract from the total.
- `--no-header` should drop the header row and the dashes, for piping into other tools.
- `--help` should mention every flag and include one usage line that starts with `Example:`.
