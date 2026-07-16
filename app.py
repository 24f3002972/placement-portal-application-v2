from flask import Flask
from backend.config import LocalDevelopmentConfig
from dotenv import load_dotenv
from backend.resources import auth_bp, api, api_bp
from flask_cors import CORS
from backend.extensions import security, celery, mail, cache

def create_app():
    from backend.celery_app import celery_init_app
    from backend.extensions import celery
    app = Flask(__name__)
    # load environment variable from .env
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True, allow_headers=["Content-Type", "Authentication-Token"])
    # config
    app.config.from_object(LocalDevelopmentConfig)

    # connection for flask with flask_sqlalchemy
    from backend.models import db, User, Role
    db.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    celery_init_app(app, celery)
    # flask security stuff
    from flask_security.datastore import SQLAlchemyUserDatastore
    from backend.extensions import security
    datastore = SQLAlchemyUserDatastore(db, User, Role )
    security.init_app(app, datastore = datastore, ) #register_blueprint=False

    app.datastore = datastore

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    api.init_app(app)
    return app

app = create_app()
if __name__ == "__main__":
    app.run()
