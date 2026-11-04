"""Expense domain class."""
from datetime import date
from decimal import Decimal

import validators as v


class Expense:
    FIELDS = ["date", "amount", "category", "description"]

    def __init__(self, amount: Decimal, category: str, expense_date: date, description: str):
        self.amount = amount
        self.category = category
        self.date = expense_date
        self.description = description

    # --- serialisation -------------------------------------------------
    def to_row(self) -> dict:
        return {
            "date": self.date.isoformat(),
            "amount": str(self.amount),
            "category": self.category,
            "description": self.description,
        }

    @classmethod
    def from_row(cls, row: dict) -> "Expense":
        """Build an Expense from a CSV row; raises ValidationError if invalid."""
        try:
            return cls(
                v.parse_amount(row["amount"]),
                v.parse_category(row["category"]),
                v.parse_date(row["date"]),
                v.parse_description(row["description"]),
            )
        except (KeyError, TypeError, AttributeError):
            raise v.ValidationError("Row is missing required fields.")

    # --- display -------------------------------------------------------
    def __str__(self) -> str:
        return (f"{self.date.isoformat()}  {self.category:<13} "
                f"{v.format_currency(self.amount):>14}  {self.description}")

    def __repr__(self) -> str:
        return f"Expense({self.amount}, {self.category!r}, {self.date}, {self.description!r})"
