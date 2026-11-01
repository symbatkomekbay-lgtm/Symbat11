
import csv
import psycopg2
from connect import connect

def create_table():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(100) NOT NULL,
                    phone VARCHAR(20) UNIQUE NOT NULL
                )
            """)


def add_contact():
    name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()

    if not name or not phone:
        print("Name and phone cannot be empty!")
        return

    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO contacts (first_name, phone)
                    VALUES (%s, %s)
                    """,
                    (name, phone)
                )
        print("Contact added successfully!")
    except psycopg2.IntegrityError:
        print("This phone number already exists!")


def import_csv():
    try:
        with open("contacts.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            with connect() as conn:
                with conn.cursor() as cur:
                    for row in reader:
                        cur.execute(
                            """
                            INSERT INTO contacts (first_name, phone)
                            VALUES (%s, %s)
                            ON CONFLICT (phone) DO NOTHING
                            """,
                            (row["first_name"], row["phone"])
                        )

        print("CSV imported successfully!")

    except FileNotFoundError:
        print("contacts.csv file not found!")
    except (KeyError, psycopg2.Error, ValueError) as e:
        print("CSV import failed:", e)


def show_contacts():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM contacts ORDER BY id"
            )
            contacts = cur.fetchall()

            if not contacts:
                print("PhoneBook is empty!")
            else:
                print("\n--- CONTACTS ---")
                for contact in contacts:
                    print(
                        f"ID: {contact[0]} | "
                        f"Name: {contact[1]} | "
                        f"Phone: {contact[2]}"
                    )


def search_contact():
    print("\n1. Search by name")
    print("2. Search by phone prefix")

    choice = input("Choose: ")

    with connect() as conn:
        with conn.cursor() as cur:

            if choice == "1":
                name = input("Enter name: ")
                cur.execute(
                    """
                    SELECT * FROM contacts
                    WHERE first_name ILIKE %s
                    """,
                    ("%" + name + "%",)
                )

            elif choice == "2":
                prefix = input("Enter phone prefix: ")
                cur.execute(
                    """
                    SELECT * FROM contacts
                    WHERE phone LIKE %s
                    """,
                    (prefix + "%",)
                )

            else:
                print("Invalid choice!")
                return

            contacts = cur.fetchall()

            if contacts:
                for contact in contacts:
                    print(contact)
            else:
                print("No contacts found!")


def update_contact():
    print("\n1. Update name")
    print("2. Update phone")

    choice = input("Choose: ")
    old_phone = input("Enter current phone: ")

    if choice == "1":
        new_value = input("Enter new name: ")
        query = """
            UPDATE contacts
            SET first_name = %s
            WHERE phone = %s
        """

    elif choice == "2":
        new_value = input("Enter new phone: ")
        query = """
            UPDATE contacts
            SET phone = %s
            WHERE phone = %s
        """

    else:
        print("Invalid choice!")
        return

    if not new_value.strip():
        print("New value cannot be empty!")
        return

    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (new_value, old_phone))
                updated = cur.rowcount

        if updated:
            print("Contact updated successfully!")
        else:
            print("Contact not found!")

    except psycopg2.IntegrityError:
        print("Phone number already exists!")


def delete_contact():
    print("\n1. Delete by name")
    print("2. Delete by phone")

    choice = input("Choose: ")

    if choice == "1":
        name = input("Enter name: ")
        query = """
            DELETE FROM contacts
            WHERE first_name = %s
        """
        value = name

    elif choice == "2":
        phone = input("Enter phone: ")
        query = """
            DELETE FROM contacts
            WHERE phone = %s
        """
        value = phone

    else:
        print("Invalid choice!")
        return

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (value,))
            deleted = cur.rowcount

    if deleted:
        print(f"{deleted} contact(s) deleted!")
    else:
        print("Contact not found!")

def main():
    create_table()

    while True:
        print("\n========== PHONEBOOK ==========")
        print("1. Add contact")
        print("2. Import contacts from CSV")
        print("3. Show all contacts")
        print("4. Search contacts")
        print("5. Update contact")
        print("6. Delete contact")
        print("0. Exit")
        print("===============================")

        choice = input("Choose an option: ")

        try:
            if choice == "1":
                add_contact()

            elif choice == "2":
                import_csv()

            elif choice == "3":
                show_contacts()

            elif choice == "4":
                search_contact()

            elif choice == "5":
                update_contact()

            elif choice == "6":
                delete_contact()

            elif choice == "0":
                print("Goodbye!")
                break

            else:
                print("Invalid option!")

        except psycopg2.Error as e:
            print("Database error:", e)


if __name__ == "__main__":
    main()
