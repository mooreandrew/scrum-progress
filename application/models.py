from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSON
from application import db
from flask.ext.security import Security, UserMixin

class projects(db.Model):
    __tablename__ = 'report_settings'

    id = Column(Integer, primary_key=True)
    project_url = Column(String(100), nullable=False)
    project_name = Column(String(100), nullable=False)
    collaboration_tool = Column(String(100), nullable=False)
    collaboration_project_name = Column(String(100), nullable=False)
    start_sprint = Column(Integer, nullable=False)
    start_day = Column(Integer, nullable=False)
    start_month = Column(Integer, nullable=False)
    start_year = Column(Integer, nullable=False)

    def __init__(self, project_url, project_name, collaboration_tool, collaboration_project_name, start_sprint, start_day, start_month, start_year):
        self.project_url = project_url
        self.project_name = project_name
        self.collaboration_tool = collaboration_tool
        self.collaboration_project_name = collaboration_project_name
        self.start_sprint = start_sprint
        self.start_day = start_day
        self.start_month = start_month
        self.start_year = start_year
