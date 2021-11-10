# ------------------------------ #
# Predictor interface definition #
# ------------------------------ #

class Predictor(object):
    """Class implementing the predictor interface"""

    def __init__(self, model):
        """Initializes the Predictor"""
        self.model = model

    def predict(self, features):
        """
        Predicts the class(/es).

        :param features: features
        :type features: api.interfaces.inputs.Features
        :return: predicted value(s)
        :rtype: numpy.ndarray
        """
        return self.model.predict(features.values)

    def predict_proba(self, features):
        """
        Predicts the probability of the <features> belonging to the class(/es).

        :param features: features
        :type features: api.interfaces.inputs.Features
        :return: predicted probabilit(y/ies)
        :rtype: numpy.ndarray
        """
        return self.model.predict_proba(features.values)
