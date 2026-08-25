import json
import os
from datetime import datetime

transactions = []


menu = {
    1: "Add Income",
    2: "Add Expense",
    3: "View Transactions",
    4: "Search Transactions",
    5: "Financial Report",
    6: "Edit Transaction",
    7: "Delete Transaction",
    8: "Clear Transactions",
    9: "Monthly Report", 
    0: "Exit"
}


def show_menu():
    print("\n===== PERSONAL FINANCE TRACKER =====")

    for key, value in menu.items():
        print(f"{key}. {value}")


def get_amount(message):
    while True:
        try:
            amount = float(input(message))

            if amount > 0:
                return amount
            else:
                print("Amount must be greater than 0.")

        except ValueError:
            print("Please enter a valid number.")


def get_number(message):
    while True:
        try:
            number = int(input(message))
            return number

        except ValueError:
            print("Please enter a valid number.")

def generate_transaction_id():
    if not transactions:
        return 1

    return max(transaction["id"] for transaction in transactions) + 1
    
def get_transaction_datetime():
    while True:
        date_input = input("Enter transaction date (YYYY-MM-DD) or press Enter for today: ")

        if date_input == "":
            date = datetime.now().strftime("%Y-%m-%d")
            break

        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            date = date_input
            break

        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD (Example: 2026-08-05)")


    while True:
        time_input = input("Enter transaction time (HH:MM) or press Enter for current time: ")

        if time_input == "":
            time = datetime.now().strftime("%H:%M")
            break

        try:
            datetime.strptime(time_input, "%H:%M")
            time = time_input
            break

        except ValueError:
            print("Invalid time format. Use HH:MM (Example: 11:45)")

    return date, time

def add_income():
    category = input("Enter income category: ")
    amount = get_amount("Enter income amount: ")
    date, time = get_transaction_datetime()

    transaction = {
        "id": generate_transaction_id(),
        "type": "Income",
        "category": category,
        "amount": amount,
        "date": date,
        "time": time
    }

    transactions.append(transaction)
    save_data()

    print("Income added successfully!")
        
def add_expense():
    category = input("Enter expense category: ")
    amount = get_amount("Enter expense amount: ")
    date, time = get_transaction_datetime()

    transaction = {
        "id": generate_transaction_id(),
        "type": "Expense",
        "category": category,
        "amount": amount,
        "date": date,
        "time": time
    }

    transactions.append(transaction)
    save_data()

    print("Expense added successfully!")

def view_transactions():
    print("\n===== VIEW TRANSACTIONS =====")
    print("1. View All Transactions")
    print("2. View By Month")
    print("0. Back")

    choice = input("Enter your choice: ")
    
    if choice == "1":
        if not transactions:
            print("No transactions available.")
            return

        print("\n===== ALL TRANSACTIONS =====")

        for transaction in transactions:
            print("--------------------")
            print("ID:", transaction["id"])
            print("Type:", transaction["type"])
            print("Category:", transaction["category"])
            print(f"Amount: ₦{transaction['amount']:,.2f}")
            print("Date:", transaction["date"])
            print("Time:", transaction["time"])
        
    elif choice == "2":
        month = input("Enter month (Example: August_2026): ")

        monthly_transactions = get_transactions_by_month(month)
        
        if not monthly_transactions:
            print("No transactions found for this month.")
            return
            
        print(f"\n===== {month} TRANSACTIONS =====")

        for transaction in monthly_transactions:
            print("--------------------")
            print("ID:", transaction["id"])
            print("Type:", transaction["type"])
            print("Category:", transaction["category"])
            print(f"Amount: ₦{transaction['amount']:,.2f}")
            print("Date:", transaction["date"])
            print("Time:", transaction["time"])
            
    elif choice == "0":
        return

    else:
        print("Invalid choice!")
        
def financial_report():
    if not transactions:
        print("No transactions available.")
        return
        
    total_income = 0
    total_expense = 0
    income_count = 0
    expense_count = 0
    
    for transaction in transactions:
        if transaction["type"] == "Income":
            total_income += transaction["amount"]
            income_count += 1
        else:
            total_expense += transaction["amount"]
            expense_count += 1
          
    balance = total_income - total_expense
    
    print("\n===== FINANCIAL REPORT =====")
    print(f"Total Income: ₦{total_income:,.2f}")
    print(f"Total Expenses: ₦{total_expense:,.2f}")
    print(f"Remaining Balance: ₦{balance:,.2f}")
    print("\nIncome Transactions:", income_count)
    print("Expense Transactions:", expense_count)
        
