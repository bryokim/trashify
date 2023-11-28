"""Core Blueprints"""

from flask import Blueprint

core_view = Blueprint("core_view", __name__)

from .status import *
from .users import *
