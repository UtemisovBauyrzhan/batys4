from flask import Blueprint, request
import sqlite3

bookings_bp = Blueprint('bookings', __name__)

CSS = """<style>
body { font-family: Arial, sans-serif; background: #f8fafc; margin: 40px; color: #1e293b; }
.container { max-width: 600px; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.card { background: #f1f5f9; padding: 15px; border-radius: 6px; margin-bottom: 10px; display: flex; justify-content: space-between; }
a { color: #2563eb; text-decoration: none; font-weight: bold; }
input { display: block; width: 100%; padding: 8px; margin: 10px 0 20px 0; border: 1px solid #cbd5e1; border-radius: 4px; }
button { background: #2563eb; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-weight: bold; }
</style>"""

@bookings_bp.route("/bookings")
def view_bookings():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings")
    bookings_data = cursor.fetchall()
    conn.close()

    result = f"{CSS}<div class='container'><h1>Bookings</h1><a href='/add-booking'>+ Add Booking</a><br><br>"
    for b in bookings_data:
        result += f"""
        <div class='card'>
            <div>ID: {b[0]} | Guest: {b[1]} | Room ID: {b[2]} | {b[3]} to {b[4]} ({b[5]})</div>
            <div><a href='/delete-booking/{b[0]}' style='color:red;'>Delete</a></div>
        </div>"""
    result += "<br><a href='/'>← Home</a></div>"
    return result

@bookings_bp.route("/add-booking", methods=["GET", "POST"])
def add_booking():
    if request.method == "POST":
        guest_name = request.form["guest_name"]
        room_id = request.form["room_id"]
        check_in = request.form["check_in"]
        check_out = request.form["check_out"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bookings (guest_name, room_id, check_in, check_out, status) VALUES (?, ?, ?, ?, ?)",
                       (guest_name, room_id, check_in, check_out, "Active"))
        conn.commit()
        conn.close()
        return f"{CSS}<div class='container'><h2>Booking Created!</h2><a href='/bookings'>View Bookings</a></div>"

    return f"""{CSS}<div class='container'><h1>Add Booking</h1>
    <form method='POST'>
        <label>Guest Name:</label><input name='guest_name' required>
        <label>Room ID:</label><input name='room_id' type='number' required>
        <label>Check In:</label><input type='date' name='check_in' required>
        <label>Check Out:</label><input type='date' name='check_out' required>
        <button type='submit'>Create Booking</button>
    </form><br><a href='/'>← Cancel</a></div>"""

@bookings_bp.route("/delete-booking/<int:id>")
def delete_booking(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return f"{CSS}<div class='container'><h2 style='color:red;'>Booking Deleted!</h2><a href='/bookings'>Back to Bookings</a></div>"
