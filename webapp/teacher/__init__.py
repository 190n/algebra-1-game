def create_module(app, **kwargs):
    from .controllers import teacher_blueprint
    app.register_blueprint(teacher_blueprint)
