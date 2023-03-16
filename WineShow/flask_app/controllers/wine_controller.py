from flask_app import app
from flask import render_template, redirect, request, session, flash

from flask_app.models.wine import Wine
from flask_app.models.sommelier import Sommelier

# =================================================
# Create Wine Routes
# =================================================

@app.route("/new_wine")
def new_wine():
    if "sommelier_id" not in session:
        flash("Please login or register before entering the site!")
        return redirect("/")

    return render_template("new_wine.html", sommelier_id = session["sommelier_id"])

@app.route("/create_wine", methods=["POST"])
def create_wine():
    # 1 - validate form data
    # if no hidden input on form w/sommelier_id -> "sommelier_id" : session["sommelier_id"] instead
    data = {
        "name" : request.form["name"],
        "type" : request.form["type"],
        "age" : request.form["age"],
		"description" : request.form["description"],
        "sommelier_id" : request.form["sommelier_id"]
    }

    if not Wine.validate_wine(data):
        return redirect("/new_wine")
    # 2 - save new wine to database
    Wine.create_wine(data)

    # 3 - redirect back to the dashboard page
    return redirect("/dashboard")

# =================================================
# Show One Wine Route
# =================================================

@app.route("/wine/<int:wine_id>")
def show_wine(wine_id):
    if "sommelier_id" not in session:
        flash("Please login or register before entering the site!")
        return redirect("/")

    # 1 - query for wine info w/associated info of sommelier
    data = {
        "wine_id" : wine_id
    }
    wine = Wine.get_wine_with_sommelier(data)

    # 2 - send info to show page

    return render_template("show_wine.html", wine = wine)

# =================================================
# Edit One Wine Route
# =================================================

@app.route("/wine/<int:wine_id>/edit")
def edit_wine(wine_id):
    # 1 - query for the wine we want to update
    data = {
        "wine_id" : wine_id
    }
    wine = Wine.get_wine_with_sommelier(data)
    # 2 - pass wine info to the html
    return render_template("edit_wine.html", wine = wine)

@app.route("/wine/<int:wine_id>/update", methods=["POST"])
def update_wine(wine_id):
    # 1 - validate our form data
    data = {
        "name" : request.form["name"],
        "type" : request.form["type"],
        "age" : request.form["age"],
		"description" : request.form["description"],
        "wine_id" : wine_id
    }

    if not Wine.validate_wine(data):
        return redirect(f"/wine/{wine_id}/edit")
    # 2 - update information    
    Wine.update_wine_info(data)
    # 3 - redirect to dashboard

    return redirect("/dashboard")

# =================================================
# Delete One Wine Route
# =================================================

@app.route("/wine/<int:wine_id>/delete")
def delete_wine(wine_id):
    # 1 - delete wine
    data = {
        "wine_id" : wine_id
    }
    Wine.delete_wine(data)

    # 2 - redirect to dashboard
    return redirect("/dashboard")