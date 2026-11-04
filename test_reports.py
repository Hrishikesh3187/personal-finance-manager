import unittest
from datetime import date
from decimal import Decimal

from src import reports
from src.expense import Expense


def make(amount, cat, d, desc):
    return Expense(Decimal(amount), cat, d, desc)


class TestReports(unittest.TestCase):
    def setUp(self):
        self.items = [
            make("1500", "Food", date(2024, 1, 15), "Grocery shopping"),
            make("250", "Transport", date(2024, 1, 20), "Bus pass"),
            make("3200", "Shopping", date(2024, 1, 25), "Shoes"),
            make("900", "Entertainment", date(2024, 2, 2), "Movie night"),
        ]

    def test_total_and_average(self):
        self.assertEqual(reports.total(self.items), Decimal("5850"))
        self.assertEqual(reports.average(self.items), Decimal("1462.50"))

    def test_empty_list(self):
        self.assertEqual(reports.total([]), Decimal("0"))
        self.assertEqual(reports.average([]), Decimal("0"))

    def test_by_category_sorted_desc(self):
        result = reports.by_category(self.items)
        self.assertEqual(list(result)[0], "Shopping")
        self.assertEqual(result["Food"], Decimal("1500"))

    def test_filter_month(self):
        self.assertEqual(len(reports.filter_month(self.items, 2024, 1)), 3)
        self.assertEqual(len(reports.filter_month(self.items, 2024, 2)), 1)
        self.assertEqual(reports.filter_month(self.items, 2023, 1), [])

    def test_search_filters(self):
        self.assertEqual(len(reports.search(self.items, keyword="shop")), 1)
        self.assertEqual(len(reports.search(self.items, category="Food")), 1)
        self.assertEqual(len(reports.search(self.items, start=date(2024, 1, 20), end=date(2024, 2, 1))), 2)
        self.assertEqual(len(reports.search(self.items, min_amount=Decimal("1000"))), 2)
        self.assertEqual(len(reports.search(self.items, max_amount=Decimal("300"))), 1)
        self.assertEqual(len(reports.search(self.items)), 4)

    def test_search_results_sorted_by_date(self):
        dates = [e.date for e in reports.search(self.items)]
        self.assertEqual(dates, sorted(dates))

    def test_monthly_report_text(self):
        text = reports.monthly_report_text(self.items, 2024, 1)
        self.assertIn("MONTHLY REPORT - 2024-01", text)
        self.assertIn("₹4,950.00", text)
        self.assertIn("Shoes", text)  # largest expense

    def test_monthly_report_empty_month(self):
        self.assertIn("No expenses recorded", reports.monthly_report_text(self.items, 2020, 5))

    def test_category_summary_empty(self):
        self.assertIn("No expenses", reports.category_summary_text([]))


if __name__ == "__main__":
    unittest.main()
