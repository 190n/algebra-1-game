def create_module(app, **kwargs):
    from .controllers import assignment_blueprint
    app.register_blueprint(assignment_blueprint)
