import csv
import os
from datetime import datetime
from collections import defaultdict

CSV_FILE = "expenses.csv"

def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Category", "Description", "Amount"])

def add_expense():
    print("\n--- Add New Expense ---")
    date_str = input("Enter date (YYYY-MM-DD) or Enter for today: ").strip()
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")
    category = input("Enter category (Food/Transport/Shopping/Bills/Other): ").strip().capitalize()
    if not category:
        category = "Other"
    desc = input("Enter description: ").strip()
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount!")
        return
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([date_str, category, desc, amount])
    print(f"Expense added: {category} - {amount}")

def view_expenses():
    print("\n--- All Expenses ---")
    if not os.path.exists(CSV_FILE):
        print("No expenses found!")
        return
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if not rows:
            print("No expenses yet!")
            return
        print(f"{'Date':<12} {'Category':<12} {'Description':<20} {'Amount'}")
        print("-"*60)
        total = 0
        for row in rows:
            print(f"{row['Date']:<12} {row['Category']:<12} {row['Description']:<20} {row['Amount']}")
            total += float(row['Amount'])
        print("-"*60)
        print(f"Total Spent: {total}")

def filter_expenses():
    print("\n--- Filter Expenses ---")
    cat = input("Enter category to filter: ").strip().capitalize()
    if not cat:
        print("Enter a category!")
        return
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        found = [r for r in reader if r['Category'].lower() == cat.lower()]
        if not found:
            print(f"No expenses for: {cat}")
            return
        total = 0
        for row in found:
            print(f"  {row['Date']} - {row['Description']} - Rs.{row['Amount']}")
            total += float(row['Amount'])
        print(f"Total for {cat}: Rs.{total}")

def category_summary():
    print("\n--- Category Summary ---")
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        summary = defaultdict(float)
        count = defaultdict(int)
        for row in reader:
            try:
                summary[row['Category']] += float(row['Amount'])
                count[row['Category']] += 1
            except:
                continue
        if not summary:
            print("No data!")
            return
        print(f"{'Category':<15} {'Count':<8} {'Total'}")
        print("-"*40)
        for cat, amt in summary.items():
            print(f"{cat:<15} {count[cat]:<8} Rs.{amt:.2f}")
        print("-"*40)
        print(f"Grand Total: Rs.{sum(summary.values()):.2f}")

def main():
    init_csv()
    while True:
        print("\n==============================")
        print(" PERSONAL EXPENSE TRACKER")
        print("==============================")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Filter by Category")
        print("4. Category Summary")
        print("5. Exit")
        ch = input("Choose (1-5): ")
        if ch == '1':
            add_expense()
        elif ch == '2':
            view_expenses()
        elif ch == '3':
            filter_expenses()
        elif ch == '4':
            category_summary()
        elif ch == '5':
            print("Bye! Data saved in expenses.csv")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()