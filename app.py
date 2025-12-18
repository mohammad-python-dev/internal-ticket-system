import sqlite3
from datetime import datetime
import csv

DB_NAME = "tickets.db"

def connect_db():
    return sqlite3.connect(DB_NAME)

def setup_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        department TEXT,
        priority TEXT,
        status TEXT,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

def create_ticket():
    title = input("Title: ")
    description = input("Description: ")
    department = input("Department (IT / HR / Finance): ")
    priority = input("Priority (Low / Medium / High): ")
    status = "Open"
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO tickets (title, description, department, priority, status, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (title, description, department, priority, status, created_at))
    conn.commit()
    conn.close()
    print("Ticket created successfully.")

def list_tickets():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()
    conn.close()

    for t in tickets:
        print(t)

def update_status():
    ticket_id = input("Ticket ID: ")
    new_status = input("New Status (Open / In Progress / Closed): ")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tickets SET status=? WHERE id=?", (new_status, ticket_id))
    conn.commit()
    conn.close()
    print("Status updated.")

def export_csv():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()
    conn.close()

    with open("tickets_export.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Title", "Description", "Department", "Priority", "Status", "Created At"])
        writer.writerows(tickets)

    print("Tickets exported to tickets_export.csv")

def menu():
    setup_db()
    while True:
        print("\n--- Internal Ticket System ---")
        print("1. Create Ticket")
        print("2. List Tickets")
        print("3. Update Ticket Status")
        print("4. Export CSV")
        print("5. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            create_ticket()
        elif choice == "2":
            list_tickets()
        elif choice == "3":
            update_status()
        elif choice == "4":
            export_csv()
        elif choice == "5":
            break
        else:
            print("Invalid choice")

menu()
