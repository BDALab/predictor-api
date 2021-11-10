from api.resources.security import SignupResource, LoginResource, RefreshAccessTokenResource
from api.resources.predict import PredictClassesResource
from api.resources.predict_proba import PredictProbaResource


# ------------------------------------------ #
# Predictor API Resources helpers definition #
# ------------------------------------------ #

def add_predict_resource(api):
    """Registers predict resource"""
    api.add_resource(PredictClassesResource, "/predict")


def add_predict_proba_resource(api):
    """Registers predict_proba resource"""
    api.add_resource(PredictProbaResource, "/predict_proba")


def add_signup_resource(api):
    """Registers signup resource"""
    api.add_resource(SignupResource, "/signup")


def add_login_resource(api):
    """Registers login resource"""
    api.add_resource(LoginResource, "/login")


def add_refresh_resource(api):
    """Registers refresh resource"""
    api.add_resource(RefreshAccessTokenResource, "/refresh")


# ------------------------------------ #
# Predictor API Resources registration #
# ------------------------------------ #

def configure_routes(api):
    """
    Prepares and registers the resources supported by the predictor API.

    :param api: api instance
    :type api: flask_restful.API
    :return: None
    :rtype: None type
    """

    # Register the resources
    #
    #  1. add and register the PredictClassesResource
    #  2. add and register the PredictProbaResource
    #  3. add and register the SignupResource
    #  4. add and register the LoginResource
    #  5. add and register the RefreshAccessTokenResource
    add_predict_resource(api)
    add_predict_proba_resource(api)
    add_signup_resource(api)
    add_login_resource(api)
    add_refresh_resource(api)
