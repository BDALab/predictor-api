from api.interfaces.outputs.schema import PredictionsSchema


# -------------------------------------- #
# Output prediction interface definition #
# -------------------------------------- #

class Predictions(object):
    """Class implementing the output predictions interface"""

    # Define the schema
    schema = PredictionsSchema()

    def __init__(self, predicted):
        """Initializes the Predictions"""
        self.predicted = predicted

    def __repr__(self):
        return str({"predicted": self.predicted})

    def __str__(self):
        return repr(self)

    def to_response(self):
        """Dumps the predictions to the data to be used in the response"""
        return self.schema.dump(self)
