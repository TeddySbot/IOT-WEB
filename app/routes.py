from flask import Flask, render_template, request, redirect, url_for, session
import bdd 

main = Flask("main", __name__)
main.secret_key = "demo-key"

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

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if bdd.create_user(username, password):
            return redirect(url_for("login"))
        else:
            return "Utilisateur déjà existant"

    return render_template("register.html")

@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
