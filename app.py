import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
from helpers import login_required, apology

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///owned.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    firstname = db.execute("SELECT firstName FROM users WHERE id = (?) ",session["user_id"])[0]["firstName"]
    debts = db.execute("SELECT id,loaner,borrower, amount,date FROM transactions WHERE  isSettled = 0 AND loaner = :firstname OR borrower = :firstname",firstname=firstname)
    return render_template("index.html",debts=debts)



@app.route("/debt", methods=["GET","POST"])
@login_required
def debt():
    if request.method == "GET":
        return render_template("debt.html")
    else:
        loaner = request.form.get("loaner").lower()
        borrower = request.form.get("borrower").lower()
        print(loaner)
        print(borrower)
        amount = int(request.form.get("amount"))
        print(session["user_id"], loaner, borrower, amount)

        if amount <= 0:
            return apology("Cannot borrow negetive number", 400)

        db.execute("INSERT INTO transactions (userId,loaner,borrower, amount) VALUES (?, ?, ?, ?)", session["user_id"], loaner, borrower, amount)
        return redirect("/")



@app.route("/owe")
@login_required
def owe():
    firstname = db.execute("SELECT firstName FROM users WHERE id = (?)",session["user_id"])[0]["firstName"]
    debts = db.execute("SELECT id,loaner, amount, date FROM transactions WHERE isSettled = 0 AND borrower = (?)", firstname )
    return render_template("owe.html",debts=debts)


@app.route("/owed")
@login_required
def owed():
    firstname = db.execute("SELECT  firstName FROM users WHERE id = (?)",session["user_id"])[0]["firstName"]
    debts = db.execute("SELECT id, borrower, amount, date FROM transactions WHERE isSettled = 0 AND loaner = (?)", firstname )
    return render_template("owed.html",debts=debts)

@app.route("/discard", methods=["GET","POST"])
@login_required
def discard():
    if request.method == "POST":
        debt_id = request.form.get("discard")
        debt_info = db.execute("SELECT loaner, borrower, amount FROM transactions WHERE id = (?)",debt_id)[0]
        db.execute("UPDATE transactions SET isSettled = 1 WHERE id = (?)",debt_id)
        flash(f"Settled debt from {debt_info['loaner']} for ₪ {debt_info['amount']}")
        return redirect("/")
    else:
        return redirect("/")






@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")

        if not username or not password or not confirm:
            return apology("Fields cannot be empty",400)
        elif password != confirm:
            return apology("Password do not match",400)
        elif not firstname or not lastname:
            return apology("Name input cannot be empty",400)
        else:
            phash = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash, firstName, lastName) VALUES (?, ?, ?, ?)", username, phash, firstname, lastname)
            return redirect("/login")
    else:
        return render_template("register.html")

@app.route("/history")
def history():
    firstname = db.execute("SELECT firstName FROM users WHERE id = (?) ",session["user_id"])[0]["firstName"]
    debts = db.execute("SELECT * FROM transactions WHERE loaner = :firstname OR borrower = :firstname ORDER BY date ASC",firstname=firstname)
    counter = 0
    for debt in debts:
        if debt["isSettled"] == 0:
            debts[counter]["isSettled"] = "Not Settled"
            counter += 1
        else:
            debts[counter]["isSettled"] = "Settled"
            counter += 1
    print(debts)
    return render_template("history.html", debts=debts)




@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")