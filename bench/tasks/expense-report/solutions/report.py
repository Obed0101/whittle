"""Expense report command. Reference solution: validates the hidden checks, not a benchmark output."""
import argparse
import csv
import json
import sys
from datetime import date
from decimal import Decimal, InvalidOperation

from app.expenses import load


class Fail(Exception):
    pass


def money(value, symbol=""):
    text = f"{symbol}{abs(value):,.2f}"
    return f"({text})" if value < 0 else text


def parse_date(text):
    try:
        return date.fromisoformat(text) if text else None
    except ValueError:
        raise Fail(f"invalid date: {text}")


def table(headers, rows, right, header):
    widths = [max(len(str(row[i])) for row in [headers, *rows]) for i in range(len(headers))]
    line = lambda row: "  ".join(str(c).rjust(w) if i in right else str(c).ljust(w) for i, (c, w) in enumerate(zip(row, widths))).rstrip()
    head = [line(headers), "-" * len(line(headers))] if header else []
    return "\n".join(head + [line(row) for row in rows])


def groups(rows, by):
    out = {}
    for row in rows:
        key = row["category"] if by == "category" else row["date"][:7]
        count, total = out.get(key, (0, Decimal(0)))
        out[key] = (count + 1, total + row["amount"])
    order = (lambda item: (-item[1][1], item[0])) if by == "category" else (lambda item: item[0])
    return [(name, count, total) for name, (count, total) in sorted(out.items(), key=order)]


def main(argv):
    parser = argparse.ArgumentParser(
        prog="python -m app.report", description="Print an expense report from a CSV file.",
        epilog="Example: python -m app.report expenses.csv --by category --format json",
    )
    parser.add_argument("path")
    parser.add_argument("--category", action="append", help="keep this category; repeat for several")
    parser.add_argument("--from", dest="start", help="first date, YYYY-MM-DD")
    parser.add_argument("--to", dest="end", help="last date, YYYY-MM-DD")
    parser.add_argument("--min", type=Decimal, help="smallest amount to keep")
    parser.add_argument("--by", choices=["category", "month"], help="group the report")
    parser.add_argument("--format", choices=["table", "json", "csv"], default="table")
    parser.add_argument("--currency", default="", help="symbol put before amounts in the table")
    parser.add_argument("--top", type=int, help="show only the N largest expenses")
    parser.add_argument("--no-header", action="store_true", help="omit the table header")
    args = parser.parse_args(argv)

    try:
        start, end = parse_date(args.start), parse_date(args.end)
        if start and end and start > end:
            raise Fail("--from is after --to")
        try:
            loaded = load(args.path)
        except FileNotFoundError:
            raise Fail(f"file not found: {args.path}")
    except Fail as problem:
        print(f"error: {problem}", file=sys.stderr)
        return 2

    wanted = {name.lower() for name in args.category or []}
    rows, skipped = [], 0
    for raw in loaded:
        try:
            amount = Decimal(raw["amount"])
        except InvalidOperation:
            skipped += 1
            continue
        when = date.fromisoformat(raw["date"])
        if wanted and raw["category"].lower() not in wanted:
            continue
        if (start and when < start) or (end and when > end) or (args.min is not None and amount < args.min):
            continue
        rows.append({**raw, "amount": amount})
    rows.sort(key=lambda row: row["date"])
    if args.top is not None:
        rows = sorted(rows, key=lambda row: row["amount"], reverse=True)[: args.top]
    total = sum((row["amount"] for row in rows), Decimal(0))
    grouped = groups(rows, args.by) if args.by else None

    if args.format == "json":
        data = ([{"group": n, "count": c, "total": float(t)} for n, c, t in grouped] if grouped is not None
                else [{**row, "amount": float(row["amount"])} for row in rows])
        print(json.dumps(data, indent=2, ensure_ascii=False))
    elif args.format == "csv":
        writer = csv.writer(sys.stdout, lineterminator="\n")
        if grouped is not None:
            writer.writerows([["group", "count", "total"], *([n, c, f"{t:.2f}"] for n, c, t in grouped)])
        else:
            writer.writerows([["date", "category", "amount", "note"], *([r["date"], r["category"], f"{r['amount']:.2f}", r["note"]] for r in rows)])
    elif not rows:
        print("No expenses.")
    elif grouped is not None:
        body = [[n.title() if args.by == "category" else n, c, money(t, args.currency)] for n, c, t in grouped]
        body.append(["Total", len(rows), money(total, args.currency)])
        print(table(["Category" if args.by == "category" else "Month", "Count", "Total"], body, {1, 2}, not args.no_header))
    else:
        cut = lambda note: note if len(note) <= 24 else note[:23] + "…"
        body = [[r["date"], r["category"], money(r["amount"], args.currency), cut(r["note"])] for r in rows]
        body.append(["Total", "", money(total, args.currency), ""])
        print(table(["Date", "Category", "Amount", "Note"], body, {2}, not args.no_header))

    if skipped:
        print(f"warning: skipped {skipped} row{'' if skipped == 1 else 's'} with invalid amount", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
