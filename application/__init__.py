from flask import Flask, request
import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object(os.environ.get('SETTINGS'))

login_manager = LoginManager()
login_manager.init_app(app)
