"""Function for Registering MongoDB with a Flask app instance."""

import logging
from typing import Dict

from flask import Flask
from flask_pymongo import ASCENDING, PyMongo

from config.config_parser import get_conf
from app.ga4gh.drs.Endpoints.server import GetServiceInfo


# Get logger instance
logger = logging.getLogger(__name__)


def register_mongodb(app: Flask) -> Flask:
    """Instantiates database and initializes collections."""
    config = app.config

    # Instantiante PyMongo client
    mongo = create_mongo_client(
        app=app,
        config=config,
    )

    # Add database
    db = mongo.db[get_conf(config, 'database', 'name')]

    Add database collection for '/service-info'
    collection_service_info = mongo.db['service-info']

    #Add database collection for '/data_objects'
    collection_data_objects = mongo.db['data_objects']
    collection_data_objects.create_index([
            ('bundle_id', ASCENDING),
            ('object_id', ASCENDING),
        ],
        unique=True,
        sparse=True
    )

    # Add database and collections to app config
    config['database']['database'] = db
    config['database']['collections'] = dict()
    config['database']['collections']['bundle_id'] = collection_runs
    #config['database']['collections']['service_info'] = collection_service_info
    app.config = config

    # Initialize service info
    #logger.debug('Initializing service info...')
    #get_service_info(config, silent=True)

    return app


def create_mongo_client(
    app: Flask,
    config: Dict,
):
    """Instantiate MongoDB client."""
    uri = 'mongodb://{host}:{port}/{name}'.format(
        host=get_conf(config, 'database', 'host'),
        port=get_conf(config, 'database', 'port'),
        name=get_conf(config, 'database', 'name'),
    )
    mongo = PyMongo(app, uri=uri)
    logger.info(
        (
            "Registered database '{name}' at URI '{uri}' with Flask "
            'application.'
        ).format(
            name=get_conf(config, 'database', 'name'),
            uri=uri,
        )
    )
    return mongo