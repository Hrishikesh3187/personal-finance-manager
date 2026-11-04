import tempfile
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path

from src.expense import Expense
from src.storage import ExpenseStorage, StorageError


def make(amount, desc):
    return Expense(Decimal(amount), "Food", date(2024, 1, 15), desc)


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.store = ExpenseStorage(root / "expenses.csv", root / "backups")

    def tearDown(self):
        self.tmp.cleanup()

    def test_load_missing_file_is_empty(self):
        self.assertEqual(self.store.load(), ([], 0))

    def test_save_and_load_round_trip(self):
        self.store.save([make("10", "a"), make("20.50", "b, with comma")])
        items, skipped = self.store.load()
        self.assertEqual(skipped, 0)
        self.assertEqual([e.description for e in items], ["a", "b, with comma"])
        self.assertEqual(items[1].amount, Decimal("20.50"))

    def test_invalid_rows_are_skipped(self):
        self.store.save([make("10", "good")])
        with open(self.store.filepath, "a", encoding="utf-8") as f:
            f.write("not-a-date,abc,Nope,bad row\n")
        items, skipped = self.store.load()
        self.assertEqual(len(items), 1)
        self.assertEqual(skipped, 1)

    def test_backup_requires_data(self):
        with self.assertRaises(StorageError):
            self.store.create_backup()

    def test_backups_never_overwrite_each_other(self):
        self.store.save([make("10", "a")])
        first = self.store.create_backup()
        second = self.store.create_backup()
        self.assertNotEqual(first, second)
        self.assertEqual(len(self.store.list_backups()), 2)

    def test_restore_replaces_current_data(self):
        self.store.save([make("10", "original")])
        backup = self.store.create_backup()
        self.store.save([make("10", "original"), make("99", "added later")])
        restored, skipped = self.store.restore_backup(backup)
        self.assertEqual((restored, skipped), (1, 0))
        self.assertEqual([e.description for e in self.store.load()[0]], ["original"])
        self.assertEqual(len(self.store.list_backups()), 2)  # includes the safety copy

    def test_restore_rejects_invalid_file(self):
        bad = Path(self.tmp.name) / "bad.csv"
        bad.write_text("foo,bar\n1,2\n", encoding="utf-8")
        self.store.save([make("10", "keep me")])
        with self.assertRaises(StorageError):
            self.store.restore_backup(bad)
        self.assertEqual(len(self.store.load()[0]), 1)  # data untouched

    def test_restore_missing_file(self):
        with self.assertRaises(StorageError):
            self.store.restore_backup(Path(self.tmp.name) / "nope.csv")


if __name__ == "__main__":
    unittest.main()
