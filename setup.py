import pathlib
from setuptools import setup, find_packages


# Get the long description from the README file
long_description = (pathlib.Path(__file__).parent.resolve() / "README.md").read_text(encoding="utf-8")

# Prepare the packages and requirements
packages = find_packages(where="api")
requires = [
    "requests",
    "flask",
    "Flask-RESTful",
    "Flask-SQLAlchemy",
    "Flask-Bcrypt",
    "Flask-JWT-Extended",
    "Flask-Cors",
    "flask-api-cache",
    "webargs",
    "marshmallow",
    "python-dotenv",
    "numpy",
    "json-tricks",
    "joblib"
]

# Prepare the setup
setup(
    name="predictor-api",
    version="1.0.0",
    description="Predictor API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BDALab/predictor-api",
    author="Brain Diseases Analysis Laboratory",
    author_email="galaz@vut.cz",
    packages=packages,
    package_data={"": ["LICENSE"]},
    package_dir={"": "api"},
    include_package_data=True,
    install_requires=requires,
    python_requires=">=3.7",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent"
    ]
)
