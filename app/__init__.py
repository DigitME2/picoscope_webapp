import logging
import os
from logging.handlers import RotatingFileHandler
from time import strftime

from flask import Flask, request
from flask.logging import default_handler
from flask_login import LoginManager
from flask_login import user_logged_out
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config

# Set up logging handlers
if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler(filename=Config.FLASK_LOG_FILE,
                                   maxBytes=Config.ROTATING_LOG_FILE_MAX_BYTES,
                                   backupCount=Config.ROTATING_LOG_FILE_COUNT)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s'))
stream_handler = logging.StreamHandler()

stream_handler.setLevel(Config.STREAM_LOGGING_LEVEL)
file_handler.setLevel(Config.FILE_LOGGING_LEVEL)

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login.login'


def create_app(config_class=Config):
    app = Flask(__name__)

    # Set up logger
    app.logger.setLevel(logging.DEBUG)
    app.logger.removeHandler(default_handler)
    app.logger.addHandler(stream_handler)
    app.logger.addHandler(file_handler)

    # Add gunicorn logger
    gunicorn_logger = logging.getLogger('gunicorn.error')
    for handler in gunicorn_logger.handlers:
        app.logger.addHandler(handler)

    print("Logging level:", logging.getLevelName(app.logger.getEffectiveLevel()))

    app.config.from_object(config_class)
    db.init_app(app)

    login_manager.init_app(app)

    # To get client IP when using a proxy
    # This requires the following line in nginx config:
    # proxy_set_header   X-Real-IP            $remote_addr;
    app.wsgi_app = ProxyFix(app.wsgi_app)

    from app.default import bp as default_bp
    from app.login import bp as login_bp
    from app.errors import bp as errors_bp
    from app.ps_interface import bp as ps_interface_bp

    app.register_blueprint(default_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(ps_interface_bp)

    @app.before_first_request
    def initial_setup():
        # Fill the database with default values
        with app.app_context():
            from app.setup_database import setup_database
            setup_database()


    # Function to log requests
    @app.before_request
    def before_request():
        timestamp = strftime('[%Y-%b-%d %H:%M]')
        app.logger.debug(f'{timestamp}, {request.remote_addr}, {request.method}, {request.scheme}, {request.full_path}')

    return app
