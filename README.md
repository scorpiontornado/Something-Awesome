# Something-Awesome

My UNSW COMP6841 Self-Selected Project - AKA "Something Awesome". I chose to complete this project on web security, creating an intentionally vulnerable web-app as a teaching tool.

Flags are of the form `SAP{...}` (for Something Awesome Project). Please don't cheat and look at the hardcoded values (of the flags, database create/insert statements etc). Later iterations would somehow redact this or move to a different file to make it less easy to cheat.

### (Intentional) Vulnerabilities

- Basic SQLI (work in progress)

### Planned (to do in future)

- XSS (stored, reflected)
- Advanced SQLI - multiple tables, UNION, blind, time-based (might be hard to implement), MySQL?
- IDOR
- SSRF (& potentially CSRF)
- Authentication vulnerabilities involving cookies (logout, but not invalidated. Cookie expired but can change it, cookie has with sever key but not validated)
- LFI

Other ideas - OWASP Top 10, DVWA, UNSW's COMP6841 content.

## Usage

See below for detailed steps

1. Install python3 and pip
2. Clone the repo
3. Set up a virtual environment (see below)
4. Run the Flask server with `python3 main.py`
5. Navigate to the URL given in the terminal.
   - By default, it should be http://127.0.0.1:5000. Simply open this URL in your preferred browser.

### Setting up a virtual environment

First clone the repo by navigating to the place where you want the new folder to be created in a terminal emulator, then running:

```
git clone https://github.com/scorpiontornado/Something-Awesome.git
cd Something-Awesome
```

Next, set up the virtual environment. The first time you do this, run the following to create and activate a new virtual environment and install the necessary packages:

```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

After the first time - run the following to activate the virtual environment:

```
. venv/bin/activate
```

## Main sources of inspiration

- Initial inspiration - [DVWA](https://github.com/digininja/DVWA)
- [Inspiration for practical lesson / prevention format](https://www.hacksplaining.com/exercises/sql-injection)
- [Repo](https://github.com/realsidg/sqlInjection) used to help implement Flask / SQLite3 for SQLI and XSS
- Some challenge ideas from [COMP6841 wargames](https://comp6841.quoccabank.com/challenges)

### SQLI1

- https://flask.palletsprojects.com/en/3.0.x/quickstart/#sessions
- https://github.com/realsidg/sqlInjection/blob/master/main.py
- COMP6841 Quoccabank sqli2.py
- https://docs.python.org/3/library/sqlite3.html
