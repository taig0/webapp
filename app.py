from flask import Flask, jsonify, render_template, request
import sqlite3

app = Flask(__name__)

def get_database():
    database = sqlite3.connect("database.db")
    database.row_factory = sqlite3.Row

    return database

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.form

    name = data["name"]
    email = data["email"]

    database = get_database()

    user = database.execute("SELECT id FROM users WHERE email = ? AND name = ?", (email, name)).fetchone()
    if user is not None:
        database.close()
        return f"Hello, {name}!"

    database.execute("INSERT INTO users (name, email) VALUES(?, ?)", (name, email))

    database.commit()
    database.close()

    return "User created!"

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