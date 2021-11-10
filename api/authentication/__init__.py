from flask_bcrypt import Bcrypt
from api.configuration import load_configuration
from api.authentication.database import initialize_database


# ------------------------------------------------ #
# Authentication configuration routines definition #
# ------------------------------------------------ #

def configure_authentication(app):
    """Configures the authentication"""

    # Initialize the encryption object
    Bcrypt(app)

    # Configure the authentication database
    for key, value in load_configuration("authentication.json").get("database", {}).items():
        app.config[key] = value

    # Initialize the authentication database
    initialize_database(app)
