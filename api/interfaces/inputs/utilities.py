import numpy
import marshmallow


class FeaturesValuesValidator(object):
    """Class implementing validator for the feature values"""

    @classmethod
    def validate(cls, values):
        """
        Validates the feature values.

        :param values: values to be validated
        :type values: Any
        :return: validated values
        :rtype: Any
        """

        # Validate the feature values
        if values is None:
            raise marshmallow.ValidationError(f"Missing data for required field.", "features.values")
        if not isinstance(values, numpy.ndarray):
            raise marshmallow.ValidationError(f"Not a valid numpy.array.", "features.values")
        if values.size == 0:
            raise marshmallow.ValidationError(f"Empty numpy.array.", "features.values")

        # Return the validated feature values
        return values


class FeaturesLabelsValidator(object):
    """Class implementing validator for the feature labels"""

    @classmethod
    def validate(cls, labels, values):
        """
        Validates the feature labels.

        :param labels: labels to be validated
        :type labels: Any
        :param values: values to be referenced
        :type values: Any
        :return: validated values
        :rtype: Any
        """

        # Validate the feature labels
        if labels:
            if not isinstance(labels, (tuple, list)):
                raise marshmallow.ValidationError(f"Not a valid (tuple, list).", "features.labels")
            if not (len(labels) == values.shape[-1]):
                raise marshmallow.ValidationError(
                    f"Not a valid shape (must match the values). The API expects the same number of labels "
                    f"as the shape of the last dimension of the features (for more information, check the "
                    f"documentation or the docstring for the predictors resources (resources.<predictor>).",
                    "features.labels")

        # Return the validated feature labels
        return labels
