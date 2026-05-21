from flask import Blueprint

routes_bp = Blueprint('routes', __name__)

from .upload import *
from .query import *