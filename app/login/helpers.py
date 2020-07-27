from datetime import datetime

from flask import current_app


from app import db
from app.login.models import UserSession
from config import Config


def start_user_session(user_id, device_ip):
    """ Start a new session. Usually called when a user logs in"""
    timestamp = datetime.now().timestamp()
    user_session = UserSession.query.filter_by(user_id=user_id, device_ip=device_ip, active=True).first()
    # Close any user sessions that the current user has
    if user_session is not None:
        current_app.logger.warning(
            f"Tried to start a user session for user {user_id} while one is already open. Closing...")
        end_user_sessions(user_id)

    # Create the new user session
    new_us = UserSession(user_id=user_id,
                         device_ip=device_ip,
                         timestamp_login=timestamp,
                         active=True)
    db.session.add(new_us)
    db.session.commit()
    current_app.logger.info(f"Started user session {new_us}")
    return True


def end_user_sessions(user_id):
    """ End all sessions for a user"""
    timestamp = datetime.now().timestamp()
    sessions = []
    if user_id:
        sessions.extend(UserSession.query.filter_by(user_id=user_id, active=True).all())
    else:
        return
    for us in sessions:
        current_app.logger.info(f"Ending user session {us}")
        us.timestamp_logout = timestamp
        us.active = False
        # End all jobs assigned to the session
        for job in us.jobs:
            job.end_time = timestamp
            job.active = None
        db.session.commit()
