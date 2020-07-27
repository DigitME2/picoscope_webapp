import logging

from app import db

logger = logging.getLogger('flask.app')


class ReadingSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    start = db.Column(db.DateTime)
    block_duration = db.Column(db.Float)
    requested_sampling_interval = db.Column(db.Float)
    actual_sampling_interval = db.Column(db.Float)
    samples_number = db.Column(db.Float)
    maximum_samples = db.Column(db.Float)
    coupling = db.Column(db.String)
    v_range = db.Column(db.Float)
    v_offset = db.Column(db.Float)

    readings = db.relationship("Reading", backref="set")


class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    set_id = db.Column(db.Integer, db.ForeignKey("reading_set.id"))
    value = db.Column(db.Integer, nullable=False)
    time_delta = db.Column(db.Integer, nullable=False)


class Settings(db.Model):
    # Only allow one row in this table
    unique = db.Column(db.String, db.CheckConstraint('1'), primary_key=True, default="1")



