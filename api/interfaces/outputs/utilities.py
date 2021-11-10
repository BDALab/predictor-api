import numpy
import marshmallow


class PredictedValuesValidator(object):
    """Class implementing validator for the predicted values"""

    @classmethod
    def validate(cls, values):
        """
        Validates the predicted values.

        :param values: values to be validated
        :type values: Any
        :return: validated values
        :rtype: Any
        """

        # Validate the predicted values
        if values is None:
            raise marshmallow.ValidationError(f"Missing data for required field.", "predicted.values")
        if not isinstance(values, numpy.ndarray):
            raise marshmallow.ValidationError(f"Not a valid numpy.array.", "predicted.values")

        # Return the validated predicted values
        return values
