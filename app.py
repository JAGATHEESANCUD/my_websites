from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["login_db"]
users_collection = db["users"]


# 🔹 LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = users_collection.find_one({"username": username})

        if user and check_password_hash(user["password"], password):
            return render_template("dashboard.html", username=username)
        else:
            return "Invalid username or password"

    return render_template("login.html")


# 🔹 REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if user already exists
        if users_collection.find_one({"username": username}):
            return "User already exists"

        hashed_password = generate_password_hash(password)

        users_collection.insert_one({
            "username": username,
            "password": hashed_password
        })

        return redirect(url_for("login"))

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
