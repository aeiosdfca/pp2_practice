from connect import get_connection
import json

conn = get_connection()
cur = conn.cursor()

def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")

    cur.execute("""
        INSERT INTO phonebook(name, email, birthday)
        VALUES (%s,%s,%s)
        RETURNING id
    """, (name, email, birthday))

    cid = cur.fetchone()[0]

    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")

    cur.execute("INSERT INTO phones(contact_id, phone, type) VALUES (%s,%s,%s)",
                (cid, phone, ptype))

    conn.commit()


def search():
    q = input("Search: ")
    cur.execute("SELECT * FROM search_contacts(%s)", (q,))
    print(cur.fetchall())


def paginate():
    limit = 2
    offset = 0

    while True:
        cur.execute("SELECT * FROM get_contacts_page(%s,%s)", (limit, offset))
        rows = cur.fetchall()

        print("\nPAGE:")
        for r in rows:
            print(r)

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            offset += limit
        elif cmd == "prev" and offset > 0:
            offset -= limit
        elif cmd == "quit":
            break


def export_json():
    cur.execute("""
        SELECT p.name, p.email, p.birthday, g.name
        FROM phonebook p
        LEFT JOIN groups g ON p.group_id = g.id
    """)

    data = []
    for r in cur.fetchall():
        data.append({
            "name": r[0],
            "email": r[1],
            "birthday": str(r[2]),
            "group": r[3]
        })

    with open("contacts.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Exported!")


def import_json():
    with open("contacts.json") as f:
        data = json.load(f)

    for item in data:
        cur.execute("""
            INSERT INTO phonebook(name,email,birthday)
            VALUES (%s,%s,%s)
        """, (item["name"], item["email"], item["birthday"]))

    conn.commit()


while True:
    print("\n1 Add\n2 Search\n3 Pages\n4 Export\n5 Import\n6 Exit")
    c = input()

    if c == "1":
        add_contact()
    elif c == "2":
        search()
    elif c == "3":
        paginate()
    elif c == "4":
        export_json()
    elif c == "5":
        import_json()
    elif c == "6":
        break

conn.close()
