from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSON
from application import db
from flask.ext.security import Security, UserMixin

class reportSettings(db.Model):
    __tablename__ = 'report_settings'

    id = Column(Integer, primary_key=True)
    setting_name = Column(Integer, nullable=False)
    setting_value = Column(String(100), nullable=False)

    def __init__(self, setting_name, setting_value):
        self.setting_name = setting_name
        self.setting_value = setting_value
