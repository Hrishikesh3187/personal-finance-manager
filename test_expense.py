import unittest
from datetime import date
from decimal import Decimal

from src.expense import Expense
from src.validators import ValidationError


class TestExpense(unittest.TestCase):
    def setUp(self):
        self.e = Expense(Decimal("1500.00"), "Food", date(2024, 1, 15), "Grocery shopping")

    def test_attributes(self):
        self.assertEqual(self.e.amount, Decimal("1500.00"))
        self.assertEqual(self.e.category, "Food")
        self.assertEqual(self.e.date, date(2024, 1, 15))
        self.assertEqual(self.e.description, "Grocery shopping")

    def test_row_round_trip(self):
        again = Expense.from_row(self.e.to_row())
        self.assertEqual(again.to_row(), self.e.to_row())

    def test_from_row_rejects_bad_data(self):
        bad_rows = [
            {"date": "2024-01-15", "amount": "abc", "category": "Food", "description": "x"},
            {"date": "2024-01-15", "amount": "10", "category": "Nope", "description": "x"},
            {"date": "bad", "amount": "10", "category": "Food", "description": "x"},
            {"date": "2024-01-15", "amount": "10", "category": "Food"},  # missing field
        ]
        for row in bad_rows:
            with self.subTest(row=row):
                with self.assertRaises(ValidationError):
                    Expense.from_row(row)

    def test_str_contains_key_info(self):
        text = str(self.e)
        for part in ["2024-01-15", "Food", "1,500.00", "Grocery shopping"]:
            self.assertIn(part, text)


if __name__ == "__main__":
    unittest.main()
