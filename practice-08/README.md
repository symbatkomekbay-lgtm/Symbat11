# Practice 8 — PostgreSQL PhoneBook

This project demonstrates PostgreSQL functions and stored procedures called from Python with psycopg2.

## Setup

1. Create a PostgreSQL database named `phonebook` (or set `PGDATABASE`).
2. Set connection environment variables as needed: `PGUSER`, `PGPASSWORD`, `PGHOST`, `PGPORT`.
3. Install dependency: `python3 -m pip install -r requirements.txt`
4. Run: `python3 phonebook.py`. SQL files are applied automatically.

## Features

- Search by name, surname, or phone (case-insensitive pattern).
- Insert/update a contact by name.
- Bulk insert JSON contacts, returning invalid entries.
- Pagination with LIMIT/OFFSET.
- Delete by name or phone.

Phone numbers are accepted if they have 10–15 digits and optionally begin with `+`.

## Example bulk input

```json
[{"name":"Aida","surname":"S","phone":"+77001234567"},{"name":"Beka","phone":"abc"}]
```

The invalid row is returned while the valid row is saved.

## GitHub

```bash
git add .
git commit -m "Add Practice8 - PhoneBook with functions and stored procedures"
git push origin main
```
