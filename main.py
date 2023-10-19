import sqlite3
from flask import Flask, request, render_template, session, redirect, url_for
from werkzeug.exceptions import NotFound, InternalServerError

app = Flask(__name__)

# Secret key: used to sign the session cookies cryptographically. This means that the user could
# look at the contents of the cookie, but not modify it without knowing this secret key.
#   - Generate with: python -c 'import secrets; print(secrets.token_hex())'
#   - Ideally wouldn't hardcode it.
#   - See: https://flask.palletsprojects.com/en/3.0.x/quickstart/#sessions
app.config[
    "SECRET_KEY"
] = "9d856fb340bb797805e0ccc5e5015837fb5725eb7d22925609035bfb929bbac5"
app.config["FLAG"] = "SAP{BOBBY_TABLES}"  # Would redact if actually used for teaching


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sqli1")
def sqli1():
    return render_template("sqli1.html", username=session.get("username"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        # Modified from COMP6841 Quoccabank SQLI 2
        username, password = request.form.get("username"), request.form.get("password")
        res = login(username, password)

        # Invalid query
        if res is False:
            error = "<strong>Error!</strong> Invalid SQL query"
        # No results for the query
        elif res is None:
            error = "Invalid username/password"
        # Successful login
        else:
            session["username"] = res[0]
            return redirect(url_for("sqli1"))

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    # Remove the username from the session if it's there
    session.pop("username", None)
    return redirect(url_for("sqli1"))


@app.errorhandler(NotFound)
def page_not_found_error(error):
    return render_template("error.html", error=error), NotFound.code


@app.errorhandler(InternalServerError)
def internal_server_error(error):
    return render_template("error.html", error=error), InternalServerError.code


### Database code
def execute(query, parameters=None):
    con = sqlite3.connect("sqli1.db")
    cur = con.cursor()

    try:
        res = cur.execute(query, parameters)
    except Exception as e:
        # Invalid SQL query
        # Could instead have a route for internal server error
        print(e)
        res = None

    con.close()
    return res


# Modified from 6841 Quoccabank SQLI2. Returns:
# - False on error (usually invalid query)
# - None when there are no results for the query (i.e., no rows with the given username/password)
# - The username of the first row to fulfill the condition (matching username/password)
def login(username, password):
    #! VULNERABLE TO SQLI - should use placeholders instead of string formatting:
    # https://docs.python.org/3/library/sqlite3.html#sqlite3-placeholders
    res = execute(
        f"SELECT username FROM Users WHERE username='{username}' AND password='{password}'"
    )
    return res.fetchone() if res else False


if __name__ == "__main__":
    con = sqlite3.connect("sqli1.db")

    try:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Users")
        cur.execute(
            "CREATE TABLE Users(id INTEGER PRIMARY KEY AUTOINCREMENT, username, password, is_admin)"
        )

        # An example of using placeholders rather than format strings
        # (If used as a teaching tool, this would either be redacted or passwords would be hashed)
        data = [
            ("admin", "correcthorsebatterystaple", "TRUE"),
            ("Nick", "hunter2", "FALSE"),
        ]
        cur.executemany("INSERT INTO Users(username, password) VALUES(?, ?)", data)
        con.commit()
    except Exception as e:
        print("Error creating SQLI 1 database:", e)
        con.rollback()

    con.close()
    app.run()
