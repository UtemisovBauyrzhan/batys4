from flask import Blueprint, request
import sqlite3

search_bp = Blueprint('search', __name__)

CSS = """<style>
body { font-family: Arial, sans-serif; background: #f8fafc; margin: 40px; color: #1e293b; }
.container { max-width: 600px; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.card { background: #f1f5f9; padding: 15px; border-radius: 6px; margin-bottom: 10px; display: flex; justify-content: space-between; }
a { color: #2563eb; text-decoration: none; font-weight: bold; }
input { display: block; width: 100%; padding: 8px; margin: 10px 0 20px 0; border: 1px solid #cbd5e1; border-radius: 4px; }
button { background: #2563eb; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-weight: bold; }
</style>"""

@search_bp.route("/search-booking", methods=["GET", "POST"])
def search_booking():
    if request.method == "POST":
        guest_name = request.form["guest_name"]
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookings WHERE guest_name LIKE ?", ('%' + guest_name + '%',))
        bookings_data = cursor.fetchall()
        conn.close()

        result = f"{CSS}<div class='container'><h1>Search Results</h1><h3>Query: {guest_name}</h3>"
        if not bookings_data:
            result += "<p>No bookings found.</p>"
        for b in bookings_data:
            result += f"<div class='card'><div><strong>Guest:</strong> {b[1]} | <strong>Room ID:</strong> {b[2]} | <strong>Dates:</strong> {b[3]} - {b[4]}</div></div>"
        result += "<br><a href='/search-booking'>New Search</a> | <a href='/'>Home</a></div>"
        return result

    return f"""{CSS}<div class='container'><h1>Search Booking</h1>
    <form method='POST'>
        <label>Guest Name:</label><input name='guest_name' required>
        <button type='submit'>Search</button>
    </form><br><a href='/'>← Home</a></div>"""
