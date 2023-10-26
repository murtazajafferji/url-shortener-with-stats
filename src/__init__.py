from flask import Flask
from .routes import routes
from flask_limiter import Limiter, RequestLimit
from flask_limiter.util import get_remote_address

def init_app():
    """Initialize the Flask application.

    Returns:
        Flask: The Flask application object
    """
    application = Flask(__name__)

    # Rate limiting
    # https://flask-limiter.readthedocs.io/en/latest/recipes.html#rate-limiting-all-routes-in-a-blueprint
    limiter = Limiter(get_remote_address, app=application, default_limits = ["1/second"], storage_uri="memory://")
    limiter.limit("60/hour")(routes) # TODO: Load from configuration

    application.register_blueprint(routes)

    return application

app = init_app()
