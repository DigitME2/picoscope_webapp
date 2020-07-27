from flask import Blueprint

bp = Blueprint('ps_interface', __name__)

# noinspection PyPep8
from app.ps_interface import routes