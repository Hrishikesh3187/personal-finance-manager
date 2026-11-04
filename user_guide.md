# User Guide

A step-by-step guide to using the Personal Finance Manager.

## 1. Starting the program

Open a terminal in the project folder and run:

```bash
python main.py
```

(On some systems use `python3 main.py`.) You will see the main menu. Type a number from 1 to 7 and press Enter.

> **Tip:** Type `cancel` at any prompt to go back to the menu without saving anything.

## 2. Menu options

### 1. Add New Expense
You will be asked for four things:

| Prompt | What to type | Example |
|---|---|---|
| Amount | A positive number (commas allowed) | `1500` or `1,500.50` |
| Category | Food, Transport, Entertainment, Shopping or Other (not case-sensitive) | `food` |
| Date | `YYYY-MM-DD`, today or earlier | `2024-01-15` |
| Description | Up to 100 characters | `Grocery shopping` |

If you type something invalid, the program tells you why and asks again. Valid expenses are saved to disk immediately.

### 2. View All Expenses
Shows every expense sorted by date, followed by the count, total and average.

### 3. View Category-wise Summary
Shows, for each category: number of expenses, total spent, share of overall spending and a bar chart. Categories are sorted from highest to lowest spend.

### 4. Generate Monthly Report
Enter a month as `YYYY-MM` (for example `2024-01`), or press Enter for the current month. The report shows the number of transactions, total, average, number of active days, the largest expense and a category breakdown.

### 5. Search Expenses
Every filter is optional. Press Enter to skip it.

- **Keyword**: matches part of the description (not case-sensitive)
- **Category**
- **From / To date**
- **Minimum / Maximum amount**

Filters are combined, so an expense must match all of the ones you filled in.

### 6. Backup / Restore Data
- **Create backup**: copies your data to `data/backups/expenses_backup_<date>_<time>.csv`.
- **Restore**: pick a backup from the list. The backup file is checked first, then a safety copy of your current data is made, and you are asked to confirm before anything is replaced.

### 7. Exit
Closes the program. Your data is already saved after every change.

## 3. Where is my data stored?

| File | Purpose |
|---|---|
| `data/expenses.csv` | Your real expenses (created automatically; not uploaded to GitHub) |
| `data/backups/` | Your backups |
| `data/sample_expenses.csv` | Example data for trying the app |

The CSV has four columns: `date,amount,category,description`. You can open it in Excel, but keep these column names and the date format, or rows will be skipped when loading.

## 4. Trying the app with sample data

**Windows (Command Prompt):**
```
copy data\sample_expenses.csv data\expenses.csv
```

**macOS / Linux:**
```bash
cp data/sample_expenses.csv data/expenses.csv
```

Then run `python main.py`. Delete `data/expenses.csv` whenever you want to start fresh.

## 5. Troubleshooting

| Problem | Fix |
|---|---|
| `python` is not recognised | Use `python3`, or reinstall Python and tick "Add Python to PATH" |
| `ModuleNotFoundError: No module named 'src'` | Run the command from the project's main folder (where `main.py` is) |
| The ₹ sign or emoji look broken | Use a modern terminal such as Windows Terminal or VS Code's terminal |
| "Skipped N invalid row(s)" warning | Some rows in the CSV are malformed. The rest still load. Open the CSV and fix or delete those rows |
| "Nothing to back up yet" | Add at least one expense first |

## 6. Running the tests

```bash
python -m unittest discover -s tests -t . -v
```
