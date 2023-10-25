# Something Awesome: Vulnerable Webapp
## https://nlangford-vulnerable-webapp-7f65a6cee144.herokuapp.com/

My UNSW COMP6841 Self-Selected Project - AKA "Something Awesome". I chose to complete this project on web security, creating an intentionally vulnerable web-app as a teaching tool.

The main problem I'm trying to solve is that when beginners are presented with a CTF (e.g. a plain login screen), they're often unsure as to how to begin. This project aims to dispel some of the mystery surrounding cybersecurity by guiding them through a few common web attacks, preparing them for traditional CTFs. My target market includes keen year 10 students (with exposure to web development / SQL - like my school's year 10 IST class), UNSW COMP3311 (databases) students, and potentially year 11/12 HSC Software Engineering students as an introduction to their new cybersecurity module. I hope to make the challenges accessible enough that even someone with a very limited technical background could complete some of them, but also provide room for students to challenge themselves.

The goal is to find "flags", pieces of text of the form `SAP{...}` (for Something Awesome Project). Each activity has hints that'll guide you through how to obtain the challenge's flag, or you can try it yourself without any help - it's up to you! The flags have been changed for the production server, so peeking at the source code won't help you much in that regard (although it might make the challenges easier in other ways).

Also, please don't be a jerk. This information is provided for informational purposes only, and you shouldn't attempt these methods (or any other attack) on a system you don't have explicit written permission to break. Feel free to try and break this webapp however you want though! If you do it in an unexpected way, let me know!

### (Intentional) Vulnerabilities
- Basic SQLI

### Planned (to do in future)

- Moderate SQLI - blacklists (find/replace once), perhaps one field with a parameterised input but not the other, etc.
- XSS (stored, reflected)
- Advanced SQLI - multiple tables, UNION, blind, time-based (might be hard to implement), MySQL?
- IDOR
- SSRF (& potentially CSRF)
- Authentication vulnerabilities involving cookies (logout, but not invalidated. Cookie expired but can change it, cookie has with sever key but not validated)
- LFI

Other ideas - OWASP Top 10, DVWA, UNSW's COMP6843 content.

## Usage

See below for detailed steps

1. Install python3 and pip
2. Clone the repo
3. Set up a virtual environment (see below)
4. Run the Flask server with `gunicorn 'vulnerable_webapp_scorpiontornado:create_app()'` (see "Development")
5. Navigate to the URL given in the terminal.
   - By default, it should be http://127.0.0.1:8000 (or perhaps http://127.0.0.1:5000). Simply open this URL in your preferred browser.

### Setting up a virtual environment

First clone the repo by navigating to the place where you want the new folder to be created in a terminal emulator, then running:

```
git clone https://github.com/scorpiontornado/Something-Awesome.git
cd Something-Awesome
```

Next, set up the virtual environment. The first time you do this, run the following to create and activate a new virtual environment and install the necessary packages:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

After the first time - run the following to activate the virtual environment:

```
source .venv/bin/activate
```

### Development
The simplest way to run the server is with `python3 vulnerable_webapp_scorpiontornado/app.py`. This will run the app locally using Flask's built-in server. To run with debugging enabled (the primary feature of which is the auto-server-restart on save), run:
```
flask --app vulnerable_webapp_scorpiontornado/app run --debug
```
(Note: only use debug mode for development. Leaving it on will allow users to run arbitrary Python code on your server.)

The Flask built-in server is fine for personal use, but it's not suitable for production. From the [Flask docs](https://flask.palletsprojects.com/en/2.3.x/deploying/):
> “Production” means “not development”, which applies whether you’re serving your application publicly to millions of users or privately / locally to a single user. Do not use the development server when deploying to production. It is intended for use only during local development. It is not designed to be particularly secure, stable, or efficient.
Instead, you should use a dedicated WSGI server or hosting platform. Currently, Gunicorn is fully set up. Just run:
```
gunicorn 'vulnerable_webapp_scorpiontornado:create_app()'
```
By default, the number of gunicorn worker processes is 1. This works fine when you only have one user, but for running a server with multiple concurrent users you should increase this - Heroku recommends 2-4 for a typical project. See [.env.example](.env.example) for more info.

If you want to learn more about deployment with Flask, check out these pages:
- [Flask docs - Deployment Options](https://flask.palletsprojects.com/en/2.3.x/deploying/) (see [here](https://packaging.python.org/en/latest/tutorials/packaging-projects/) for more info about Python packages)
- [Flask docs tutorial - Deploy to Production](https://flask.palletsprojects.com/en/2.3.x/tutorial/deploy/) - especially the "Build and Install" section
  - Prereqs:
    - [Flask docs tutorial - Project Layout](https://flask.palletsprojects.com/en/3.0.x/tutorial/layout/) ((already done))
    - [Flask docs tutorial - Application Setup](https://flask.palletsprojects.com/en/3.0.x/tutorial/factory/)
- [Flask docs - Gunicorn](https://flask.palletsprojects.com/en/2.3.x/deploying/gunicorn/)
- [Heroku - Deploying Python Applications with Gunicorn](https://devcenter.heroku.com/articles/python-gunicorn)
- [Getting Started on Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python)
	- (And other Heroku articles - procfile, pipelines, github integration, config vars)
	- [Heroku for GitHub Students](https://www.heroku.com/github-students)
	- [Preparing a Codebase for Heroku Deployment](https://devcenter.heroku.com/articles/preparing-a-codebase-for-heroku-deployment)

To build the project (to deploy elsewhere, put on [PyPI](https://pypi.org/), etc.), run `python -m build` or `python -m build --wheel` and follow the PyPI instructions.
See [SetupTools docs](https://setuptools.pypa.io/en/latest/userguide/quickstart.html) and [this Flask docs page](https://flask.palletsprojects.com/en/2.3.x/tutorial/deploy/) for more info on both. I'm not entirely sure why you'd use one or the other, but they seem to do roughly the same thing. For info about publishing to [PyPI](https://pypi.org/), see [here](https://twine.readthedocs.io/en/stable/index.html).

## Main sources of inspiration

- Initial inspiration - [DVWA](https://github.com/digininja/DVWA)
- [Inspiration for practical lesson / prevention format](https://www.hacksplaining.com/exercises/sql-injection)
- [Repo](https://github.com/realsidg/sqlInjection) used to help implement Flask / SQLite3 for SQLI and XSS
- Some challenge ideas from [COMP6841 wargames](https://comp6841.quoccabank.com/challenges)

### SQLI1
Challenges:
- https://github.com/realsidg/sqlInjection/blob/master/main.py
- COMP6841 Quoccabank sqli2.py

Code:
- https://flask.palletsprojects.com/en/3.0.x/quickstart/#sessions
- https://docs.python.org/3/library/sqlite3.html
- And Flask docs (esp. the tutorial), Bootstrap docs, Bootstrap-Flask docs (not to be confused with Flask-Bootstrap, which is BS3 not BS5), Heroku docs, and wayyy to many StackOverflow questions.
