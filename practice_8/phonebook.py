import psycopg2
from connect import get_connection
import csv

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    create_sql = """
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL
    )
    """
    cur.execute(create_sql)
    conn.commit()
    cur.close()
    conn.close()

def import_from_csv(filename='contacts.csv'):
    conn = get_connection()
    cur = conn.cursor()
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            if len(row) < 2:
                continue
            name, phone = row[0].strip(), row[1].strip()
            cur.execute(
                "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                (name, phone)
            )
    conn.commit()
    cur.close()
    conn.close()
    print("Contacts imported from CSV successfully.")

def add_contact():
    name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Contact added successfully.")

def update_contact():
    conn = get_connection()
    cur = conn.cursor()
    choice = input("Update name or phone? (enter 'name' or 'phone'): ").strip().lower()
    if choice == 'name':
        old_name = input("Enter existing name: ").strip()
        new_name = input("Enter new name: ").strip()
        cur.execute(
            "UPDATE contacts SET name = %s WHERE name = %s",
            (new_name, old_name)
        )
    elif choice == 'phone':
        name = input("Enter name of the contact: ").strip()
        new_phone = input("Enter new phone: ").strip()
        cur.execute(
            "UPDATE contacts SET phone = %s WHERE name = %s",
            (new_phone, name)
        )
    else:
        print("Invalid choice for update.")
        cur.close()
        conn.close()
        return
    conn.commit()
    updated = cur.rowcount
    cur.close()
    conn.close()
    if updated:
        print(f"{updated} contact(s) updated successfully.")
    else:
        print("No contacts were updated (contact may not exist).")

def query_contacts():
    conn = get_connection()
    cur = conn.cursor()
    choice = input("Query by name or phone prefix? (enter 'name' or 'phone'): ").strip().lower()
    if choice == 'name':
        name = input("Enter name to search for: ").strip()
        cur.execute(
            "SELECT id, name, phone FROM contacts WHERE name = %s",
            (name,)
        )
    elif choice == 'phone':
        prefix = input("Enter phone prefix to search for: ").strip()
        cur.execute(
            "SELECT id, name, phone FROM contacts WHERE phone LIKE %s",
            (prefix + '%',)
        )
    else:
        print("Invalid choice for query.")
        cur.close()
        conn.close()
        return
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if rows:
        print("Search results:")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    else:
        print("No matching contacts found.")

def search_pattern(pattern):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, phone FROM search_contacts(%s::text)", (pattern,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    print("Search results:")
    for row in rows:
        print(f"Name: {row[0]}, Phone: {row[1]}")

def upsert(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Upserted contact: {name} -> {phone}")

def bulk_upsert(names, phones):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT bulk_upsert_users(%s, %s)", (names, phones))
    invalid = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    print("Invalid entries:", invalid)

def delete_contact(name=None, phone=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.callproc("delete_contact", (name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted (if existed).")



def show_all_contacts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def main():
    create_table()
    while True:
        print("\nPhoneBook Menu:")
        print("1. Import contacts from CSV")
        print("2. Add a new contact")
        print("3. Update a contact")
        print("4. Query contacts (old)")
        print("5. Delete contact (procedure)")
        print("6. Show all contacts")
        print("7. Search by pattern (FUNCTION)")
        print("8. Upsert contact (PROCEDURE)")
        print("9. Bulk upsert (FUNCTION)")
        print("10. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            import_from_csv()
        elif choice == '2':
            add_contact()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            query_contacts()
        elif choice == '5':
            name = input("Enter name (or leave empty): ").strip() or None
            phone = input("Enter phone (or leave empty): ").strip() or None
            delete_contact(name, phone)
        elif choice == '6':
            show_all_contacts()
        elif choice == '7':
            pattern = input("Enter pattern: ").strip()
            search_pattern(pattern)
        elif choice == '8':
            name = input("Enter name: ").strip()
            phone = input("Enter phone: ").strip()
            upsert(name, phone)
        elif choice == '9':
            names = input("Enter names (comma separated): ").split(',')
            phones = input("Enter phones (comma separated): ").split(',')
            names = [n.strip() for n in names]
            phones = [p.strip() for p in phones]
            bulk_upsert(names, phones)
        elif choice == '10':
            print("Exiting PhoneBook.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__': 
    main()