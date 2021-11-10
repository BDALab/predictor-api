import flask
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_api_cache import ApiCache
from http import HTTPStatus
from api.wrappers.request import RequestWrapper
from api.wrappers.response import ResponseWrapper
from api.interfaces.inputs.interface import Features, PredictorModel
from api.interfaces.outputs.interface import Predictions
from api.resources.base import LoggableResource, CacheableResource


# ------------------------------------------ #
# Predict class(/es) API Resource definition #
# ------------------------------------------ #

class PredictClassesResource(Resource, LoggableResource, CacheableResource):
    """Class implementing the predict classes API resource (controller)"""

    @jwt_required()
    @ApiCache(expired_time=CacheableResource.CACHE_EXPIRATION_TIME)
    def post(self):
        """
        Predicts the class(/es) for 1-M subjects.

        The method expects the JSON-serialized data in the body of the request
        that contains all information that is needed for the prediction. The
        information needed comprise: a) features to be fed into a predictor, b)
        predictor identifier used to load and instantiate the predictor model.
        More information about the structure of the data can be seen bellow.

        The prediction can be secured by the auth JWT token. If the method is
        decorated with ``@jwt_required()``, every request must be authorized by
        the JWT token that an authenticated user obtained via the ``/signup``
        and ``/login`` API calls. For more information, see:
        ``api.resources.security.py``.

        **Input data**

        Structure of the input data is the following: it is a ``dict`` object
        with these field-value pairs (example bellow):

        - ``features`` (``dict``, mandatory)
        - ``features.values`` (``np.array``, mandatory)
        - ``features.labels`` (``list``, optional)
        - ``model`` (``str``, mandatory)

        .. code-block:: python

            # Example: 10 subjects, each having 5 2-D features (shape: (2, 5))
            {
                "features": {
                    "labels": ["feature 1", ... "feature 5"],
                    "values": np.array((10, 2, 5))
                },
                "model": "model_identifier"
            }

        It can be seen that the feature values can be multi-dimensional. The
        logic is that the last dimension of the N-dimensional feature values
        array for a particular subject stands for the number of features in the
        array. E.g. in the case of 1-D data (N 1-D features), it can be
        ``(1, N)`` or ``(N,)``, in the case of 2-D data (N 2-D features), it
        is ``(2, N)``, etc.

        As the feature values are stored in a ``np.array``, they must be
        serialized before sending in the request. The predictor API expects the
        features to be JSON-serialized using a lightweight serialization library
        `json-tricks <https://json-tricks.readthedocs.io/en/latest/>`_. The API
        package also provides ``api.wrapper.data.DataWrapper.wrap_data``
        for serialization.

        **Output data**

        Structure of the output data is the following: it is a ``dict`` object
        with these field-value pairs (example bellow): ``predicted``
        (``np.array``, mandatory)

        .. code-block:: python

            # Example: 10 subjects, 1 predicted value
            {
                "predicted": np.array((10, 1))
            }

        The output predicted values in the response object are JSON-serialized
        in the same way as the features. So, to get the predicted ``np.array``,
        the deserialization must be performed after the response is obtained
        (``api.wrapper.data.DataWrapper.unwrap_data``; see the example bellow).

        **Workflow**

        1. Unwrap the input request
        2. Prepare and validate the features
        3. Prepare and validate the predictor based on the model identifier
        4. Predict the class(/es) for the features
        5. Prepare and validate the prediction(s)
        6. Wrap the output response
        7. Send the successful HTTP Response

        **Example**

        .. code-block:: python

            import numpy
            import requests
            from pprint import pprint
            from api.wrappers.data import DataWrapper

            # Prepare the features (example: 10 subjects, each 100 1-D features)
            features = numpy.random.rand(10, *(1, 100))

            # Serialize the features
            features = DataWrapper.wrap_data(features)

            # Prepare the model identifier (example: unreal identifier)
            model = "model"

            # Prepare the predictor data
            body = {
                "model": model,
                "features": {
                    "values": features
                }
            }

            # Prepare the authorization header (example: unreal JWT token)
            headers = {
                "Authorization": f"Bearer 123456789"
            }

            # Call the predict endpoint (example: locally deployed API)
            response = requests.post(
                url="http://localhost:5000/predict",
                json=body,
                headers=headers,
                verify=True,
                timeout=10)

            # Get the predictions
            predicted = response.json().get("predicted")

            # Deserialize the predictions
            predicted = DataWrapper.unwrap_data(predicted)

            pprint(predicted)
        """

        try:

            # Predict the class(/es) for the input sample features
            #
            #  1. Unwrap the input request
            #  2. Prepare and validate the features
            #  3. Prepare and validate the predictor based on the model identifier
            #  4. Predict the class(/es) for the features
            #  5. Prepare and validate the prediction
            #  6. Wrap the output response
            #  7. Send the successful HTTP Response

            # Unwrap the input request
            request = RequestWrapper.unwrap_request(flask.request)
            self.log_request_data(request)

            # Prepare and validate the features
            features = Features.from_request(request)

            # Prepare predictor based on the model name specification and configuration
            model = PredictorModel.from_request(request).model

            # Predict the class(/es) for the features
            predicted = model.predict(features)

            # Prepare and validate the prediction(s)
            predicted = Predictions(predicted).to_response()
            self.log_response_data(predicted)

            # Wrap the output response
            response = ResponseWrapper.wrap_response(predicted)

            # Send the successful HTTP Response
            return flask.Response(response=response, status=HTTPStatus.OK, mimetype="application/json")

        # Handle the error logging
        except Exception as e:
            self.application_logger.error(e)
            raise
