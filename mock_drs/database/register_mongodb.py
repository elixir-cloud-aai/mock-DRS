"""Function for Registering MongoDB with a Flask app instance."""

import logging
from typing import Dict
import json

from flask import Flask
from flask_pymongo import ASCENDING, PyMongo
from pymongo import MongoClient

from config.config_parser import get_conf

from random import choice

def register_mongodb(app: Flask) -> Flask:
    """Instantiates database and initializes collections."""
    config = app.config

    # Instantiate PyMongo client
    mongo = create_mongo_client(app=app, config=config)

    # Add database
    db = mongo.db[get_conf(config, "database", "name")]

    # Add database collection for '/service-info'
    collection_service_info = mongo.db["service-info"]

    # Add database collection for '/data_objects'
    collection_data_objects = mongo.db["data_objects"]
    collection_data_objects.create_index(
        [("object_id", ASCENDING)], unique=True, sparse=True
    )

    # Add database to app config
    config["database"]["objects"] = db
    config["database"]["bundles"] = dict()
    # config["database"]["collections"]["object_id"] =
    config["database"]["service_info"] = collection_service_info
    app.config = config

    return app


def create_mongo_client(app: Flask, config: Dict):
    """Instantiate MongoDB client."""
    uri = "mongodb://{host}:{port}/{name}".format(
        host=get_conf(config, "database", "host"),
        port=get_conf(config, "database", "port"),
        name=get_conf(config, "database", "name"),
    )

    mongo = PyMongo(app, uri=uri)
    return mongo


def populate_mongo_databse(config: Dict, number: int):
    """Populate the DRS  with data objects."""
    uri = "mongodb://{host}:{port}/{name}".format(
        host=get_conf(config, "database", "host"),
        port=get_conf(config, "database", "port"),
        name=get_conf(config, "database", "name"),
    )

    client = MongoClient(uri)
    database = client["data_objects"]
    db_object = json.loads(open("database/data_objects.json", "r").read())
    database["data_objects"].insert(db_object)

    #choice()