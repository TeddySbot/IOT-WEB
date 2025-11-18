from flask import render_template, request, redirect, url_for, session, Blueprint
from app import bdd 

main = Blueprint("main", __name__)

@main.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))

    pots = bdd.get_pots(session["user_id"])
    return render_template("dashboard.html", username=session["user"], pots=pots)

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = bdd.get_user(username, password)
        if user:
            session["user"] = user["username"]
            session["user_id"] = user["id"]
            return redirect(url_for("home"))
        return "Identifiants invalides"

    return render_template("login.html")

@main.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        created = bdd.create_user(username, password)
        if created:
            return redirect(url_for("main.login"))
        else:
            return "Utilisateur déjà existant"

    return render_template("signup.html")

@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@main.route("/add-pot", methods=["POST"])
def add_pot():
    if "user" not in session:
        return redirect(url_for("login"))

    name = request.form["name"]

    bdd.add_pot(session["user_id"], name)
    return redirect(url_for("home"))