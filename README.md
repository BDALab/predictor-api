# Predictor API

![GitHub last commit](https://img.shields.io/github/last-commit/BDALab/predictor-api)
![GitHub issues](https://img.shields.io/github/issues/BDALab/predictor-api)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/BDALab/predictor-api)
![GitHub top language](https://img.shields.io/github/languages/top/BDALab/predictor-api)
![GitHub](https://img.shields.io/github/license/BDALab/predictor-api)

**Server side application**:

This package provides a modern RESTFul predictor API created using Python programming language and [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/) library. It is designed to be used for various predictors due to its flexible input/output data definition (multi-dimensional features, multiple subjects, etc.). On top of that, the predictor API provides endpoints for user authentication and JWT-based request authorization, it supports handling of cross-origin resource sharing, request-response caching, advanced logging, etc. It comes also with the basic support for containerization via Docker (Dockerfile and docker-compose).

**Client side application**:

To make the use of the Predictor API as easy as possible, there is a [PyPi-installable](https://pypi.org/project/predictor-api-client/) lightweight client side application named [Predictor API client](https://github.com/BDALab/predictor-api-client/) that provides method-based calls to all endpoints accessible on the API. For more information about the Predictor API client, please read the official [readme](https://github.com/BDALab/predictor-api-client#readme) and [documentation](https://github.com/BDALab/predictor-api-client/tree/master/docs).

**Endpoints**:
1. predictor endpoints (`api/resources/predict` and `api/resources/predict_proba`)
    1. `/predict` - calls `.predict` on the specified predictor. This endpoint is designed to be used to get the predicted values (e.g. classification: class label, regression: predicted value).
    2. `/predict_proba` - calls `.predict_proba` on the specified predictor. This endpoint is supposed to be used to get the predicted probabilities (e.g. classification: class probabilities).
2. security endpoints (`api/resources/security`)
    1. `/signup` - signs-up a new user.
    2. `/login` - logs-in an existing user (obtains access and refresh JWT tokens).
    3. `/refresh` - refreshes an expired access token (obtains refreshed FWT access token).

_The full programming sphinx-generated docs can be seen in `docs/`_.

**Contents**:
1. [Installation](#Installation)
2. [Configuration](#Configuration)
3. [Workflow](#Workflow)
4. [Data](#Data)
5. [Examples](#Examples)
6. [License](#License)
7. [Contributors](#Contributors)

---

## Installation

```
# Clone the repository
git clone https://github.com/BDALab/predictor-api.git

# Install packaging utils
pip install --upgrade pip
pip install --upgrade virtualenv

# Change directory
cd predictor-api

# Activate virtual environment
# Linux
# Windows

# Linux
virtualenv .venv
source .venv/bin/activate

# Windows
virtualenv venv
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Two necessary steps (see the configuration section bellow):
#
# 1. create .env file with the JWT secret key at api/.env
# 2. add dependencies of the predictors to be used at requirements_predictors.txt
# 3. configure the location of the serialized predictors at api/configuration/ml.json
```

## Configuration

The package provides various configuration files stored at `api/configuration`. More specifically, the following configuration is provided:
1. authentication (`api/configuration/authentication.json`): it supports the configuration of the database of users. In this version, the `sqlite` database is used for simplicity. The main configuration is the URI for the `*.db` file (pre-set to `api/authentication/database/database/database.db`). An empty database file is created automatically.
2. authorization (`api/configuration/authorization.json`): it supports the configuration of the request authorization. In this version, the JWT authorization is supported. The main configuration is the name of the `.env` file that stores the JWT secret key. For security reasons, the `.env` file is not part of this repository, i.e. **before using the API, it is necessary to create the .env file** at `api`-level, i.e. `api/.env` **and set the JWT_SECRET_KEY** field (e.g. `JWT_SECRET_KEY: "wfTHu38GpF5y60djwKC0EkFj586jdyZR"`).
3. cors (`api/configuration/cors.json`): it supports the configuration of the cross-origin resource sharing. In this version, no sources are added to the `origins`, (to be updated per deployment).
4. caching (`api/configuration/caching.json`): it supports the configuration of API request-response caching. In this version, the simple in-memory caching with the TTL of 60 seconds is used.
5. logging (`api/configuration/logging.json`): it supports the configuration of the logging. The package provides logging on three levels: (a) request, (b) response, (c) werkzeug. The log files are created in the `logs` directory located at the predictor's root directory.
6. machine learning (`api/configuration/ml.json`): it supports the configuration of the predictors. First, the dependencies of the serialized predictor models must be added to `requirements_predictors.txt` (e.g. when using serialized scikit-learn models, `scikit-learn` must be added). The API will automatically install all predictor dependencies specified in this file. Next, the location of the serialized models must be set via `predictors.location` (full-path is needed; by default, it is set to: `api/ml/models`). **All serialized models must be placed at `predictors.location`** to be loadable at the runtime. **Only models serialized as `joblib` files are supported**.

## Workflow

In order for a user to use the API, the following steps are required:
1. a new user must be created via the `/signup` endpoint
2. the existing user must log-in to get the access and refresh token via the `login` endpoint
3. calls to the `/predict` or `/predict_proba` endpoints can be made 
4. if the access token expires, a new one must be obtained via the `/refresh` endpoint

For specific examples for each step of the workflow, see the [Examples](#Examples) section.

## Data

### Input data

Structure of the input data is the following: it is a ``dict`` object with these field-value pairs (example bellow):
- ``features`` (``dict``, mandatory; _placeholder for the feature values/labels_)
- ``features.values`` (``numpy.array``, mandatory; _feature values_)
- ``features.labels`` (``list``, optional; _feature labels_)
- ``model`` (``str``, mandatory; _predictor identifier_)

**Shape**:

Shape of the feature values: (first dimension, (inner dimensions), last dimension)

- the first dimension is dedicated to subjects
- the inner dimensions are dedicated to the dimensionality of the features
- the last dimension is dedicated to features

Important requirement that must be met is to provide the predictor with the data it can process (shape, format, etc.).

```
# Dimensions: M subjects, N features of (... dimensions)
{
    "features": {
        "labels": ["feature 1", ... "feature N"],
        "values": array of shape (M, ..., N)
    },
    "model": "model_identifier"
}
```

**Examples**:

- 100 subjects, each having 30 1-D features (shape `(1,)` or shape `(1, 1)`): `shape = (100, 1, 30)`
- 250 subjects, each having 20 2-D features (shape `(2,)` or shape `(1, 2)`): `shape = (250, 2, 20)`
- 500 subjects, each having 10 features with the shape of `(3, 4)`: `shape = (500, 3, 4, 10)`

### Output data

Structure of the output data is the following: it is a ``dict`` object with these field-value pairs (example bellow): ``predicted``(``numpy.array``, mandatory; _predicted values_)

**Shape**:

Shape of the predicted values: (first dimension, last dimension)

- the first dimension is dedicated to subjects
- the last dimension is dedicated to the dimensionality of the predicted values

```
# Dimensions: M subjects, C-dimenasional predicted values
{
    "predicted": array of shape (M, C)
}
```

**Examples**:

- 100 subjects, `/predict` (classification): `shape = (100, 1)` or `shape = (100, 1, 1)` (1 class label)
- 250 subjects, `/predict_proba` (classification): `shape = (250, 1, 10)` (10 classes; class probabilities)
- 500 subjects, `/predict` (regression): `shape = (100, 1)` or `shape = (100, 1, 1)` (1 predicted value)

### Serialization/deserialization

As the feature values/predictions are stored as a ``numpy.array``, they must be JSON-serialized/deserialized. For this purpose, the package provides the ``api.wrapper.data.DataWrapper`` class.

## Examples

### User sign-up

```python
import requests

# Prepare the sign-up data (new user to be created)
body = {
    "username": "user123",
    "password": "pAsSw0rd987!"
}

# Call the sign-up endpoint (locally deployed API)
response = requests.post(
    "http://localhost:5000/signup",
    json=body)
```

### User log-in

```python
import requests

# Prepare the log-in data (already created user)
body = {
    "username": "user123",
    "password": "pAsSw0rd987!"
}

# Call the log-in endpoint (locally deployed API)
response = requests.post(
    "http://localhost:5000/login",
    json=body)

# Get the access and refresh tokens from the response
if response.ok:
    access_token = response.json().get("access_token")
    refresh_token = response.json().get("refresh_token")
```

### Prediction

```python
import numpy
import requests
from pprint import pprint
from api.wrappers.data import DataWrapper

# Set the number of subjects (10)
num_subjects = 10

# Set the shape of the features for each subject (1, 100): 1-D feature vector with 100 features
features_shape = (1, 100)

# Prepare the feature values/labels (labels are optional)
values = numpy.random.rand(num_subjects, *features_shape)
labels = [f"feature {i}" for i in range(features_shape[-1])]

# Serialize the feature values
values = DataWrapper.wrap_data(values)

# Prepare the model identifier
model = "a3ed6e799cd755286138a53e5fd43102"

# Prepare the predictor data
body = {
    "features": {
        "labels": values,
        "values": labels
    },
    "model": model
}

# Prepare the authorization header (take the access_token obtained via /login endpoint)
headers = {
    "Authorization": f"Bearer <access_token>"
}

# Call the predict endpoint (locally deployed API; endpoints: /predict or /predict_proba)
response = requests.post(
    url="http://localhost:5000/predict",
    json=body,
    headers=headers,
    verify=True,
    timeout=10)

if response.ok:

    # Get the predictions
    predicted = response.json().get("predicted")
    
    # Deserialize the predictions
    predicted = DataWrapper.unwrap_data(predicted)
    
    pprint(predicted)
```

### Expired access token refresh

```python
import requests

# Prepare the refresh headers (take the refresh_token obtained via /login endpoint)
headers = {
    "Authorization": f"Bearer <refresh_token>"
}

# Call the refresh endpoint (locally deployed API)
response = requests.post(
    "http://localhost:5000/refresh",
    headers=headers)

# Get the refreshed access token
if response.ok:
    access_token = response.json().get("access_token")
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributors

This package is developed by the members of [Brain Diseases Analysis Laboratory](http://bdalab.utko.feec.vutbr.cz/). For more information, please contact the head of the laboratory Jiri Mekyska <mekyska@vut.cz> or the main developer: Zoltan Galaz <galaz@vut.cz>.