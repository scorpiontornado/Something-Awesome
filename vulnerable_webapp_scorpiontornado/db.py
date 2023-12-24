import sqlite3


### Database code
def init_sqli1_db(db_path):
    print("Connecting to database...")

    try:
        con = sqlite3.connect(db_path)  # Will create db if doesn't exist

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
        # )  # TESTING - should return: test ('admin',)
    except Exception as e:
        print("Error creating SQLI 1 database:", e)
        # If connection was made, rollback changes (otherwise, con won't have a value)
        if con:
            con.rollback()
    finally:
        if con:
            con.close()


def init_sqli2_db(db_path, schema_path, data_path):
    # try:
    con = sqlite3.connect(db_path)  # Will create db if doesn't exist
    cur = con.cursor()

    # TODO insert flags from env variables (one in Students, one in Marks)
    with open(schema_path) as schema_file:
        schema = schema_file.read()
        cur.executescript(schema)
    with open(data_path) as data:
        cur.executescript(data.read())

    con.commit()

    # except Exception as e:
    #     print("Error creating SQLI 2 database:", e)
    #     # If connection was made, rollback changes (otherwise, con won't have a value)
    #     if con:
    #         con.rollback()

    # finally:
    #     if con:
    #         con.close()


# TODO init SQLI 3 db


def execute(con, query, parameters=()):
    # Moved database connection outside, as fetchone() is a Cursor method & Cursors close when their
    # parent connection does. Not closing would slow down the system over time.
    cur = con.cursor()

    try:
        # Note - cur.execute() just returns the same cursor, cur, if it succeeds, so this is a bit redundant
        res = cur.execute(query, parameters)
    except Exception as e:
        # Invalid SQL query
        # Could instead have a route for internal server error
        print(e)
        res = None

    return res
