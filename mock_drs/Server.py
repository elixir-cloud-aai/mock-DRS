"""
Mock Service for the GA4GH Data Repository Schema 
"""
from config.app_config import parse_app_config
from connexion import App

from database.register_mongodb import register_mongodb


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
    # add api & configuration for port
    app = configure_app(app)

    # Add mongo_db configuration
    app.app = register_mongodb(app.app)

    app.run()


if __name__ ==  '__main__' :
    main(app)
