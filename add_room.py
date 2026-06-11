import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO rooms (
    room_number,
    room_type,
    price,
    status
)
VALUES (?, ?, ?, ?)
""", (
    "101",
    "Single",
    15000,
    "Available"
))

conn.commit()
conn.close()

print("Room added!")