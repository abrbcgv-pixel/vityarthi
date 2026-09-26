"""Expense Tracker: a command-line app to record and review spending.

Features: add, view, edit and delete expenses, categorize them,
and see monthly totals. Data is saved in expenses.json.
"""

import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"
CATEGORIES = ["Food", "Transport", "Shopping", "Bills","Entertainment", "Health", "Other"]


# ---------- File handling ----------

def load_expenses():
    """Read expenses from the JSON file (empty list if none yet)."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Warning: could not read the data file. Starting fresh.")
        return []

def save_expenses(expenses):
    """Write all expenses to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=2)


# ---------- Input helpers ----------

def ask_amount(current=None):
    """Ask for a positive amount. Blank keeps `current` when editing."""
    while True:
        text = input("Amount" + (f" [{current}]" if current else "") + ": ").strip()
        if not text and current is not None:
            return current
        try:
            value = float(text)
            if value <= 0:
                print("Amount must be greater than 0.")
                continue
            return round(value, 2)
        except ValueError:
            print("Please enter a valid number.")


def ask_date(current=None):
    """Ask for a date as YYYY-MM-DD. Blank uses today's date (or `current`)."""
    default = current or datetime.today().strftime("%Y-%m-%d")
    while True:
        text = input(f"Date (YYYY-MM-DD) [{default}]: ").strip() or default
        try:
            datetime.strptime(text, "%Y-%m-%d")
            return text
        except ValueError:
            print("Invalid date. Use the format YYYY-MM-DD.")


def ask_category(current=None):
    """Show the category list and let the user pick one by number."""
    for number, name in enumerate(CATEGORIES, start=1):
        print(f"  {number}. {name}")
    while True:
        text = input("Category number" + (f" [{current}]" if current else "") + ": ").strip()
        if not text and current is not None:
            return current
        if text.isdigit() and 1 <= int(text) <= len(CATEGORIES):
            return CATEGORIES[int(text) - 1]
        print("Choose a number from the list.")


def ask_id(expenses):
    """Ask for an expense ID and return the matching expense (or None)."""
    text = input("Enter expense ID: ").strip()
    if not text.isdigit():
        print("ID must be a number.")
        return None
    for expense in expenses:
        if expense["id"] == int(text):
            return expense
    print("No expense found with that ID.")
    return None


# ---------- Features ----------

def add_expense(expenses):
    new_id = max((e["id"] for e in expenses), default=0) + 1
    expense = {
        "id": new_id,
        "date": ask_date(),
        "amount": ask_amount(),
        "category": ask_category(),
        "description": input("Description: ").strip() or "-",
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Expense #{new_id} added.")


def view_expenses(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return
    print(f"\n{'ID':<4} {'Date':<11} {'Amount':>10}  {'Category':<14} Description")
    print("-" * 60)
    for e in sorted(expenses, key=lambda x: x["date"]):
        print(f"{e['id']:<4} {e['date']:<11} {e['amount']:>10.2f}  "
              f"{e['category']:<14} {e['description']}")


def edit_expense(expenses):
    view_expenses(expenses)
    if not expenses:
        return
    expense = ask_id(expenses)
    if expense is None:
        return
    print("Press Enter to keep the current value.")
    expense["date"] = ask_date(expense["date"])
    expense["amount"] = ask_amount(expense["amount"])
    expense["category"] = ask_category(expense["category"])
    new_desc = input(f"Description [{expense['description']}]: ").strip()
    if new_desc:
        expense["description"] = new_desc
    save_expenses(expenses)
    print("Expense updated.")


def delete_expense(expenses):
    view_expenses(expenses)
    if not expenses:
        return
    expense = ask_id(expenses)
    if expense is None:
        return
    if input("Delete this expense? (y/n): ").strip().lower() == "y":
        expenses.remove(expense)
        save_expenses(expenses)
        print("Expense deleted.")
    else:
        print("Cancelled.")


def monthly_summary(expenses):
    """Show the total for one month, broken down by category."""
    month = input("Month (YYYY-MM), or Enter for all months: ").strip()

    if not month:
        totals = {}
        for e in expenses:
            key = e["date"][:7]
            totals[key] = totals.get(key, 0) + e["amount"]
        if not totals:
            print("No expenses recorded yet.")
            return
        print("\nMonthly totals")
        for key in sorted(totals):
            print(f"  {key}: {totals[key]:.2f}")
        return

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month. Use the format YYYY-MM.")
        return

    selected = [e for e in expenses if e["date"].startswith(month)]
    if not selected:
        print(f"No expenses found for {month}.")
        return

    by_category = {}
    for e in selected:
        by_category[e["category"]] = by_category.get(e["category"], 0) + e["amount"]

    print(f"\nSummary for {month}")
    for category, amount in sorted(by_category.items(), key=lambda x: -x[1]):
        print(f"  {category:<14} {amount:>10.2f}")
    print("  " + "-" * 25)
    print(f"  {'TOTAL':<14} {sum(by_category.values()):>10.2f}")


# ---------- Main menu ----------

def main():
    expenses = load_expenses()
    actions = {
        "1": add_expense,
        "2": view_expenses,
        "3": edit_expense,
        "4": delete_expense,
        "5": monthly_summary,
    }
    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Edit an expense")
        print("4. Delete an expense")
        print("5. Monthly totals")
        print("6. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "6":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action(expenses)
        else:
            print("Invalid choice. Please enter 1-6.")


if __name__ == "__main__":
    main()
