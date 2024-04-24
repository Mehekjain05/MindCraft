from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from server.config import config
from flask_cors import CORS
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(config_class=config):
    app = Flask(__name__)

    app.config.from_object(config_class)
    app.json.sort_keys = False
    CORS(app, supports_credentials=True)

    db.init_app(app)
    bcrypt.init_app(app)
    migrate = Migrate(app, db)

    from server.users.routes import users

    # Register the blueprint
    app.register_blueprint(users)

    return app
