"""
Mock Service for the GA4GH Data Repository Schema 
"""
import os
import sys

from connexion import App

from specsynthase.specbuilder import SpecBuilder

from mock_drs.config.app_config import parse_app_config
from mock_drs.database.register_mongodb import register_mongodb, populate_mongo_database
from mock_drs.database.db_utils import create_mongo_client


app = App(__name__)
config = parse_app_config(config_var="DRS_CONFIG")

# use the swagger spec to define the flaskapp
try:
    app = App(__name__, swagger_ui=True, swagger_json=True)
except KeyError:
    sys.exit("Config file corrupt. Execution aborted.")


def configure_app(app):
    """Configure app"""

    # Add settings
    app = add_settings(app)

    # Add OpenAPIs
    app = add_openapi(app)

    # Add user configuration to Flask app config
    app.app.config.update(config)

    return app


def add_settings(app):
    """Add settings to Flask app instance"""
    try:
        app.host = config["server"]["host"]
        app.port = config["server"]["port"]
        app.debug = config["server"]["debug"]
    except KeyError:
        sys.exit("Config file corrupt. Execution aborted.")

    return app


def add_openapi(app):
    """Add OpenAPI specification to connexion app instance"""
    try:
        specs = SpecBuilder()\
                .add_spec(config["openapi"]["drs"])\
                .add_spec(config["openapi"]["db_update"])
        app.add_api(
            specs,
            validate_responses=True,
            strict_validation=True,
        )
    except KeyError:
        sys.exit("Config file corrupt. Execution aborted.")
    return app


def main(app):
    """Initialize, configure and run server"""
    # add api & configuration for port
    app = configure_app(app)

    # Add mongoDB configuration
    app.app = register_mongodb(app.app)

    # Create a client for the mongoDB instance
    mongo_client = create_mongo_client(app.app, config)

    # Add objects to the database
    populate_mongo_database(app.app, config)

    # run app
    app.run()


if __name__ == "__main__":
    main(app)