def delete_transaction():
    if not transactions:
        print("No transactions available.")
        return

    transaction_id = get_number("Enter transaction ID to delete: ")

    for transaction in transactions:
        if transaction["id"] == transaction_id:

            month = datetime.strptime(
                transaction["date"],
                "%Y-%m-%d"
            ).strftime("%B_%Y")

            transactions.remove(transaction)

            save_data()

            monthly_transactions = get_transactions_by_month(month)

            filename = get_month_file(month)

            with open(filename, "w") as file:
                json.dump(monthly_transactions, file, indent=4)

            print("Transaction deleted successfully!")
            return

    print("Invalid transaction ID.")

def create_folder():
    if not os.path.exists("finance_data"):
        os.mkdir("finance_data")
        
def get_month_file(month_name):
    return f"finance_data/{month_name}.json"
    
def get_transactions_by_month(month_name):
    monthly_transactions = []

    for transaction in transactions:
        month = datetime.strptime(
            transaction["date"],
            "%Y-%m-%d"
        ).strftime("%B_%Y")

        if month == month_name:
            monthly_transactions.append(transaction)

    return monthly_transactions
    
def clear_transactions():
    print("\n===== CLEAR TRANSACTIONS =====")
    print("1. Clear Specific Month")
    print("2. Clear All Transactions")
    print("0. Cancel")

    choice = input("Enter your choice: ")

    if choice == "1":
        month_name = input(
    "Enter month name (Example: August 2026): "
)

        month_name = month_name.replace(" ", "_")

        filename = get_month_file(month_name)

        if os.path.exists(filename):

            confirm = input(
                f"Are you sure you want to clear {month_name}? (YES/yes/Y/y): "
            ).lower()

            if confirm in ["yes", "y"]:
                with open(filename, "w") as file:
                    json.dump([], file, indent=4)
                    
                if month_name == get_current_month():
                    transactions.clear()

                print(f"{month_name} transactions cleared successfully!")

            else:
                print("Cancelled.")

        else:
            print("Month record not found.")

    elif choice == "2":
        confirm = input(
            "Are you sure you want to clear ALL transactions? (YES/yes/Y/y): "
        ).lower()

        if confirm in ["yes", "y"]:
            transactions.clear()

            folder = "finance_data"

            if os.path.exists(folder):
                for file_name in os.listdir(folder):
                    file_path = os.path.join(folder, file_name)

                    if file_name.endswith(".json"):
                        os.remove(file_path)

            print("All transactions cleared successfully!")

        else:
            print("Cancelled.")

    elif choice == "0":
        print("Cancelled.")

    else:
        print("Invalid choice.")
        
def search_transactions():
    print("\n===== SEARCH TRANSACTIONS =====")
    print("1. Search by ID")
    print("2. Search by Category")
    print("3. Search by Type")
    print("4. Search by Date")
    print("0. Back")

    choice = input("Enter your choice: ")

    if choice == "1":
        search_id = get_number("Enter transaction ID: ")

        found = False

        for transaction in transactions:
            if transaction["id"] == search_id:
                print(transaction)
                found = True
                break

        if not found:
            print("Transaction not found.")

    elif choice == "2":
        category = input("Enter category to search: ").lower()

        found = False

        for transaction in transactions:
            if transaction["category"].lower() == category:
                print(transaction)
                found = True

        if not found:
            print("No transaction found.")

    elif choice == "3":
        transaction_type = input(
            "Enter type (Income/Expense): "
        ).lower()

        found = False

        print("\n===== SEARCH RESULTS =====")

        for transaction in transactions:
            if transaction["type"].lower() == transaction_type:

                print("--------------------")
                print("ID:", transaction["id"])
                print("Type:", transaction["type"])
                print("Category:", transaction["category"])
                print(f"Amount: ₦{transaction['amount']:,.2f}")
                print("Date:", transaction["date"])
                print("Time:", transaction["time"])

                found = True

        if not found:
            print("No transaction found with that type.")

    elif choice == "4":
        date = input("Enter date (YYYY-MM-DD): ")

        found = False

        print("\n===== SEARCH RESULTS =====")

        for transaction in transactions:
            if transaction["date"] == date:

                print("--------------------")
                print("ID:", transaction["id"])
                print("Type:", transaction["type"])
                print("Category:", transaction["category"])
                print(f"Amount: ₦{transaction['amount']:,.2f}")
                print("Date:", transaction["date"])
                print("Time:", transaction["time"])

                found = True

        if not found:
            print("No transaction found on that date.")

    elif choice == "0":
        print("Returning to menu.")

    else:
        print("Invalid choice.")

def get_date(message):
    while True:
        date = input(message)

        try:
            datetime.strptime(date, "%Y-%m-%d")
            return date

        except ValueError:
            print(
                "Invalid date format. "
                "Use YYYY-MM-DD (Example: 2026-08-21)"
            )
            
