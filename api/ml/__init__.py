import os
from pathlib import Path
from api.configuration import load_configuration


# -------------------------------------------------- #
# Machine learning configuration routines definition #
# -------------------------------------------------- #

def configure_machine_learning():
    """Configures the machine learning"""

    # Get the configuration
    configuration = load_configuration("ml.json")["predictors"]

    # Get the location of the models
    models_location = configuration.get("location")
    models_location = models_location or os.path.join(os.path.dirname(os.path.realpath(__file__)), "models")

    # Make sure the location of the models exists
    Path(models_location).mkdir(parents=True, exist_ok=True)

    # Return the configuration
    return {"location": models_location}
