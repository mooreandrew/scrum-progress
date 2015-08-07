import os

class Config(object):
    DEBUG = False
    LOGGING_PATH = os.getenv('LOGGING_PATH', 'python_logging/logging.yaml')
    SECRET_KEY = os.environ['SECRET_KEY']

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://scrum-progress:scrum-progress@localhost/scrum-progress'
    DEBUG = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI','')
    DEBUG = True
