"""
Mock Service for the GA4GH Data Repository Schema 
"""
from config.app_config import parse_app_config
from connexion import App

from flask_pymongo import ASCENDING, PyMongo

# from ga4gh.drs.endpoints import

from connexion.resolver import RestyResolver
from connexion import App

app = App(__name__)
config = parse_app_config("config.yaml", config_var="DRS_CONFIG")

# use the swagger spec to define the flaskapp
try:
    app = App(
        __name__,
        specification_dir=config["openapi"]["path"],
        swagger_ui=True,
        swagger_json=True,
    )
except KeyError:
    sys.exit("Config file corrupt. Execution aborted.")


# Initialize database
try:
    mongo = PyMongo(
        app.app,
        uri="mongodb://{host}:{port}/{name}".format(
            host=config["database"]["host"],
            port=config["database"]["port"],
            name=config["database"]["name"],
        ),
    )
    db = mongo.db[config["database"]["name"]]
except KeyError:
    sys.exit("Config file corrupt. Execution aborted.")

# Add database collections
db_service_info = mongo.db["service-info"]
db_tasks = mongo.db["tasks"]
db_tasks.create_index([("task_id", ASCENDING)], unique=True)


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
        app.add_api(config["openapi"]["yaml_specs"], validate_responses=True)
    except KeyError:
        sys.exit("Config file corrupt. Execution aborted.")

    return app



def main(app):
    """Initialize, configure and run server"""
    app = configure_app(app)
    app.run()


if __name__ ==  '__main__' :
    main(app)
