import os
import glob
import ntpath
import joblib
from api.ml import configure_machine_learning
from api.ml.interface import Predictor


# ---------------------------------------- #
# Predictor-specific exceptions definition #
# ---------------------------------------- #
class NoLoadablePredictorException(Exception): pass


# ---------------------------- #
# Predictor manager definition #
# ---------------------------- #

class PredictorManager(object):
    """Class implementing the predictor manager"""

    # Supported serialization
    extension = "joblib"

    def load(self, model_identifier):
        """Loads the predictor model and returns the interface instance"""

        # Get the configuration
        configuration = configure_machine_learning()

        # Get the models location
        location = configuration["location"]

        # Load the model
        if model_identifier not in self.available_models(location):
            raise NoLoadablePredictorException(f"Model with identifier '{model_identifier}' cannot be loaded")
        with open(os.path.join(location, f"{model_identifier}.{self.extension}"), "rb") as file:
            return Predictor(joblib.load(file))

    def available_models(self, models_path):
        """Lists the models that are available"""
        return [
            os.path.splitext(ntpath.basename(f))[0]
            for f in glob.glob(f"{models_path}**/*.{self.extension}")
        ]
