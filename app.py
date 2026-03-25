import os
from flask import Flask, render_template, request, jsonify
import psycopg2
from urllib.parse import urlparse

app = Flask(__name__)

# --- Parse PostgreSQL URL ---
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://varghese_user:DHuhZi1Ec1Olz1R88fx4CxdVwErnm6v2@dpg-d71sr9oule4c73d34v6g-a/varghese")

result = urlparse(DATABASE_URL)

db_host = result.hostname
db_port = result.port or 5432
db_name = result.path[1:]  # remove leading '/'
db_user = result.username
db_password = result.password

# --- Connect to PostgreSQL ---
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    database=db_name,
    user=db_user,
    password=db_password
)
cur = conn.cursor()

# --- Create contacts table if it doesn't exist ---
cur.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT,
    message TEXT
)
""")
conn.commit()

# --- Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    data = request.json
    cur.execute(
        "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
        (data['name'], data['email'], data['message'])
    )
    conn.commit()
    return jsonify({"message": "Message saved successfully!"})

@app.route('/admin')
def admin():
    admin_key = os.environ.get("ADMIN_KEY", "admin123")
    password = request.args.get('key')
    if password != admin_key:
        return "Unauthorized"
    cur.execute("SELECT * FROM contacts ORDER BY id DESC")
    data = cur.fetchall()
    return render_template("admin.html", data=data)

if __name__ == '__main__':
    app.run(debug=True)
