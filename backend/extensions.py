from flask_sqlalchemy import SQLAlchemy
from flask_security.core import Security
from flask_mail import Mail
from flask_caching import Cache
from celery import Celery

db = SQLAlchemy()
security = Security()
mail = Mail()
cache = Cache()
celery = Celery()
