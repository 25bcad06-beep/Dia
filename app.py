import os
from flask import Flask, render_template, request, jsonify
import psycopg2

# ✅ Force templates folder (important on Render sometimes)
app = Flask(__name__, template_folder='templates')


# --- Get DATABASE_URL from environment ---
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is not set in environment variables")


# --- Function to get DB connection ---
def get_db_connection():
    return psycopg2.connect(DATABASE_URL)


# --- Initialize DB ---
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name TEXT,
        email TEXT,
        message TEXT
    )
    """)

    conn.commit()
    cur.close()
    conn.close()


# ✅ Initialize DB safely
with app.app_context():
    init_db()


# --- Routes ---
@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        # 🔥 DEBUG: shows real error instead of blank "Not Found"
        return f"Error loading template: {str(e)}"


@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
        (data.get('name'), data.get('email'), data.get('message'))
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Message saved successfully!"})


@app.route('/admin')
def admin():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts ORDER BY id DESC")
    data = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("admin.html", data=data)


# --- Health check route (VERY IMPORTANT for debugging) ---
@app.route('/test')
def test():
    return "App is running ✅"


# --- Run locally only ---
if __name__ == '__main__':
    app.run(debug=True)
