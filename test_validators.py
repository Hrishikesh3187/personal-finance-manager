import unittest
from datetime import date
from decimal import Decimal

from src import validators as v


class TestAmount(unittest.TestCase):
    def test_valid_amounts(self):
        self.assertEqual(v.parse_amount("1500"), Decimal("1500.00"))
        self.assertEqual(v.parse_amount("1,500.5"), Decimal("1500.50"))
        self.assertEqual(v.parse_amount("₹250"), Decimal("250.00"))

    def test_rounds_to_two_decimals(self):
        self.assertEqual(v.parse_amount("12.345"), Decimal("12.35"))

    def test_invalid_amounts(self):
        for bad in ["", "abc", "0", "-5", "NaN", "Infinity", "10000001"]:
            with self.subTest(bad=bad):
                with self.assertRaises(v.ValidationError):
                    v.parse_amount(bad)


class TestCategory(unittest.TestCase):
    def test_case_insensitive(self):
        self.assertEqual(v.parse_category("food"), "Food")
        self.assertEqual(v.parse_category("  TRANSPORT "), "Transport")

    def test_invalid(self):
        for bad in ["", "Groceries"]:
            with self.assertRaises(v.ValidationError):
                v.parse_category(bad)


class TestDate(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(v.parse_date("2024-01-15"), date(2024, 1, 15))

    def test_invalid_formats(self):
        for bad in ["", "15-01-2024", "2024-13-45", "2024/01/15", "hello"]:
            with self.assertRaises(v.ValidationError):
                v.parse_date(bad)

    def test_future_and_too_old(self):
        with self.assertRaises(v.ValidationError):
            v.parse_date("2999-01-01")
        with self.assertRaises(v.ValidationError):
            v.parse_date("1980-01-01")


class TestDescriptionMonthMenu(unittest.TestCase):
    def test_description_cleanup(self):
        self.assertEqual(v.parse_description("  Grocery    shopping "), "Grocery shopping")

    def test_description_invalid(self):
        with self.assertRaises(v.ValidationError):
            v.parse_description("   ")
        with self.assertRaises(v.ValidationError):
            v.parse_description("x" * (v.MAX_DESC_LEN + 1))

    def test_month(self):
        self.assertEqual(v.parse_month("2024-01"), (2024, 1))
        with self.assertRaises(v.ValidationError):
            v.parse_month("2024-13")

    def test_menu_choice(self):
        self.assertEqual(v.parse_menu_choice("3", 1, 7), 3)
        for bad in ["0", "8", "x", ""]:
            with self.assertRaises(v.ValidationError):
                v.parse_menu_choice(bad, 1, 7)

    def test_format_currency(self):
        self.assertEqual(v.format_currency(1500), "₹1,500.00")
        self.assertEqual(v.format_currency(Decimal("0.5")), "₹0.50")


if __name__ == "__main__":
    unittest.main()
