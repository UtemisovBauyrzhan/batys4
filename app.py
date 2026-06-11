from flask import Flask
from rooms import rooms_bp
from bookings import bookings_bp
from search import search_bp

app = Flask(__name__)
app.register_blueprint(rooms_bp)
app.register_blueprint(bookings_bp)
app.register_blueprint(search_bp)

CSS = """<style>
body { font-family: Arial, sans-serif; background: #f8fafc; margin: 40px; color: #1e293b; display: flex; justify-content: center; }
.container { width: 400px; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
h1 { border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }
.menu { display: flex; flex-direction: column; gap: 15px; margin-top: 20px; }
a { color: #2563eb; text-decoration: none; font-weight: bold; font-size: 1.1rem; }
a:hover { text-decoration: underline; }
</style>"""

@app.route("/")
def home():
    return f"""
    {CSS}
    <div class="container">
        <h1>Hotel System</h1>
        <div class="menu">
            <a href='/rooms'>➔ View & Manage Rooms</a>
            <a href='/bookings'>➔ View & Manage Bookings</a>
            <a href='/search-booking'>➔ Search Booking</a>
        </div>
    </div>
    """

if __name__ == "__main__":
    app.run(debug=True)
