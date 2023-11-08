from flask import Flask, request, render_template, session, redirect, url_for
from werkzeug.exceptions import NotFound, InternalServerError

# https://pythonhosted.org/Flask-Bootstrap/basic-usage.html --> Bootstrap 3
# https://bootstrap-flask.readthedocs.io/en/stable/migrate/ --> Turns out it was using Bootstrap 4.6.1
# https://bootstrap-flask.readthedocs.io/en/stable/api/#flask_bootstrap.Bootstrap5 --> Bootstrap 5
from flask_bootstrap import Bootstrap5

from vulnerable_webapp_scorpiontornado.db import init_sqli1_db, init_sqli2_db
from vulnerable_webapp_scorpiontornado.auth import insecure_login

import os
import sqlite3
from vulnerable_webapp_scorpiontornado.db import execute


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    bootstrap = Bootstrap5(app)

    # Default config (will be overridden by environment variables / test_config if they exist)
    app.config.from_mapping(
        SQLI1_DATABASE=os.path.join(app.instance_path, "sqli1.db"),
        SQLI2_DATABASE=os.path.join(app.instance_path, "sqli2.db"),
        SQLI2_SCHEMA=os.path.join(app.root_path, "sqli2_schema.sql"),
        SQLI2_DATA=os.path.join(app.root_path, "sqli2_data.sql"),
        SECRET_KEY="dev",
        SQLI1_FLAG="SAP{BOBBY_TABLES}",
        # TODO add SQLI2_FLAG1, SQLI2_FLAG2, update flag if env set
    )

    if test_config is None:
        # When not testing, will load all environment variables starting with FLASK_ into the
        #   (instance) config (overriding existing values) so that FLASK_KEY=1 means app.config["KEY"] == 1
        # To set your own environment variables, make a .env file based on .env.example, and run:
        #   `source .env` in terminal (done by Heroku automatically when deploying to production).
        app.config.from_prefixed_env()
        # TODO add different flag to env - .env, .env.example, Heroku
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
    @app.route("/sqli2", methods=["GET", "POST"])
    def sqli2():
        error = None
        hints = [
            "As always, first try and use the system normally. Next, try and break it!",
            "Try entering a student ID that doesn't exist, nothing, or a single quote <code>'</code> into the student ID field. What does this tell us about the system?",
            (
                "We also know that when we enter a single quote, we get an error - so, the system may be vulnerable to SQL injection. "
                "However, unlike SQLI 1, simply selecting all rows won't suffice. "
                # "We can already do that by entering nothing (because of the ILIKE and wildcard %), but we can't see the flag. "
                "Where else could it be hidden?"
            ),
            (
                "Because of the way the server is configured, we can't simply end the query with a semicolon and start a new one. "
                "To get around this, you might find the <code>UNION</code> SQL operator helpful - it allows you to combine the results of two queries. "
                "</br></br>Also, most database management systems have a table that contains information about the database itself, like the names of tables."
                "</br></br>To save you some trial-and-error, this server is using sqlite3, which has a table called <a href='https://www.sqlite.org/schematab.html'>sqlite_master</a>. "
                "Try researching these concepts and see if you can find some information about table names."
                "</br></br>(Note: other DBMSs have similar tables, like <code>INFORMATION_SCHEMA.tables</code> and <code>INFORMATION_SCHEMA.columns</code> for MySQL)."
            ),
            (
                "Relevant columns of sqlite_master include <code>name</code> (the name of the table) and <code>sql</code> (the SQL used to create the table)."
                "</br></br>You can also use the value <code>1</code> in a SELECT statement as if it were a column - it will make a column with only 1's. "
                "This is handy because <code>UNION</code>s are only valid if the number of columns in both <code>SELECT</code> statements match."
                "</br></br>(In other DBMSs with strict typing, you might need to match the datatype to make the UNION valid "
                "- <code>NULL</code> works in most cases, but if the column is specifically <code>NOT NULL</code> you'll have to use e.g. <code>'a'</code> for a text column. "
                "You don't need that for this challenge though)"
            ),
            (
                "Try entering <code>1 UNION SELECT name,sql,1 FROM sqlite_master WHERE type='table'</code> into the student ID field. "
                "This will return the name and SQL used to create each table in the database, including information about columns. "
                # "The <code>1</code> will create a column with only 1's. This  to make the UNION valid - we need the same number of columns as the original query. "
            ),
            (
                "Now that you know the tables in the database and their columns, "
                "try using UNIONs to extract data from the tables to get the two flags. "
                "<br/><br/>I don't want to give too much away for this challenge, so good luck! "
                "Don't be afraid to Google things, like SQL UNION syntax!"
            )
            # Important concepts:
            #   - Padding with 1- or NULL-filled columns to make the UNION valid / get the same number of columns as the original query
            #   - UNION with sqlite_master to find table names
            #       Want to run something like SELECT * FROM sqlite_master WHERE type = 'table'
            #           (mention INFORMATION_SCHEMA.tables, INFORMATION_SCHEMA.columns for MySQL)
            #       1 UNION SELECT name, tbl_name, sql FROM sqlite_master WHERE type = 'table'
            #   - UNION with sqlite_master to find column names
            #   - UNION with table names
        ]
        res = None

        if request.method == "POST":
            student_id = request.form.get("student_id")

            # TODO clean up nesting hell
            try:
                with sqlite3.connect(app.config["SQLI2_DATABASE"]) as con:
                    # TODO decide if they should enter the zid, or the full name & get back email
                    res = execute(
                        con,
                        f"SELECT first_name, last_name, email FROM Students WHERE student_id = {student_id}",
                    )
            except Exception as e:
                # res will remain None
                print(e)

            # False = invalid query
            if res:
                # If res is populated with results, query is successful
                res = res.fetchall()
                if not res:
                    # No results for the query
                    error = "No students found"
            else:
                # Invalid query
                error = "<strong>Error!</strong> Invalid SQL query"

            print("res:", res)

        return render_template(
            "sqli2.html",
            heading="Student Lookup",
            chal_name="sqli2",
            task_desc="A benign student lookup system - you enter a student ID, and get back their name and email. What could go wrong? (Note: there are two flags in this challenge)",
            error=error,
            hints=hints,
            res=res,
        )

    # TODO add two flags to sqli2 (one in students, one in marks)

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
    init_sqli2_db(
        app.config["SQLI2_DATABASE"],
        app.config["SQLI2_SCHEMA"],
        app.config["SQLI2_DATA"],
    )

    return app


# To allow the project to be run manually from the command line
# (with python3 src/vulnerable_webapp_scorpiontornado/app.py)
if __name__ == "__main__":
    # TODO add support for passing test_config as a command line argument
    create_app().run()
