from vulnerable_webapp_scorpiontornado.db import execute
import sqlite3


# Modified from 6841 Quoccabank SQLI2. Returns:
# - False on error (usually invalid query)
# - None when there are no results for the query (i.e., no rows with the given username/password)
# - The username of the first row to fulfill the condition (matching username/password)
# Currently only used for sqli1.
def insecure_login(username, password, db_path):
    # "with" will auto-close the connection
    # TODO what if error while connecting? Might just get rid of the execute function tbh
    with sqlite3.connect(db_path) as con:
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
        # res is either a sqlite3.Cursor object if the query was valid, else None

        return res.fetchone() if res else False
