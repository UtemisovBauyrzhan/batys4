from flask import Blueprint, request
import sqlite3

rooms_bp = Blueprint('rooms', __name__)
CSS = """<style>
body { font-family: Arial, sans-serif; background: #f8fafc; margin: 40px; color: #1e293b; }
.container { max-width: 600px; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.card { background: #f1f5f9; padding: 15px; border-radius: 6px; margin-bottom: 10px; display: flex; justify-content: space-between; }
a { color: #2563eb; text-decoration: none; font-weight: bold; }
input { display: block; width: 100%; padding: 8px; margin: 10px 0 20px 0; border: 1px solid #cbd5e1; border-radius: 4px; }
button { background: #2563eb; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-weight: bold; }
</style>"""

@rooms_bp.route("/rooms")
def view_rooms():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rooms")
    rooms_data = cursor.fetchall()
    conn.close()

    result = f"{CSS}<div class='container'><h1>Rooms</h1><a href='/add-room'>+ Add New Room</a><br><br>"
    for room in rooms_data:
        result += f"""
        <div class='card'>
            <div>ID: {room[0]} | Room: {room[1]} | {room[2]} | {room[3]} KZT | {room[4]}</div>
            <div>
                <a href='/edit-room/{room[0]}'>Edit</a> | 
                <a href='/delete-room/{room[0]}' style='color:red;'>Delete</a>
            </div>
        </div>"""
    result += "<br><a href='/'>← Home</a></div>"
    return result

@rooms_bp.route("/add-room", methods=["GET", "POST"])
def add_room():
    if request.method == "POST":
        room_number = request.form["room_number"]
        room_type = request.form["room_type"]
        price = request.form["price"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO rooms (room_number, room_type, price, status) VALUES (?, ?, ?, ?)",
                       (room_number, room_type, price, "Available"))
        conn.commit()
        conn.close()
        return f"{CSS}<div class='container'><h2>Room Added Successfully!</h2><a href='/rooms'>Back to Rooms</a></div>"

    return f"""{CSS}<div class='container'><h1>Add Room</h1>
    <form method='POST'>
        <label>Room Number:</label><input name='room_number' required>
        <label>Room Type:</label><input name='room_type' required>
        <label>Price:</label><input name='price' type='number' required>
        <button type='submit'>Add Room</button>
    </form><br><a href='/rooms'>← Back</a></div>"""

@rooms_bp.route("/edit-room/<int:id>", methods=["GET", "POST"])
def edit_room(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":
        room_number = request.form["room_number"]
        room_type = request.form["room_type"]
        price = request.form["price"]
        status = request.form["status"]

        cursor.execute("UPDATE rooms SET room_number=?, room_type=?, price=?, status=? WHERE id=?",
                       (room_number, room_type, price, status, id))
        conn.commit()
        conn.close()
        return f"{CSS}<div class='container'><h2>Room Updated!</h2><a href='/rooms'>Back to Rooms</a></div>"

    cursor.execute("SELECT * FROM rooms WHERE id=?", (id,))
    room = cursor.fetchone()
    conn.close()
    return f"""{CSS}<div class='container'><h1>Edit Room</h1>
    <form method='POST'>
        <input name='room_number' value='{room[1]}' required>
        <input name='room_type' value='{room[2]}' required>
        <input name='price' value='{room[3]}' required>
        <input name='status' value='{room[4]}' required>
        <button type='submit'>Save Changes</button>
    </form></div>"""

@rooms_bp.route("/delete-room/<int:id>")
def delete_room(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rooms WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return f"{CSS}<div class='container'><h2 style='color:red;'>Room Deleted!</h2><a href='/rooms'>Back to Rooms</a></div>"
