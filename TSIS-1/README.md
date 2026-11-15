# TSIS 1 — PhoneBook Extended Contact Management

Python + PostgreSQL console project extending Practice 7 and Practice 8.

## Setup (macOS / VS Code)

1. Open this folder in VS Code (**File → Open Folder → TSIS1**).
2. Ensure PostgreSQL is installed and running, and your existing Practice 7/8 `contacts` table is in the selected database.
3. In VS Code Terminal:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4. Configure database credentials **in the terminal** (do not commit passwords):

```bash
export PGHOST=localhost
export PGPORT=5432
export PGUSER=postgres
export PGDATABASE=postgres
export PGPASSWORD='YOUR_POSTGRES_PASSWORD'
```

If your Practice 7/8 database has a different name, use that name for `PGDATABASE`.

5. Run:

```bash
python3 phonebook.py
```

Startup applies `schema.sql` and `procedures.sql` automatically, including migrating existing `contacts.phone` values into `phones`. Existing rows are preserved. Back up your database before schema migrations.

## Features

- Contacts with multiple typed phones, email, birthday, group and created timestamp
- Filter by group, partial email search, sort by name/birthday/date added
- Extended `search_contacts(text)` function searches name/surname/email/all phones
- Paginated `next` / `prev` / `quit` console navigation
- JSON export and import with duplicate-name skip/overwrite prompt
- CSV import supports `name,surname,phone,phone_type,email,birthday,group`
- SQL procedures `add_phone` and `move_to_group`

## Sample test

Choose **7** to import the sample `contacts.csv`, **2** to list, **3** to search `gmail`, **4** to paginate, **5** to export, and **8/9** to test stored procedures.

## Note about Practice 8

This package is a standalone extension because the exact previous repository source files could not be accessed during generation. It retains the legacy `contacts(name,surname,phone)` columns, and uses `CREATE TABLE IF NOT EXISTS` / `ALTER TABLE ... IF NOT EXISTS` for safe schema extension. Practice 8's existing pagination function remains untouched; console pagination uses SQL `LIMIT/OFFSET` for compatibility. If the instructor specifically requires calling the existing `paginated_contacts` function, adapt that one menu action to the function's actual signature.

## GitHub

From the parent `Symbat11` repository folder:

```bash
git add TSIS1
git commit -m "Add TSIS1 extended contact model and console tools"
git push origin main
```

Check your actual branch with `git branch --show-current` and replace `main` if needed.
