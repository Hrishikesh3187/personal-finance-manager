"""Interactive command-line interface."""
from datetime import date

import reports
import validators as v
from expense import Expense
from storage import ExpenseStorage, StorageError

WIDTH = 42


class Cancelled(Exception):
    """User typed 'cancel' during a prompt."""


def ask(prompt, parser, optional=False):
    """Prompt until input parses. Blank returns None if optional; 'cancel' aborts."""
    while True:
        raw = input(prompt).strip()
        if raw.lower() == "cancel":
            raise Cancelled
        if not raw and optional:
            return None
        try:
            return parser(raw)
        except v.ValidationError as exc:
            print(f"❌ {exc}")


def header(title=None):
    print("\n" + "=" * WIDTH)
    print((title or "").center(WIDTH) if title else "")
    print("=" * WIDTH)


class FinanceApp:
    MENU = ["Add New Expense", "View All Expenses", "View Category-wise Summary",
            "Generate Monthly Report", "Search Expenses", "Backup / Restore Data", "Exit"]

    def __init__(self, storage: ExpenseStorage):
        self.storage = storage
        self.expenses, skipped = storage.load()
        if skipped:
            print(f"⚠️  Skipped {skipped} invalid row(s) while loading data.")

    # --- main loop -----------------------------------------------------
    def run(self):
        header("PERSONAL FINANCE MANAGER")
        actions = {1: self.add_expense, 2: self.view_all, 3: self.category_summary,
                   4: self.monthly_report, 5: self.search, 6: self.backup_menu}
        while True:
            print("\nMAIN MENU:")
            for i, item in enumerate(self.MENU, 1):
                print(f"{i}. {item}")
            choice = ask(f"\nEnter your choice (1-{len(self.MENU)}): ",
                         lambda t: v.parse_menu_choice(t, 1, len(self.MENU)))
            if choice == len(self.MENU):
                print("\n👋 Goodbye! Keep tracking your spending.")
                return
            try:
                actions[choice]()
            except Cancelled:
                print("\n↩️  Cancelled.")
            except StorageError as exc:
                print(f"\n❌ {exc}")

    # --- features ------------------------------------------------------
    def add_expense(self):
        print("\nADD NEW EXPENSE:  (type 'cancel' at any prompt to abort)")
        amount = ask("Enter amount: ", v.parse_amount)
        category = ask(f"Enter category ({'/'.join(v.CATEGORIES)}): ", v.parse_category)
        when = ask("Enter date (YYYY-MM-DD): ", v.parse_date)
        desc = ask("Enter description: ", v.parse_description)
        self.expenses.append(Expense(amount, category, when, desc))
        try:
            self.storage.save(self.expenses)
        except StorageError:
            self.expenses.pop()  # keep memory consistent with disk
            raise
        print("\n✅ Expense added successfully!")

    def _print_table(self, items):
        print(f"\n{'#':>3}  {'Date':<10}  {'Category':<13} {'Amount':>14}  Description")
        print("-" * 70)
        for i, e in enumerate(items, 1):
            print(f"{i:>3}  {e}")
        print("-" * 70)
        print(f"{len(items)} expense(s) | Total: {v.format_currency(reports.total(items))}"
              f" | Average: {v.format_currency(reports.average(items))}")

    def view_all(self):
        if not self.expenses:
            print("\nNo expenses recorded yet.")
            return
        self._print_table(sorted(self.expenses, key=lambda e: e.date))

    def category_summary(self):
        print("\nCATEGORY-WISE SUMMARY:\n")
        print(reports.category_summary_text(self.expenses))

    def monthly_report(self):
        today = date.today()
        default = f"{today.year}-{today.month:02d}"
        print(f"\nGENERATE MONTHLY REPORT  (blank = {default})")
        raw = ask("Enter month (YYYY-MM): ", lambda t: v.parse_month(t), optional=True)
        year, month = raw or (today.year, today.month)
        print("\n" + reports.monthly_report_text(self.expenses, year, month))

    def search(self):
        print("\nSEARCH EXPENSES  (press Enter to skip any filter)")
        keyword = ask("Keyword in description: ", v.parse_description, optional=True)
        category = ask(f"Category ({'/'.join(v.CATEGORIES)}): ", v.parse_category, optional=True)
        start = ask("From date (YYYY-MM-DD): ", v.parse_date, optional=True)
        end = ask("To date (YYYY-MM-DD): ", v.parse_date, optional=True)
        if start and end and start > end:
            print("❌ 'From' date is after 'To' date.")
            return
        lo = ask("Minimum amount: ", v.parse_amount, optional=True)
        hi = ask("Maximum amount: ", v.parse_amount, optional=True)
        if lo is not None and hi is not None and lo > hi:
            print("❌ Minimum amount is greater than maximum.")
            return
        results = reports.search(self.expenses, keyword, category, start, end, lo, hi)
        if results:
            self._print_table(results)
        else:
            print("\nNo matching expenses found.")

    def backup_menu(self):
        print("\nBACKUP / RESTORE:\n1. Create backup now\n2. Restore from a backup\n3. Back")
        choice = ask("Choice (1-3): ", lambda t: v.parse_menu_choice(t, 1, 3))
        if choice == 1:
            path = self.storage.create_backup()
            print(f"\n✅ Backup created: {path.name}")
        elif choice == 2:
            backups = self.storage.list_backups()
            if not backups:
                print("\nNo backups found.")
                return
            print("\nAvailable backups (newest first):")
            for i, b in enumerate(backups, 1):
                print(f"{i}. {b.name}")
            idx = ask(f"Select backup (1-{len(backups)}): ",
                      lambda t: v.parse_menu_choice(t, 1, len(backups)))
            confirm = input("This replaces current data (a safety backup is made first). Continue? (y/n): ")
            if confirm.strip().lower() != "y":
                print("\n↩️  Restore cancelled.")
                return
            count, skipped = self.storage.restore_backup(backups[idx - 1])
            self.expenses, _ = self.storage.load()
            print(f"\n✅ Restored {count} expense(s)." + (f" ({skipped} invalid row(s) skipped.)" if skipped else ""))
