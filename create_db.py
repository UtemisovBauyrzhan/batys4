import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_number TEXT,
    room_type TEXT,
    price REAL,
    status TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guest_name TEXT,
    room_id INTEGER,
    check_in TEXT,
    check_out TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()

print("Database created!")