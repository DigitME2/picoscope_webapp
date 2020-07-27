import logging
import os


class Config(object):

    package_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(package_dir, 'app', 'test.db')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"
    SQLALCHEMY_ECHO = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or "yS7o2R64duQ"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.realpath(os.path.join('app', 'static', 'uploads'))

    if not os.path.exists('logs'):
        os.mkdir('logs')

    STREAM_LOGGING_LEVEL = logging.DEBUG
    FILE_LOGGING_LEVEL = logging.DEBUG
    FLASK_LOG_FILE = 'logs/oee_app.log'
    ROTATING_LOG_FILE_MAX_BYTES = 1024000
    ROTATING_LOG_FILE_COUNT = 10
    LOG_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

    # The database IDs for activity codes
    NO_USER_CODE_ID = 1
    UNEXPLAINED_DOWNTIME_CODE_ID = 2
    UPTIME_CODE_ID = 3  # Preferably 0 to keep it on the bottom of the graph
    SETTING_CODE_ID = 4

    MACHINE_STATE_OFF = 0
    MACHINE_STATE_RUNNING = 1
