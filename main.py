"""Entry point: python main.py"""
import sys

from storage import ExpenseStorage, StorageError
from ui import FinanceApp


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # so ₹ and emoji print on Windows
    try:
        app = FinanceApp(ExpenseStorage())
        app.run()
    except StorageError as exc:
        print(f"❌ Fatal storage error: {exc}")
        sys.exit(1)
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Interrupted. Your saved data is safe. Goodbye!")


if __name__ == "__main__":
    main()
