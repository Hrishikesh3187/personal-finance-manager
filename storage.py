"""CSV persistence, backup and restore."""
import csv
import os
import shutil
from datetime import datetime
from pathlib import Path

from expense import Expense
from validators import ValidationError

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
BACKUP_DIR = DATA_DIR / "backups"


class StorageError(Exception):
    """Raised for file-related failures."""


class ExpenseStorage:
    def __init__(self, filepath: Path = DATA_DIR / "expenses.csv", backup_dir: Path = BACKUP_DIR):
        self.filepath = Path(filepath)
        self.backup_dir = Path(backup_dir)
        try:
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            self.backup_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise StorageError(f"Cannot create data folders: {exc}")

    # --- reading / writing --------------------------------------------
    @staticmethod
    def _read_file(path: Path):
        """Return (expenses, skipped_count). Raises StorageError on I/O problems."""
        expenses, skipped = [], 0
        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None or set(Expense.FIELDS) - set(reader.fieldnames):
                    raise StorageError(f"'{path.name}' is not a valid expense file "
                                       f"(expected columns: {', '.join(Expense.FIELDS)}).")
                for row in reader:
                    try:
                        expenses.append(Expense.from_row(row))
                    except ValidationError:
                        skipped += 1
        except FileNotFoundError:
            raise StorageError(f"File not found: {path}")
        except (OSError, UnicodeDecodeError, csv.Error) as exc:
            raise StorageError(f"Could not read '{path.name}': {exc}")
        return expenses, skipped

    def load(self):
        """Load all expenses. Missing file means an empty list."""
        if not self.filepath.exists():
            return [], 0
        return self._read_file(self.filepath)

    def save(self, expenses) -> None:
        """Atomically write all expenses (temp file + replace avoids corruption)."""
        tmp = self.filepath.with_suffix(".tmp")
        try:
            with open(tmp, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=Expense.FIELDS)
                writer.writeheader()
                writer.writerows(e.to_row() for e in expenses)
            os.replace(tmp, self.filepath)
        except OSError as exc:
            raise StorageError(f"Could not save data: {exc}")

    # --- backup / restore ---------------------------------------------
    def create_backup(self) -> Path:
        if not self.filepath.exists():
            raise StorageError("Nothing to back up yet - add an expense first.")
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = self.backup_dir / f"expenses_backup_{stamp}.csv"
        try:
            shutil.copy2(self.filepath, target)
        except OSError as exc:
            raise StorageError(f"Backup failed: {exc}")
        return target

    def list_backups(self):
        return sorted(self.backup_dir.glob("expenses_backup_*.csv"), reverse=True)

    def restore_backup(self, backup_path: Path):
        """Validate the backup, snapshot current data, then replace it.
        Returns (restored_count, skipped_count)."""
        expenses, skipped = self._read_file(backup_path)  # validates first
        if self.filepath.exists():
            self.create_backup()  # safety copy of current data
        self.save(expenses)
        return len(expenses), skipped
