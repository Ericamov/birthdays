import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    # Ensure responses aren't cached
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Save the user's input into variables
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        # Validate input
        if not name or not month or not day:
            print("Input is empty")
            return redirect("/")
        
        try:
            month = int(month)
            day = int(day)
        except ValueError:
            print("Not an integer")
            return redirect("/")

        if month not in range(1, 13):
            print("Invalid month")
            return redirect("/")

        if day not in range(1, 32):
            print("Invalid day")
            return redirect("/")

        # Add the new birthday into the database
        db.execute("Insert INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)

        return redirect("/")

    else:
        # Display the entries in the database on index.html
        birthdays = db.execute("SELECT * FROM birthdays")
        
        return render_template("index.html", birthdays=birthdays)

@app.route("/deregister", methods=["POST"])
def deregister():
    # Delete user data using it's id
    id = request.form.get("id")   
    if id:
        db.execute("DELETE FROM birthdays WHERE id = ?", id)

    return redirect("/")
