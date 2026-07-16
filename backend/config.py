import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class LocalDevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'database.sqlite3')}"
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
    SECURITY_PASSWORD_HASH = "argon2"
    CELERY = {
    "broker_url": "redis://127.0.0.1:6379/0",
    "result_backend": "redis://127.0.0.1:6379/0",
    "task_ignore_result": False,
    }
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "24f3002972@ds.study.iitm.ac.in"
    MAIL_PASSWORD = "ndpx aexs jcdm nese"
    MAIL_DEFAULT_SENDER = "24f3002972@ds.study.iitm.ac.in"
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "127.0.0.1"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 1
    CACHE_DEFAULT_TIMEOUT = 300


class ProductionConfig(BaseConfig):
    DEBUG = False
