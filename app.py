from flask import Flask, jsonify, render_template, request
from psycopg.rows import dict_row
import psycopg

import os

database_url = os.environ["DATABASE_URL"]

app = Flask(__name__)

def get_database():
    return psycopg.connect(database_url, row_factory=dict_row) 

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.form

    name = data["name"]
    email = data["email"]

    database = get_database()

    user = database.execute("SELECT id FROM users WHERE email = %s AND name = %s", (email, name)).fetchone()
    if user is not None:
        database.close()
        return f"Hello, {name}!"

    database.execute("INSERT INTO users (name, email) VALUES(%s, %s)", (name, email))

    database.commit()
    database.close()

    return "User created!"

@app.route("/users")
def users_page():
    return render_template("users.html")

@app.route("/api/users")
def get_users():
    database = get_database()

    users = database.execute(
        "SELECT * FROM users"
    ).fetchall()

    database.close()

    return jsonify([dict(user) for user in users])

if __name__ == "__main__":
    app.run(debug=True)