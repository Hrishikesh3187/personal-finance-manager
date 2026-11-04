"""Input validation and formatting helpers."""
from datetime import date, datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CATEGORIES = ["Food", "Transport", "Entertainment", "Shopping", "Other"]
CURRENCY = "₹"
MAX_AMOUNT = Decimal("10000000")
MAX_DESC_LEN = 100


class ValidationError(ValueError):
    """Raised when user input fails validation."""


def parse_amount(text: str) -> Decimal:
    cleaned = text.strip().replace(",", "").replace(CURRENCY, "").replace("Rs.", "").strip()
    if not cleaned:
        raise ValidationError("Amount cannot be empty.")
    try:
        value = Decimal(cleaned)
    except InvalidOperation:
        raise ValidationError(f"'{text}' is not a valid number.")
    if not value.is_finite():
        raise ValidationError("Amount must be a finite number.")
    if value <= 0:
        raise ValidationError("Amount must be greater than zero.")
    if value > MAX_AMOUNT:
        raise ValidationError(f"Amount cannot exceed {format_currency(MAX_AMOUNT)}.")
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def parse_category(text: str) -> str:
    cleaned = text.strip()
    if not cleaned:
        raise ValidationError("Category cannot be empty.")
    for cat in CATEGORIES:
        if cat.lower() == cleaned.lower():
            return cat
    raise ValidationError(f"Unknown category '{cleaned}'. Choose from: {', '.join(CATEGORIES)}.")


def parse_date(text: str) -> date:
    cleaned = text.strip()
    try:
        parsed = datetime.strptime(cleaned, "%Y-%m-%d").date()
    except ValueError:
        raise ValidationError("Invalid date. Use YYYY-MM-DD (e.g. 2024-01-15).")
    if parsed > date.today():
        raise ValidationError("Date cannot be in the future.")
    if parsed.year < 1990:
        raise ValidationError("Date is too far in the past (before 1990).")
    return parsed


def parse_description(text: str) -> str:
    cleaned = " ".join(text.split())  # collapse whitespace/newlines
    if not cleaned:
        raise ValidationError("Description cannot be empty.")
    if len(cleaned) > MAX_DESC_LEN:
        raise ValidationError(f"Description too long (max {MAX_DESC_LEN} characters).")
    return cleaned


def parse_month(text: str) -> tuple:
    """Parse 'YYYY-MM' into (year, month)."""
    try:
        parsed = datetime.strptime(text.strip(), "%Y-%m")
    except ValueError:
        raise ValidationError("Invalid month. Use YYYY-MM (e.g. 2024-01).")
    return parsed.year, parsed.month


def parse_menu_choice(text: str, low: int, high: int) -> int:
    try:
        choice = int(text.strip())
    except ValueError:
        raise ValidationError(f"Please enter a number between {low} and {high}.")
    if not low <= choice <= high:
        raise ValidationError(f"Please enter a number between {low} and {high}.")
    return choice


def format_currency(amount) -> str:
    return f"{CURRENCY}{Decimal(amount):,.2f}"
