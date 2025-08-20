import json
from datetime import datetime
from collections import defaultdict

DATA_FILE = "finance_data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(transactions):
    with open(DATA_FILE, "w") as f:
        json.dump(transactions, f, indent=4)

def add_transaction(transactions):
    t_type = input("Enter type (income/expense): ").strip().lower()
    if t_type not in ["income", "expense"]:
        print("Invalid type!")
        return
    amount = float(input("Enter amount: "))
    category = input("Enter category (e.g., Food, Rent, Salary): ").strip()
    date_str = input("Enter date (YYYY-MM-DD) [leave blank for today]: ").strip()
    if not date_str:
        date_str = datetime.today().strftime("%Y-%m-%d")
    transaction = {
        "type": t_type,
        "amount": amount,
        "category": category,
        "date": date_str
    }
    transactions.append(transaction)
    print("Transaction added!")

def view_transactions(transactions, filter_type=None):
    data = [t for t in transactions if not filter_type or t["type"] == filter_type]
    if not data:
        print("No transactions found.")
        return
    data.sort(key=lambda x: x["date"])
    print("\nTransactions:")
    for t in data:
        print(f"{t['date']} | {t['type'].upper():7} | ${t['amount']:8.2f} | {t['category']}")
    print()

def filter_expenses_over(transactions, threshold=100):
    filtered = [t for t in transactions if t["type"] == "expense" and t["amount"] > threshold]
    if not filtered:
        print(f"No expenses over ${threshold}")
        return
    print(f"\nExpenses over ${threshold}:")
    for t in filtered:
        print(f"{t['date']} | ${t['amount']:8.2f} | {t['category']}")
    print()

def search_category(transactions, category):
    results = [t for t in transactions if t["category"].lower() == category.lower()]
    if not results:
        print(f"No transactions in category '{category}'")
        return
    print(f"\nTransactions in '{category}':")
    for t in results:
        print(f"{t['date']} | {t['type'].upper():7} | ${t['amount']:8.2f}")
    print()

def monthly_spending_chart(transactions):
    monthly = defaultdict(float)
    for t in transactions:
        if t["type"] == "expense":
            month = t["date"][:7]  # YYYY-MM
            monthly[month] += t["amount"]

    if not monthly:
        print("No expense data for chart.")
        return

    print("\nMonthly Spending Chart:")
    for month, total in sorted(monthly.items()):
        bar = "#" * (int(total) // 10)  # scale: 1 bar = $10
        print(f"{month}: ${total:.2f} {bar}")

def summary(transactions):
    income = sum(t["amount"] for t in transactions if t["type"] == "income")
    expenses = sum(t["amount"] for t in transactions if t["type"] == "expense")
    savings = income - expenses
    print(f"\nSummary:")
    print(f" Total Income : ${income:.2f}")
    print(f" Total Expense: ${expenses:.2f}")
    print(f" Savings      : ${savings:.2f}\n")

def menu():
    transactions = load_data()
    while True:
        print("\n--- Personal Finance Tracker ---")
        print("1. Add Transaction")
        print("2. View All Transactions")
        print("3. View Only Incomes")
        print("4. View Only Expenses")
        print("5. Filter Expenses > $100")
        print("6. Search by Category")
        print("7. Monthly Spending Chart")
        print("8. Show Summary")
        print("9. Save & Exit")

        choice = input("Enter choice: ").strip()
        if choice == "1":
            add_transaction(transactions)
        elif choice == "2":
            view_transactions(transactions)
        elif choice == "3":
            view_transactions(transactions, "income")
        elif choice == "4":
            view_transactions(transactions, "expense")
        elif choice == "5":
            filter_expenses_over(transactions, 100)
        elif choice == "6":
            cat = input("Enter category: ")
            search_category(transactions, cat)
        elif choice == "7":
            monthly_spending_chart(transactions)
        elif choice == "8":
            summary(transactions)
        elif choice == "9":
            save_data(transactions)
            print("Data saved. Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    menu()
