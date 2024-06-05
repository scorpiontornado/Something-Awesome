# Something Awesome (AKA Vulnerable Webapp, nlangford-vulnerable-webapp or nlangford-sqli)
# An intentionally vulnerable web-app, as a teaching tool for cybersecurity.
# Copyright (C) 2024  Nicholas Langford
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


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
