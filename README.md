# Something-Awesome

My UNSW COMP6841 Self-Selected Project - AKA "Something Awesome". I chose to complete this project on web security, creating an intentionally vulnerable web-app as a teaching tool.

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
   - By default, it should be http://localhost:5000/. Simply open this URL in your preferred browser.

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
