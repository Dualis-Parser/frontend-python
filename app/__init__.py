import requests
import werkzeug.exceptions
from flask import Flask, render_template, session, request, redirect

server = Flask(__name__)


@server.route("/", methods=["GET", ])
def start():
    session["bootstrap_path"] = "https://drrago.de/bootstrap.min.css"
    if (session.get("username") and session.get("password")):
        return redirect("/grades")
    return render_template("index.html")


@server.route("/grades", methods=["GET", ])
def grades():
    if (not session.get("username") or not session.get("password")):
        return redirect("/")

    data = get_data(session.get("username"), session.get("password")).get("data")
    return render_template("grades.html", user_data=data)


@server.route("/login", methods=["POST", ])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if ("@" not in username):
        username += "@dh-karlsruhe.de"

    session["username"] = username.lower()
    session["password"] = password

    data = get_data(session.get("username"), session.get("password"), "http://localhost:8081/dualis/user/validate")

    if not data.get("data", False):
        logout()
        return redirect("/")

    return redirect("/grades")


def get_data(username, password, url='http://localhost:8081/dualis/user'):
    data = {
        "username": username.lower(),
        "password": password
    }
    response = make_request(data, url)
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


def make_request(data, url):
    return requests.get(url, json=data)


@server.errorhandler(Exception)
def exception_handler(error):
    """
    Return a error json string. If it is a werkzeug error (like 404 or 400) send a specific message, otherwise

    :param error: the exception that occurred
    :type error: Exception or werkzeug.exceptions.HTTPException

    :return: the template to render
    """

    # determine whether the exception is a HTTP exception
    if (issubclass(type(error), werkzeug.exceptions.HTTPException)):
        error_files = [400, 401, 403, 404, 405, 500, 501, 502, 503, 520, 521, 533]
        return_code = error.code
        if error.code not in error_files:
            return_code = 500
    else:
        return_code = 500

    return render_template("ErrorPages/HTTP%d.html" % return_code), return_code
