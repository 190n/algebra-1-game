algebra-1-game
==============

Math game for Algebra 1 students. Early WIP.

Built in Python 3 with Flask, SQLAlchemy, Flask-Login, WTForms.

Running
-------

Set up and enter virtual environment:

```bash
$ virtualenv -p $(which python3) venv
$ source venv/bin/activate
```

Install dependencies:

```bash
(venv) $ pip3 install -r requirements.txt
```

Tell Flask where to find the app and run it:

```bash
(venv) $ export FLASK_APP=main.py
(venv) $ flask run
```

This will make the website available at `http://localhost:5000/`.
