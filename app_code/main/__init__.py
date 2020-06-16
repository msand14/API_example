from flask import Blueprint

main = Blueprint('main',__name__)
# the next module importation are in this order to avoid circular dependencies failure.
from . import views, errors