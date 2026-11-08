import os

DB_CONFIG = {
    "dbname": os.getenv("PGDATABASE", "phonebook_db"),
    "user": os.getenv("PGUSER", "symbat"),
    "password": os.getenv("PGPASSWORD", ""),
    "host": os.getenv("PGHOST", "localhost"),
    "port": os.getenv("PGPORT", "5433"),
}
