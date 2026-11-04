# 💰 Personal Finance Manager

A command-line application to track expenses, generate reports and analyse spending patterns. Built in Python with an object-oriented, modular design, CSV data persistence and a menu-driven interface.

## Features

- **Add expenses** with amount, category, date and description
- **Input validation** everywhere: bad input is explained and re-asked, never crashes the program
- **CSV persistence**: data is saved after every change, using atomic writes so a crash cannot corrupt the file
- **Reports**: total, average, category-wise breakdown with bar charts, and a full monthly report
- **Search** by keyword, category, date range and amount range
- **Backup and restore** with validation and an automatic safety copy before restoring
- **Exact money maths** using `Decimal` instead of `float`
- **34 unit tests** covering validation, the `Expense` class, reports and file handling
- **No dependencies**: standard library only

## Screenshots

| Add expense | View all expenses |
|---|---|
| ![Add expense](screenshots/01_add_expense.png) | ![View all](screenshots/02_view_all_expenses.png) |

| Category summary | Monthly report |
|---|---|
| ![Category summary](screenshots/03_category_summary.png) | ![Monthly report](screenshots/04_monthly_report.png) |

## Project structure

```
personal-finance-manager/
├── main.py                  # Entry point
├── requirements.txt         # Dependencies (none needed)
├── README.md
├── src/                     # Source code
│   ├── expense.py           # Expense class
│   ├── validators.py        # Input validation and formatting
│   ├── storage.py           # CSV persistence, backup, restore
│   ├── reports.py           # Calculations, search, report text
│   └── ui.py                # Menu system and prompts
├── data/
│   └── sample_expenses.csv  # Sample data (your own data is git-ignored)
├── docs/
│   └── user_guide.md        # Full user guide
├── tests/                   # Unit tests (unittest)
└── screenshots/             # Application screenshots
```

## Getting started

**Requirements:** Python 3.8 or newer. Check with `python --version`.

```bash
git clone https://github.com/Hrishikesh3187/personal-finance-manager.git
cd personal-finance-manager
python main.py
```

To try it with example data first:

```bash
# macOS / Linux
cp data/sample_expenses.csv data/expenses.csv

# Windows (Command Prompt)
copy data\sample_expenses.csv data\expenses.csv
```

## Usage

```
==========================================
         PERSONAL FINANCE MANAGER
==========================================

MAIN MENU:
1. Add New Expense
2. View All Expenses
3. View Category-wise Summary
4. Generate Monthly Report
5. Search Expenses
6. Backup / Restore Data
7. Exit
```

See the [User Guide](docs/user_guide.md) for details on every option. Type `cancel` at any prompt to return to the menu.

## Running the tests

```bash
python -m unittest discover -s tests -t . -v
```

## Design notes

- **Separation of concerns:** `ui.py` handles only input and output; business logic lives in `reports.py`, file handling in `storage.py`, and rules in `validators.py`, so each can be tested on its own.
- **Validation at the boundary:** every value is checked once by `validators.py`. Rows loaded from CSV go through the same checks, so a hand-edited file can't break the app.
- **Safe persistence:** data is written to a temporary file and then swapped in. Restore validates the backup first and keeps a safety copy of the current data.

## Ideas for future improvements

- Edit and delete expenses
- Monthly budgets with overspend warnings
- Export reports to CSV or PDF
- Recurring expenses
- Charts using matplotlib

## License

Free to use for learning and personal projects.
