# ==========================================
# Flask Loan Prediction Application
# ==========================================

from flask import Flask, render_template
from flask import request, redirect
from flask import session, flash

import sqlite3
import pickle
import secrets

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

# ==========================================
# Flask Configuration
# ==========================================

app = Flask(__name__)
app.secret_key = "loan_prediction_secret_key_2025"

# ==========================================
# Load Trained Model
# ==========================================

model = pickle.load(
    open("loan_model.pkl", "rb")
)

# ==========================================
# Create Database
# ==========================================

def create_database():

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


create_database()

# ==========================================
# Register Page
# ==========================================

@app.route("/")
def register_page():

    return render_template(
        "register.html"
    )

# ==========================================
# Register User
# ==========================================

@app.route(
    "/register",
    methods=["POST"]
)
def register():

    name = request.form["name"].strip()

    email = request.form["email"].strip().lower()

    password = request.form["password"]

    hashed_password = generate_password_hash(
        password
    )

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (name,email,password)
            VALUES (?,?,?)
            """,
            (
                name,
                email,
                hashed_password
            )
        )

        conn.commit()

        flash(
            "Registration Successful. Please Login.",
            "success"
        )

        return redirect("/login")

    except:

        flash(
            "Email already registered.",
            "danger"
        )

        return redirect("/")

    finally:

        conn.close()

# ==========================================
# Login Page
# ==========================================

@app.route("/login")
def login_page():

    return render_template(
        "login.html"
    )

# ==========================================
# Login User
# ==========================================

@app.route(
    "/login",
    methods=["POST"]
)
def login():

    email = request.form["email"].strip().lower()

    password = request.form["password"]

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id,name,password
        FROM users
        WHERE email=?
        """,
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        user_id = user[0]
        user_name = user[1]
        stored_password = user[2]

        if check_password_hash(
            stored_password,
            password
        ):

            session["logged_in"] = True
            session["user_id"] = user_id
            session["user_name"] = user_name

            flash(
                "Login Successful",
                "success"
            )

            return redirect(
                "/dashboard"
            )

    flash(
        "Invalid Email or Password",
        "danger"
    )

    return redirect("/login")

# ==========================================
# Dashboard
# ==========================================

@app.route("/dashboard")
def dashboard():

    if not session.get(
        "logged_in"
    ):
        return redirect("/login")

    return render_template(
        "dashboard.html",
        user_name=session["user_name"]
    )

# ==========================================
# Predict Loan
# ==========================================

@app.route("/predict", methods=["POST"])
def predict():

    # User login check
    if not session.get("logged_in"):
        return redirect("/login")

    try:
        # Form data lena
        age = int(request.form.get("Age", 0))
        income = float(request.form.get("Income", 0))
        loan_amount = float(request.form.get("LoanAmount", 0))
        credit_score = float(request.form.get("CreditScore", 0))

        # Debug ke liye
        print(request.form)

        # Prediction
        prediction = model.predict([
            [
                age,
                income,
                loan_amount,
                credit_score
            ]
        ])

        # Result
        if prediction[0] == 1:
            result = "✅ Loan Approved"
        else:
            result = "❌ Loan Rejected"

        return render_template(
            "dashboard.html",
            user_name=session["user_name"],
            prediction_text=result
        )

    except Exception as e:

        return render_template(
            "dashboard.html",
            user_name=session["user_name"],
            prediction_text=f"Error: {str(e)}"
        )
# ==========================================
# Logout
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "Logged Out Successfully",
        "danger"
    )

    return redirect("/")

# ==========================================
# Run App
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
