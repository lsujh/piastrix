import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap


db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)
    app_settings = os.getenv('FLASK_ENV', 'config.Config')
    app.config.from_object(app_settings)
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
