from flask import Flask
from .config import Config
from .extensions import db, migrate
from .routes.main import main_bp
from .routes.categories import categories_bp
from .routes.activities import activities_bp
from .routes.logs import logs_bp
from .routes.import_export import import_export_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(categories_bp, url_prefix="/categories")
    app.register_blueprint(activities_bp, url_prefix="/activities")
    app.register_blueprint(logs_bp, url_prefix="/logs")
    app.register_blueprint(import_export_bp, url_prefix="/data")


    return app
