from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Tell our Flask application to use SQLAlchemy and Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    from app.blueprints.blog import bp as blog
    app.register_blueprint(blog)

    from app.blueprints.main import bp as main
    app.register_blueprint(main)

    from app.blueprints.shop import bp as shop
    app.register_blueprint(shop)

    from app.blueprints.authentication import bp as authentication
    app.register_blueprint(authentication)

    with app.app_context():
        # build rest of the flask app (configurations, additional packages, etc.)
        pass

    return app