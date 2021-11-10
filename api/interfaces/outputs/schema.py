import numpy
import marshmallow
from api.interfaces.outputs.utilities import PredictedValuesValidator
from api.wrappers.data import *


# --------------------------------------- #
# Output predictions interface definition #
# --------------------------------------- #

class PredictionsSchema(marshmallow.Schema):
    """Class defining the schema for the predictions output interface"""

    # Define the meta attributes
    class Meta:
        unknown = marshmallow.EXCLUDE

    # Define the schema attributes
    predicted = marshmallow.fields.Str(required=True)

    @marshmallow.pre_dump
    def _pre_dump(self, instance, **kwargs):
        """Handles the pre-dumping data preparation and validation"""

        # Validate the predictions
        if not isinstance(instance.predicted, numpy.ndarray):
            raise marshmallow.ValidationError("Not a valid numpy.array.", "predicted.values")

        # Handle the predictions
        instance.predicted = DataWrapper.wrap_data(PredictedValuesValidator.validate(instance.predicted))

        # Return the output data
        return {"predicted": instance.predicted}
