import requests
from flask import Flask, render_template, session, request, redirect

server = Flask(__name__)


@server.route("/", methods=["GET", "POST"])
def start():
    session["bootstrap_path"] = "https://drrago.de/bootstrap.min.css"
    if (session.get("username") and session.get("password")):
        return redirect("/grades")
    return render_template("index.html")


@server.route("/grades", methods=["GET", ])
def grades():
    if (not session.get("username") or not session.get("password")):
        return redirect("/")
    return render_template("grades.html",
                           user_data=get_data(session.get("username"), session.get("password")).get("data"))


@server.route("/login", methods=["POST", ])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if ("@" not in username):
        username += "@dh-karlsruhe.de"

    session["username"] = username.lower()
    session["password"] = password

    data = get_data(session.get("username"), session.get("password"))

    if (data.get("code") != 200):
        logout()
        return redirect("/")

    return redirect("/grades")


def get_data(username, password):
    data = {
        "username": username.lower(),
        "password": password
    }
    response = make_request(data)
    return response.json()


@server.route("/logout")
def logout():
    theme = session["bootstrap_path"]
    session.clear()

    session["bootstrap_path"] = theme
    return redirect("/")


@server.route("/imprint")
def imprint():
    return render_template("imprint.html")


def make_request(data):
    return requests.get('http://localhost:8081/dualis/user', json=data)
