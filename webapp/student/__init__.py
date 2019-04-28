def create_module(app, **kwargs):
    from .controllers import student_blueprint
    app.register_blueprint(student_blueprint)
