from flask import Flask, render_template, request, redirect, url_for, session
import bdd
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)
app.secret_key = "demo-key"

MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_BASE_TOPIC = "Ynov/VHT"

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))

    pots = bdd.get_pots(session["user_id"])
    return render_template("dashboard.html", username=session["user"], pots=pots)

@app.route("/login", methods=["GET", "POST"])
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

@app.route("/signup", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if bdd.create_user(username, password):
            return redirect(url_for("login"))
        else:
            return "Utilisateur déjà existant"

    return render_template("signup.html")

@app.route("/add-pot", methods=["POST"])
def add_pot():
    if "user" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    name = request.form["name"]
    code = request.form["code"]
    nomtopic = "idClient"

    pot_id, topic = bdd.add_pot(user_id, name, code)

    topic = f"{MQTT_BASE_TOPIC}/{nomtopic}/{code}"
    payload = json.dumps({"user_id": session["user_id"]})
    mqtt_client.publish(topic, payload, qos=1)
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    bdd.init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
