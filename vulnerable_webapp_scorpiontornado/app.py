from flask import Flask, request, render_template, session, redirect, url_for
from werkzeug.exceptions import NotFound, InternalServerError

# https://pythonhosted.org/Flask-Bootstrap/basic-usage.html --> Bootstrap 3
# https://bootstrap-flask.readthedocs.io/en/stable/migrate/ --> Turns out it was using Bootstrap 4.6.1
# https://bootstrap-flask.readthedocs.io/en/stable/api/#flask_bootstrap.Bootstrap5 --> Bootstrap 5
from flask_bootstrap import Bootstrap5

from vulnerable_webapp_scorpiontornado.db import init_sqli1_db
from vulnerable_webapp_scorpiontornado.auth import insecure_login

import os

from flask import Flask


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    bootstrap = Bootstrap5(app)

    # Default config (will be overridden by environment variables / test_config if they exist)
    app.config.from_mapping(
        SQLI1_DATABASE=os.path.join(app.instance_path, "sqli1.db"),
        SECRET_KEY="dev",
        SQLI1_FLAG="SAP{BOBBY_TABLES}",
    )

    if test_config is None:
        # When not testing, will load all environment variables starting with FLASK_ into the
        #   (instance) config (overriding existing values) so that FLASK_KEY=1 means app.config["KEY"] == 1
        # To set your own environment variables, make a .env file based on .env.example, and run:
        #   `source .env` in terminal (done by Heroku automatically when deploying to production).
        app.config.from_prefixed_env()
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Routes
    @app.route("/")
    def index():
        return render_template("index.html", heading="Index")

    @app.route("/sqli1")
    def sqli1():
        return render_template(
            "sqli1.html",
            heading="SQLI 1",
            username=session.get("username"),
            flag=app.config["SQLI1_FLAG"],
        )

    @app.route("/sqli1/login", methods=["GET", "POST"])
    def login():
        error = None
        hints = [
            "It's always good to start by testing the intended behaviour of a system. Try logging in with a random username and password.",
            "Next, its time to think like an attacker - what are things you could do to break it?",
            "Try entering a single quote (<code>'</code>) in the username or password field (note: may have to copy-paste it on mobile).",
            (
                "Uh oh! The query returned an error! This is a sign the form might be vulnerable to SQL injection, as data we (the user) have entered has affected the control of the program. "
                "The error is coming from us closing off the string with the quote, making the rest of the query invalid. "
                "As the program isn't sanitising our inputs, we can modify the sql query to do whatever we want. "
            ),
            (
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
            username, password = request.form.get("username"), request.form.get(
                "password"
            )
            res = insecure_login(username, password, app.config["SQLI1_DATABASE"])
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

        return render_template(
            "login.html",
            heading="Login",
            chal_name="sqli1",
            task_desc="SQLI 1 is a simple SQL injection challenge. There are two fields: username and password - both are vulnerable to SQL injection. Try to log in as any user!",
            error=error,
            hints=hints,
        )

    @app.route("/sqli1/logout")
    def logout():
        # Remove the username from the session if it's there
        session.pop("username", None)
        return redirect(url_for("sqli1"))

    # COMP6841 SQLI pre-reading: https://youtu.be/bAhvzXfuhg8
    @app.route("/sqli2")
    def sqli2():
        # TODO create db and tables ()

        error = None
        hints = [
            "As always, first try and use the system normally. Next, try and break it!",
            "Try entering a student ID that doesn't exist, nothing, or a single quote ' into the student ID field. What does this tell us about the system?",
            (
                "We also know that when we enter a single quote, we get an error - so, the system may be vulnerable to SQL injection. "
                "However, unlike SQLI 1, simply selecting all rows won't work. "
                "We can already do that by entering nothing (because of the ILIKE and wildcard %), but we can't see the flag. "
                "Where else could it be hidden?"
            ),
            (
                "UNION is a SQL operator that allows you to combine the results of two queries. "
                "Also, most database management systems have a table that contains information about the database itself, like the names of tables. "
                "To save you some trial-and-error, this server is using sqlite3, which has a table called sqlite_master. "
                "Try researching these concepts and see if you can find some information about table names."
            ),
            # TODO add more hints
            #   - Padding with 1- or NULL-filled columns to make the UNION valid / get the same number of columns as the original query
            #   - UNION with sqlite_master to find table names
            #   - UNION with sqlite_master to find column names
            #   - UNION with table names
        ]

        return render_template(
            "sqli2.html",
            heading="Student Lookup",
            chal_name="sqli2",
            task_desc="A benign student lookup system - you enter a student ID, and get back their name and email. What could go wrong?",
            error=error,
            hints=hints,
        )

    # TODO If request.method == "POST", then get inputs from form, execute(), then pass fetchall() into render_template
    # (For get, this variable will just start as None like I did with error in sqli1)
    # Still want to get error - invalid SQL query, and no results

    ### Resources

    @app.route("/resources/sqli")
    def sqli_resources():
        return render_template("sqli_resources.html", heading="SQL Injection Resources")

    ### Error handlers

    @app.errorhandler(NotFound)
    def page_not_found_error(error):
        return (
            render_template("error.html", heading="Error", error=error),
            NotFound.code,
        )

    @app.errorhandler(InternalServerError)
    def internal_server_error(error):
        return (
            render_template("error.html", heading="Error", error=error),
            InternalServerError.code,
        )

    # Initialise databases
    init_sqli1_db(app.config["SQLI1_DATABASE"])

    return app


# To allow the project to be run manually from the command line
# (with python3 src/vulnerable_webapp_scorpiontornado/app.py)
if __name__ == "__main__":
    # TODO add support for passing test_config as a command line argument
    create_app().run()
