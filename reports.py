"""Calculations, searching and report generation."""
from collections import defaultdict
from decimal import Decimal

from validators import format_currency


def total(expenses) -> Decimal:
    return sum((e.amount for e in expenses), Decimal("0"))


def average(expenses) -> Decimal:
    return (total(expenses) / len(expenses)).quantize(Decimal("0.01")) if expenses else Decimal("0")


def by_category(expenses) -> dict:
    """Category -> total, sorted by highest spend first."""
    sums = defaultdict(Decimal)
    for e in expenses:
        sums[e.category] += e.amount
    return dict(sorted(sums.items(), key=lambda kv: kv[1], reverse=True))


def filter_month(expenses, year: int, month: int):
    return [e for e in expenses if e.date.year == year and e.date.month == month]


def search(expenses, keyword=None, category=None, start=None, end=None, min_amount=None, max_amount=None):
    results = []
    for e in expenses:
        if keyword and keyword.lower() not in e.description.lower():
            continue
        if category and e.category != category:
            continue
        if start and e.date < start:
            continue
        if end and e.date > end:
            continue
        if min_amount is not None and e.amount < min_amount:
            continue
        if max_amount is not None and e.amount > max_amount:
            continue
        results.append(e)
    return sorted(results, key=lambda e: e.date)


def _bar(share: float, width: int = 20) -> str:
    filled = round(share * width)
    return "█" * filled + "░" * (width - filled)


def category_summary_text(expenses) -> str:
    if not expenses:
        return "No expenses to summarise."
    grand = total(expenses)
    lines = [f"{'Category':<15}{'Count':>6}{'Total':>16}{'Share':>8}  Chart", "-" * 68]
    counts = defaultdict(int)
    for e in expenses:
        counts[e.category] += 1
    for cat, amt in by_category(expenses).items():
        share = float(amt / grand)
        lines.append(f"{cat:<15}{counts[cat]:>6}{format_currency(amt):>16}{share:>7.1%}  {_bar(share)}")
    lines += ["-" * 68,
              f"{'TOTAL':<15}{len(expenses):>6}{format_currency(grand):>16}",
              f"Average per expense: {format_currency(average(expenses))}"]
    return "\n".join(lines)


def monthly_report_text(expenses, year: int, month: int) -> str:
    items = filter_month(expenses, year, month)
    title = f"MONTHLY REPORT - {year}-{month:02d}"
    if not items:
        return f"{title}\n\nNo expenses recorded for this month."
    top = max(items, key=lambda e: e.amount)
    days = {e.date for e in items}
    lines = [title, "=" * len(title),
             f"Transactions     : {len(items)}",
             f"Total spent      : {format_currency(total(items))}",
             f"Average expense  : {format_currency(average(items))}",
             f"Active days      : {len(days)}  (avg {format_currency(total(items) / len(days))}/day)",
             f"Largest expense  : {format_currency(top.amount)} - {top.description} ({top.category})",
             "", "Spending by category:", category_summary_text(items)]
    return "\n".join(lines)
