import marshmallow
from api.interfaces.inputs.utilities import FeaturesValuesValidator, FeaturesLabelsValidator
from api.wrappers.data import *


# ------------------------------------------ #
# Input features interface schema definition #
# ------------------------------------------ #

class FeaturesSchema(marshmallow.Schema):
    """Class defining the schema for the feature input interface"""

    # Define the meta attributes
    class Meta:
        unknown = marshmallow.EXCLUDE

    # Define the schema attributes
    values = marshmallow.fields.Str(required=True)
    labels = marshmallow.fields.List(marshmallow.fields.String, missing=[])

    @marshmallow.pre_load
    def _pre_load(self, data, **kwargs):
        """Handles the pre-loading data preparation and validation"""

        # Handle the feature field
        if not data.get("features"):
            raise marshmallow.ValidationError("Missing data for required field.", "features")
        if not isinstance(data.get("features"), dict):
            raise marshmallow.ValidationError("Not a valid dict.", "features")

        # Return the output data
        return data.get("features")

    @marshmallow.post_load
    def _post_load(self, data, **kwargs):
        """Handles the post-loading data preparation and validation"""

        # Get the attributes
        values = DataWrapper.unwrap_data(data["values"])
        labels = data["labels"] or []

        # Handle the feature values/labels
        values = FeaturesValuesValidator.validate(values)
        labels = FeaturesLabelsValidator.validate(labels, values)

        # Return the output data
        return {"values": values, "labels": labels}


# ------------------------------------------- #
# Input predictor interface schema definition #
# ------------------------------------------- #

class PredictorModelSchema(marshmallow.Schema):
    """Class defining the schema for the predictor model input interface"""

    # Define the meta attributes
    class Meta:
        unknown = marshmallow.EXCLUDE

    # Define the schema attributes
    model = marshmallow.fields.Str(required=True)
