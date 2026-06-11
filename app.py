from flask import Flask, request
import sqlite3

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>Hotel Booking System</h1>

    <a href='/rooms'>View Rooms</a>
    <br><br>

    <a href='/add-room'>Add Room</a>
    <br><br>

    <a href='/bookings'>View Bookings</a>
    <br><br>

    <a href='/add-booking'>Add Booking</a>
<br><br>

<a href='/search-booking'>Search Booking</a>
"""


@app.route("/rooms")
def rooms():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM rooms")
    rooms = cursor.fetchall()

    conn.close()

    result = """
    <h1>Rooms</h1>

    <a href='/add-room'>Add New Room</a>

    <br><br>
    """

    for room in rooms:

        result += f"""
        <p>

        ID: {room[0]} |
        Room: {room[1]} |
        Type: {room[2]} |
        Price: {room[3]} KZT |
        Status: {room[4]}

        <a href='/edit-room/{room[0]}'>Edit</a>

        |

        <a href='/delete-room/{room[0]}'>Delete</a>

        </p>
        """

    result += "<br><a href='/'>Home</a>"

    return result


@app.route("/add-room", methods=["GET", "POST"])
def add_room():

    if request.method == "POST":

        room_number = request.form["room_number"]
        room_type = request.form["room_type"]
        price = request.form["price"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO rooms
            (room_number, room_type, price, status)
            VALUES (?, ?, ?, ?)
            """,
            (room_number, room_type, price, "Available")
        )

        conn.commit()
        conn.close()

        return """
        <h2>Room Added Successfully!</h2>
        <a href='/rooms'>View Rooms</a>
        """

    return """
    <h1>Add Room</h1>

    <form method='POST'>

        Room Number:
        <br>
        <input name='room_number' required>

        <br><br>

        Room Type:
        <br>
        <input name='room_type' required>

        <br><br>

        Price:
        <br>
        <input name='price' required>

        <br><br>

        <button type='submit'>
            Add Room
        </button>

    </form>
    """


@app.route("/edit-room/<int:id>", methods=["GET", "POST"])
def edit_room(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":

        room_number = request.form["room_number"]
        room_type = request.form["room_type"]
        price = request.form["price"]
        status = request.form["status"]

        cursor.execute(
            """
            UPDATE rooms
            SET room_number=?,
                room_type=?,
                price=?,
                status=?
            WHERE id=?
            """,
            (room_number, room_type, price, status, id)
        )

        conn.commit()
        conn.close()

        return """
        <h2>Room Updated Successfully!</h2>
        <a href='/rooms'>Back to Rooms</a>
        """

    cursor.execute(
        "SELECT * FROM rooms WHERE id=?",
        (id,)
    )

    room = cursor.fetchone()

    conn.close()

    return f"""
    <h1>Edit Room</h1>

    <form method='POST'>

        Room Number:
        <br>
        <input name='room_number' value='{room[1]}' required>

        <br><br>

        Room Type:
        <br>
        <input name='room_type' value='{room[2]}' required>

        <br><br>

        Price:
        <br>
        <input name='price' value='{room[3]}' required>

        <br><br>

        Status:
        <br>
        <input name='status' value='{room[4]}' required>

        <br><br>

        <button type='submit'>
            Save Changes
        </button>

    </form>
    """


@app.route("/delete-room/<int:id>")
def delete_room(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM rooms WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return """
    <h2>Room Deleted Successfully!</h2>
    <a href='/rooms'>Back to Rooms</a>
    """


@app.route("/bookings")
def bookings():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()

    conn.close()

    result = """
    <h1>Bookings</h1>

    <a href='/add-booking'>Add Booking</a>

    <br><br>
    """

    for booking in bookings:

        result += f"""
        <p>

        ID: {booking[0]} |
        Guest: {booking[1]} |
        Room ID: {booking[2]} |
        Check In: {booking[3]} |
        Check Out: {booking[4]} |
        Status: {booking[5]}

        <a href='/delete-booking/{booking[0]}'>
            Delete
        </a>

        </p>
        """

    result += "<br><a href='/'>Home</a>"

    return result


@app.route("/add-booking", methods=["GET", "POST"])
def add_booking():

    if request.method == "POST":

        guest_name = request.form["guest_name"]
        room_id = request.form["room_id"]
        check_in = request.form["check_in"]
        check_out = request.form["check_out"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO bookings
            (
                guest_name,
                room_id,
                check_in,
                check_out,
                status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                guest_name,
                room_id,
                check_in,
                check_out,
                "Active"
            )
        )

        conn.commit()
        conn.close()

        return """
        <h2>Booking Created Successfully!</h2>
        <a href='/bookings'>View Bookings</a>
        """

    return """
    <h1>Add Booking</h1>

    <form method='POST'>

        Guest Name:
        <br>
        <input name='guest_name' required>

        <br><br>

        Room ID:
        <br>
        <input name='room_id' required>

        <br><br>

        Check In:
        <br>
        <input type='date' name='check_in' required>

        <br><br>

        Check Out:
        <br>
        <input type='date' name='check_out' required>

        <br><br>

        <button type='submit'>
            Create Booking
        </button>

    </form>
    """


@app.route("/delete-booking/<int:id>")
def delete_booking(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM bookings WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return """
<h2>Booking Deleted Successfully!</h2>
<a href='/bookings'>Back to Bookings</a>
"""


@app.route("/search-booking", methods=["GET", "POST"])
def search_booking():

    if request.method == "POST":

        guest_name = request.form["guest_name"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM bookings WHERE guest_name LIKE ?",
            ('%' + guest_name + '%',)
        )

        bookings = cursor.fetchall()

        conn.close()

        result = f"""
        <h1>Search Results</h1>

        <h3>Guest: {guest_name}</h3>

        <a href='/search-booking'>
            New Search
        </a>

        <br><br>
        """

        if len(bookings) == 0:
            result += "<p>No bookings found.</p>"

        for booking in bookings:

            result += f"""
            <p>

            ID: {booking[0]} |
            Guest: {booking[1]} |
            Room ID: {booking[2]} |
            Check In: {booking[3]} |
            Check Out: {booking[4]} |
            Status: {booking[5]}

            </p>
            """

        result += """
        <br>
        <a href='/bookings'>
            Back to Bookings
        </a>
        """

        return result

    return """
    <h1>Search Booking</h1>

    <form method='POST'>

        Guest Name:

        <br>

        <input name='guest_name' required>

        <br><br>

        <button type='submit'>
            Search
        </button>

    </form>

    <br>

    <a href='/'>
        Home
    </a>
    """
if __name__ == "__main__":
    app.run(debug=True)


    