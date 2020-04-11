from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'dem3_multi.sqlite'),
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import data

    from . import auth
    app.register_blueprint(auth.bp)

    from . import admin
    app.register_blueprint(admin.bp)

    from . import dem3
    app.register_blueprint(dem3.bp)

    return app
