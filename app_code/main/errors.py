from flask import render_template
from . import main

# It's neccesary to use app_error_handler instead of error_handler to use this funcitons
# not only in a Blueprint Domain
@main.app_errorhandler(404)
def page_not_found(err):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_error(err):
    return render_template('500.html'), 500