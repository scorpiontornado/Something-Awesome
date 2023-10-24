import sqlite3
from flask import Flask, request, render_template, session, redirect, url_for
from werkzeug.exceptions import NotFound, InternalServerError

# https://pythonhosted.org/Flask-Bootstrap/basic-usage.html --> Bootstrap 3
# https://bootstrap-flask.readthedocs.io/en/stable/migrate/ --> Turns out it was using Bootstrap 4.6.1
# https://bootstrap-flask.readthedocs.io/en/stable/api/#flask_bootstrap.Bootstrap5 --> Bootstrap 5
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
bootstrap = Bootstrap5(app)

# Secret key: used to sign the session cookies cryptographically. This means that the user could
# look at the contents of the cookie, but not modify it without knowing this secret key.
#   - Generate with: python -c 'import secrets; print(secrets.token_hex())'
#   - Ideally wouldn't hardcode it.
#   - See: https://flask.palletsprojects.com/en/3.0.x/quickstart/#sessions
app.config[
    "SECRET_KEY"
] = "9d856fb340bb797805e0ccc5e5015837fb5725eb7d22925609035bfb929bbac5"
app.config["flags"] = {
    "sqli1": "SAP{BOBBY_TABLES}"  # Would redact if actually used for teaching
}


@app.route("/")
def index():
    return render_template("index.html", heading="Index")


@app.route("/sqli1")
def sqli1():
    return render_template(
        "sqli1.html",
        heading="SQLI 1",
        username=session.get("username"),
        flag=app.config["flags"]["sqli1"],
    )


@app.route("/sqli1/login", methods=["GET", "POST"])
def login():
    error = None
    hints = [
        "It's always good to start by testing the intended behaviour of a system. Try logging in with a random username and password",
        "Next, its time to think like an attacker - what are things you could do to break it?",
        "Try entering a single quote (<code>'</code>) in the username or password field",
        (
            "Now that we've successfully closed off the string, we can modify the sql query to do whatever we want. "
            "How would you get the <code>WHERE</code> condition to always be true? "
            "This would match all rows (users) in the table. Then, the website would log you in as the first user - regardless of their username/password."
        ),
        "<code>1=1</code>, <code>'1'='1'</code> etc. all evaluate to true. What if tried to OR this with the rest of the condition?",
        (
            "One way of doing this is entering: <code>' OR '1'='1</code> into both the username and password fields. "
            "How does this affect the query that gets executed? "
            "As a challenge, try to figure out how to get the flag by only inserting into the username field, leaving the password blank."
        ),
        "Another way of dealing with that extra <code>'</code> is to comment out the rest of the query. In SQL, comments start with <code>--</code>.",
        (
            "We first want to close off the string using a single quote. "
            "Next, we want to make the <code>WHERE</code> condition always true to match every user, so we enter <code>OR 1=1</code>. "
            "Many SQL implementations require queries to be terminated with a semicolon, so its good practice to include. "
            "Finally, we comment out the rest of the query to make it valid - anything after the two hyphens will be ignored. "
            "Our final payload (that we enter into the username field) is thus: <code>' OR 1=1; -- </code>"
        ),
    ]

    if request.method == "POST":
        # Modified from COMP6841 Quoccabank SQLI 2
        username, password = request.form.get("username"), request.form.get("password")
        res = login(username, password)
        print(res)

        # Invalid query
        if res is False:
            error = "<strong>Error!</strong> Invalid SQL query"
        # No results for the query
        elif res is None:
            error = "Incorrect username/password"
        # Successful login
        else:
            session["username"] = res[0]
            return redirect(url_for("sqli1"))

    return render_template("login.html", heading="Login", error=error, hints=hints)


@app.route("/sqli1/logout")
def logout():
    # Remove the username from the session if it's there
    session.pop("username", None)
    return redirect(url_for("sqli1"))


@app.errorhandler(NotFound)
def page_not_found_error(error):
    return render_template("error.html", heading="Error", error=error), NotFound.code


@app.errorhandler(InternalServerError)
def internal_server_error(error):
    return (
        render_template("error.html", heading="Error", error=error),
        InternalServerError.code,
    )


### Database code
def execute(con, query, parameters=()):
    # Moved database connection outside, as fetchone() is a Cursor method & Cursors close when their
    # parent connection does. Not closing would slow down the system over time.
    cur = con.cursor()

    try:
        res = cur.execute(query, parameters)
    except Exception as e:
        # Invalid SQL query
        # Could instead have a route for internal server error
        print(e)
        res = None

    return res


# Modified from 6841 Quoccabank SQLI2. Returns:
# - False on error (usually invalid query)
# - None when there are no results for the query (i.e., no rows with the given username/password)
# - The username of the first row to fulfill the condition (matching username/password)
def login(username, password):
    # "with" will auto-close the connection
    with sqlite3.connect("sqli1.db") as con:
        #! VULNERABLE TO SQLI - should use placeholders instead of string formatting:
        # https://docs.python.org/3/library/sqlite3.html#sqlite3-placeholders
        print(
            "Executing...",
            f"SELECT username FROM Users WHERE username='{username}' AND password='{password}'",
        )  # Debugging, can remove

        res = execute(
            con,
            f"SELECT username FROM Users WHERE username='{username}' AND password='{password}'",
        )

        return res.fetchone() if res else False


if __name__ == "__main__":
    print("Connecting to database...")

    con = sqlite3.connect("sqli1.db")  # Will create db if doesn't exist

    try:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Users")
        cur.execute(
            "CREATE TABLE Users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, is_admin INTEGER)"
        )

        # An example of using placeholders rather than format strings
        # (If used as a teaching tool, this would either be redacted or passwords would be hashed)
        data = [
            ("admin", "correcthorsebatterystaple", "TRUE"),
            ("Nick", "hunter2", "FALSE"),
        ]
        cur.executemany(
            "INSERT INTO Users(username, password, is_admin) VALUES(?, ?, ?)", data
        )

        con.commit()

        # print(
        #     "test",
        #     cur.execute(
        #         f"SELECT username FROM Users WHERE username='admin' AND password='correcthorsebatterystaple'"
        #     ).fetchone(),
        # )  # TESTING - returns: test ('admin',)
    except Exception as e:
        print("Error creating SQLI 1 database:", e)
        con.rollback()

    con.close()
    app.run()
