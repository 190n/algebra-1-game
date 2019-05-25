from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def page_not_found(error):
    return render_template('404.html'), 404

def create_app(object_name):
    from . import assignment, auth, student, main, teacher

    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    migrate.init_app(app, db)
    main.create_module(app)
    auth.create_module(app)
    assignment.create_module(app)
    student.create_module(app)
    teacher.create_module(app)
    app.register_error_handler(404, page_not_found)
    return app
