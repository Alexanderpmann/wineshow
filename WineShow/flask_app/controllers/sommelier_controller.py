from flask_app import app
from flask import render_template, redirect, request, session, flash

#controllers file always has upper case model name
from flask_app.models.sommelier import Sommelier 
from flask_app.models.wine import Wine

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

# =================================================
# Register / Login Routes
# =================================================

@app.route("/register", methods=["POST"])
def register():
    # 1 - validating form information
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : request.form["password"],
        "pass_conf" : request.form["pass_conf"]
    }

    if not Sommelier.validate_register(data):
        return redirect("/")

    # 2 - bcrypt password
    data["password"] = bcrypt.generate_password_hash(request.form['password'])

    # 3 - save new sommelier to db
    new_sommelier_id = Sommelier.create_sommelier(data)
    # 4 - enter sommelier id into session and redirect to dashboard
    session["sommelier_id"] = new_sommelier_id
    return redirect("/dashboard")

@app.route("/login", methods=["POST"])
def login():
    # 1 - validate login info
    data = {
        "email" : request.form["email"],
        "password" : request.form["password"]
    }
    if not Sommelier.validate_login(data):
        return redirect("/")
    # 2 - query for sommelier info based on email
    sommelier = Sommelier.get_by_email(data)

    # 3 - put sommelier id into session and redirect to dashboard
    session["sommelier_id"] = sommelier.id
    return redirect("/dashboard")


# =================================================
# Render Dashboard Route - this route will reference both models
# =================================================

@app.route("/dashboard")
def dashboard():
    if "sommelier_id" not in session:
        flash("Please login or register before entering the site!")
        return redirect("/")

    data = {
        "sommelier_id" : session["sommelier_id"]
    }
    sommelier = Sommelier.get_by_id(data)
    all_wines = Wine.get_all()

    return render_template("dashboard.html", sommelier = sommelier, all_wines = all_wines)


# =================================================
# Logout Route
# =================================================

@app.route("/logout")
def logout():
    session.clear()
    flash("Successfully logged out!")
    return redirect("/")