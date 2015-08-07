from application.models import reportSettings
from application import app, db

from flask import request, render_template, request, redirect, url_for, session, flash
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta


@app.route('/')
def login():
    return 'ok'


@app.route('/template')
def test():
   return render_template('test.html',
        helloworld='hello world',
        asset_path='/static/'
    )
