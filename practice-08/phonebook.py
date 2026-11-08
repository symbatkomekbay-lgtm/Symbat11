import json
from pathlib import Path
from psycopg2.extras import Json
from connect import get_connection

BASE = Path(__file__).resolve().parent


def setup():
    with get_connection() as conn:
        with conn.cursor() as cur:
            for filename in ("functions.sql", "procedures.sql"):
                cur.execute((BASE / filename).read_text(encoding="utf-8"))
    print("Database setup completed.")


def display(rows):
    if not rows:
        print("No contacts found.")
    for contact_id, name, surname, phone in rows:
        print(f"{contact_id}: {name} {surname} - {phone}")


def search():
    pattern = input("Search name, surname, or phone: ")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
            display(cur.fetchall())


def upsert():
    name = input("Name: ").strip()
    surname = input("Surname (optional): ").strip()
    phone = input("Phone (10-15 digits, optional +): ").strip()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL upsert_contact(%s::varchar, %s::varchar, %s::varchar)", (name, phone, surname))
    print("Contact saved.")


def bulk_insert():
    print('Enter JSON list, e.g. [{"name":"Aida","phone":"+77001234567"}]')
    entries = json.loads(input("Contacts: "))
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL bulk_insert_contacts(%s::jsonb, %s::jsonb)", (Json(entries), Json([])))
            invalid = cur.fetchone()[0]
    print("Invalid entries:", json.dumps(invalid, ensure_ascii=False, indent=2))
    print("Valid contacts saved.")


def paginate():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM paginated_contacts(%s, %s)", (limit, offset))
            display(cur.fetchall())


def delete():
    name = input("Name (leave blank to delete by phone): ").strip()
    phone = input("Phone (leave blank to delete by name): ").strip()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL delete_contact(%s::varchar, %s::varchar)", (name, phone))
    print("Delete completed.")


def main():
    setup()
    actions = {"1": search, "2": upsert, "3": bulk_insert, "4": paginate, "5": delete}
    while True:
        print("\nPHONEBOOK\n1. Search\n2. Insert / update\n3. Bulk insert\n4. Pagination\n5. Delete\n0. Exit")
        choice = input("Choose: ").strip()
        if choice == "0":
            break
        if choice not in actions:
            print("Invalid option.")
            continue
        try:
            actions[choice]()
        except (Exception) as exc:
            print("Error:", exc)


if __name__ == "__main__":
    main()
