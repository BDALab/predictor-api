from api.interfaces.inputs.schema import FeaturesSchema, PredictorModelSchema
from api.ml.manager import PredictorManager


# ----------------------------------- #
# Input features interface definition #
# ----------------------------------- #

class Features(object):
    """Class implementing the input features interface"""

    # Define the schema
    schema = FeaturesSchema()

    def __init__(self, values, labels):
        """Initializes the Features"""
        self.values = values
        self.labels = labels

    def __repr__(self):
        return str({"values": self.values, "labels": self.labels})

    def __str__(self):
        return repr(self)

    @classmethod
    def from_request(cls, request):
        """
        Creates the Features instance utilizing the schema.

        :param request: dict with the feature values and labels
        :type request: dict
        :return: class instance
        :rtype: api.interfaces.inputs.Features
        """
        return cls(**cls.schema.load(request))


# ------------------------------------------ #
# Input predictor model interface definition #
# ------------------------------------------ #

class PredictorModel(object):
    """Class implementing the input predictor model interface"""

    # Define the schema
    schema = PredictorModelSchema()

    def __init__(self, model):
        """Initializes the PredictorModel"""
        self.model = PredictorManager().load(model)

    def __repr__(self):
        return str({"model": self.model})

    def __str__(self):
        return repr(self)

    @classmethod
    def from_request(cls, request):
        """
        Creates the PredictorModel instance utilizing the schema.

        :param request: dict with the model identifier
        :type request: dict
        :return: class instance
        :rtype: api.interfaces.inputs.PredictorModel
        """
        return cls(**cls.schema.load(request))
