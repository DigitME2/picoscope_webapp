import os
from datetime import datetime, time

from flask import current_app

from app import db
from app.login.models import create_default_users
from config import Config


def setup_database():

    """ Enter default values into the database on its first run"""
    db.create_all()
    create_default_users()