def get_time(message):
    while True:
        time = input(message)

        try:
            datetime.strptime(time, "%H:%M")
            return time

        except ValueError:
            print(
                "Invalid time format. "
                "Use HH:MM (Example: 14:30)"
            )
                
def edit_transaction():
    if not transactions:
        print("No transactions available.")
        return

    transaction_id = get_number("Enter transaction ID to edit: ")

    for transaction in transactions:
        if transaction["id"] == transaction_id:
            
            old_month = datetime.strptime(
    transaction["date"],
    "%Y-%m-%d"
).strftime("%B_%Y")

            print("\n===== TRANSACTION FOUND =====")
            print("ID:", transaction["id"])
            print("Type:", transaction["type"])
            print("Category:", transaction["category"])
            print(f"Amount: ₦{transaction['amount']:,.2f}")
            print("Date:", transaction["date"])
            print("Time:", transaction["time"])

            print("\n===== EDIT TRANSACTION =====")
            print("1. Category")
            print("2. Amount")
            print("3. Date")
            print("4. Time")
            print("0. Cancel")

            choice = input("What do you want to edit? ")
            
            if choice == "1":
                new_category = input("Enter new category: ")

                transaction["category"] = new_category

                save_data()

                print("Category updated successfully!")
                
            elif choice == "2":
                new_amount = get_amount("Enter new amount: ")

                transaction["amount"] = new_amount

                save_data()

                print("Amount updated successfully!")
                
            elif choice == "3":
                new_date = get_date("Enter new date (YYYY-MM-DD): ")

                new_month = datetime.strptime(
        new_date,
        "%Y-%m-%d"
    ).strftime("%B_%Y")

                transaction["date"] = new_date

                save_data()

                print("Date updated successfully!")
                
            elif choice == "4":
                new_time = get_time("Enter new time (HH:MM): ")

                transaction["time"] = new_time

                save_data()

                print("Time updated successfully!")
                
            elif choice == "0":
                print("Edit cancelled.")
                return

            return

    print("Invalid transaction ID.")

def save_data(message=False):
    create_folder()

    months = set()

    for transaction in transactions:
        month = datetime.strptime(
            transaction["date"],
            "%Y-%m-%d"
        ).strftime("%B_%Y")

        months.add(month)

    for month in months:
        filename = get_month_file(month)

        monthly_transactions = get_transactions_by_month(month)

        with open(filename, "w") as file:
            json.dump(monthly_transactions, file, indent=4)

    if message:
        print("Data saved successfully!")

def get_current_month():
    return datetime.now().strftime("%B_%Y")
    
def load_data():
    global transactions

    create_folder()
    
    transactions = []

    for filename in os.listdir("finance_data"):
        if filename.endswith(".json"):

            filepath = os.path.join("finance_data", filename)

            try:
                with open(filepath, "r") as file:
                    monthly_transactions = json.load(file)

                transactions.extend(monthly_transactions)

            except (json.JSONDecodeError, FileNotFoundError):
                continue
                
def monthly_report():
    print("\n===== MONTHLY REPORT =====")
    
    month = input("Enter month (Example: August_2026): ")
    
    monthly_transactions = get_transactions_by_month(month)
    
    if not monthly_transactions:
        print("No transactions found for this month.")
        return
        
    total_income = 0
    total_expense = 0
    income_count = 0 
    expense_count = 0
    
    for transaction in monthly_transactions:
        if transaction["type"] == "Income":
            total_income += transaction["amount"]
            income_count += 1
        else:
            total_expense += transaction["amount"]
            expense_count += 1
            
    balance = total_income - total_expense
    
    print("\n===== MONTHLY REPORT =====")
    print("Month:", month)
    print(f"Total Income: ₦{total_income:,.2f}")
    print(f"Total Expenses: ₦{total_expense:,.2f}")
    print(f"Balance: ₦{balance:,.2f}")
    print("\nIncome Transactions:", income_count)
    print("Expense Transactions:", expense_count)

load_data()

while True:
    show_menu()

    choice = input("Enter your choice (0-9): ")

    if choice == "1":
        add_income()

    elif choice == "2":
        add_expense()

    elif choice == "3":
        view_transactions()

    elif choice == "4":
        search_transactions()

    elif choice == "5":
        financial_report()
        
    elif choice == "6":
        edit_transaction()
        
    elif choice == "7":
        delete_transaction()
        
    elif choice == "8":
        clear_transactions()
        
    elif choice == "9":
        monthly_report()

    elif choice == "0":
        save_data(message=True)
        print("Exiting Personal Finance Tracker...")
        break

    else:
        print("Invalid choice!")
