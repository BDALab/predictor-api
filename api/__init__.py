import sys
import subprocess
import importlib
import warnings
from flask import Flask
from api.common.base import Api
from api.common.errors import register_errors
from api.common.logging import configure_logging
from api.cors import configure_cors
from api.authentication import configure_authentication
from api.authorization import configure_authorization
from api.resources import configure_routes


# Filter out unnecessary warning messages
warnings.filterwarnings("ignore", category=UserWarning)


def prepare_app(app_name):
    """Prepares the application"""

    # Initialize the Flask object
    app = Flask(app_name)

    # Initialize the cross origin resource sharing object
    configure_cors(app)

    # Configure the logging and error-handling
    configure_logging(app)
    register_errors(app)

    # Configure the authentication and authorization
    configure_authentication(app)
    configure_authorization(app)

    # Prepare the API
    prepare_api(app)

    # Return the app
    return app


def prepare_api(app):
    """Prepares the API"""

    # Initialize the Flask-RestFul object
    api = Api(app)

    # Register the routes
    configure_routes(api)

    # Install the predictor dependencies
    install_predictor_dependencies()


def install_predictor_dependencies():
    """Installs the predictor dependencies"""

    # Install the predictor dependencies
    with open("requirements_predictors.txt", "rt") as file:
        for dependency in file.readlines():
            try:
                importlib.import_module(dependency)
            except ImportError:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dependency])
