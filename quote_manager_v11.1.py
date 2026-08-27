import csv
import os
import datetime
from getpass import getpass

PIN = "1234"
FILE = "quotes.csv"

def login():
	pin_input = getpass("Enter PIN: ")
	if pin_input!= PIN:
		print("Wrong PIN! Access denied.")
		return False
	print("Access granted!")
	return True
	
def save_quote():
	client = input("Client Name: ").strip()
	item = input("Item/Service: ").strip()
	try:
		amount = float(input("Amount Charged (R): "))
		cost = float(input("Cost (R): "))
	except ValueError:
		print("Amount and Cost must be numbers!")
		return
	profit = amount - cost
	date = datetime.date.today().strftime("%Y-%m-%d")
	
	with open(FILE, "a", newline="") as f:
		writer = csv.writer(f)
		writer.writerow([date, client, item, amount, cost, profit])
	print(f"Quote saved! Profit: R{profit:.2f}")
	
def view_quotes():
	if not os.path.exists(FILE):
		print("No quotes yet.")
		return
	
	total_profit = 0
	monthly_profit = 0
	current_month = datetime.date.today().strftime("%Y-%m")
	
	with open(FILE, "r") as f:
		reader = csv.reader(f)
		quotes = list(reader)
		
	if not quotes:
		print("No quotes yet.")
		return
		
	for i, q in enumerate(quotes, 1):
		try: 
			print(f"{i}. {q[0]} | {q[1]} | {q[2]} | Sold: R{q[3]} | Cost: {q[4]} | Profit: R{q[5]}")
			total_profit += float(q[5])
			if q[0].startswith(current_month):
				monthly_profit += float(q[5])
		except (ValueError, IndexError):
			print(f"{i}. [Corrupted row - skipping]")
			
	print(f"\nTotal Profit All Time: R{total_profit:.2f}")
	print(f"Profit This Month ({current_month}): R{monthly_profit:.2f}")
	
def search_quotes():
	keyword = input("Enter client name to search: ").lower()
	if not os.path.exists(FILE): return
	with open(FILE, "r") as f:
		reader = csv.reader(f)
		found = [q for q in reader if len(q) > 1 and keyword in q[1].lower()]
	if found:
		for q in found: print(q)
	else: print ("No results found.")
	
def monthly_total():
	month = input("Enter month (YYYY-MM): ")
	if not os.path.exists(FILE): return
	total_sales = 0
	total_profit = 0
	with open(FILE, "r") as f:
		reader = csv.reader(f)
		for q in reader:
			try:
				if q[0].startswith(month):
					total_sales += float(q[3])
					total_profit += float(q[5])
			except ValueError:
				continue
	print(f"Month: {month} | Total Sales: R{total_sales:.2f} | Total Profit: R{total_profit:.2f}")
	
def edit_quote():
		if not os.path.exists(FILE): return
		with open(FILE, "r") as f: quotes = list(csv.reader(f))
		for i, q in enumerate(quotes, 1):
			try: print(f"{i}. {q[0]} | {q[1]} | {q[2]}")
			except: print(f"{i}. [Corrupted row]")
		try:
			index = int(input("Enter quote number to delete: ")) - 1
			if 0 <= index < len(quotes):
				quotes[index][2] = input("New Item: ")
				quotes[index][3] = input("New Amount: ")
				quotes[index][4] = input("New Cost: ")
				quotes[index][5] = str(float(quotes[index][3]) - float(quotes[index][4]))
				with open(FILE, "w", newline="") as f: csv.writer(f).writerows(quotes)
				print("Quote updated!")
			else: print("Invalid number.")
		except: print("Invalid input.")
		
def delete_quote():
		if not os.path.exists(FILE): return
		with open(FILE, "r") as f: quotes = list(csv.reader(f))
		for i, q in enumerate(quotes, 1):
			try: print(f"{i}. {q[0]} | {q[1]} | {q[2]}")
			except: print(f"{i}. [Corrupted row]")
		try:
			index = int(input("Enter quote number to delete: ")) - 1
			if 0 <= index < len(quotes):
				del quotes[index]
				with open(FILE, "w", newline="") as f: csv.writer(f).writerows(quotes)
				print("Quote deleted!")
			else: print("Invalid number.")
		except: print("Invalid input.")
		
def backup_data():
		if not os.path.exists(FILE): return
		backup_name = f"quotes_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
		with open(FILE, "r") as f1, open(backup_name, "w", newline="") as f2:
			f2.write(f1.read())
		print(f"Backup created: {backup_name}")
		
def client_report():
	if not os.path.exists(FILE): return
	client_data = {}
	with open(FILE, "r") as f:
		reader = csv.reader(f)
		for q in reader:
			try:
				client = q[1]
				profit = float(q[5])
				client_data[client] = client_data.get(client, 0) + profit
			except (ValueError, IndexError):
				continue
	for client, profit in client_data.items():
		print(f"{client}: R{profit:.2f}")
		
def main():
	if not login(): return
	
	while True:
		print("\n--- QUOTE MANAGER V11.0 ---")
		choice = input("What do you want to do? SAVE, VIEW, SEARCH, TOTAL, EDIT, DELETE, BACKUP, CLIENTS, EXIT: ").upper().replace(" ", "")
		
		if choice == "SAVE": save_quote()
		elif choice == "VIEW": view_quotes()
		elif choice == "SEARCH": search_quotes()
		elif choice == "TOTAL": monthly_total()
		elif choice == "EDIT": edit_quote()
		elif choice == "DELETE": delete_quote()
		elif choice == "BACKUP": backup_data()
		elif choice == "CLIENT" or choice == "CLIENTS": client_report()
		elif choice == "EXIT":
			print("Goodbye!")
			break
		else: print("Invalid choice.")
main()		
