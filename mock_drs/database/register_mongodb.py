"""Function for Registering MongoDB with a Flask app instance."""

import json
import logging
import os
from typing import Dict
from random import choice, randint

from flask import Flask
from flask_pymongo import ASCENDING, PyMongo

from pymongo import InsertOne, DeleteOne, ReplaceOne
from pymongo.errors import DuplicateKeyError

from config.config_parser import get_conf


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
    collection_data_objects.create_index([("id", ASCENDING)], unique=True, sparse=True)

    # Add database to app config
    config["database"]["drs_db"] = collection_data_objects
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


def clear_mongo_database(database):
    for id in database.distinct("id"):
        database.delete_one({"id": id})


def populate_mongo_database(app: Flask, config: Dict):
    """Populate the DRS  with data objects."""
    data_objects_path = os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "data_objects.json")
    )
    database = create_mongo_client(app=app, config=app.config)
    data = json.loads(open(data_objects_path, "r").read())
    clear_mongo_database(database.db.data_objects)
    database_contents = config["database"]["objects"]
    data = {x["id"]: x for x in data}
    for object_id in database_contents:
        try:
            database.db.data_objects.insert(data[object_id])
        except DuplicateKeyError:
            database.db.data_objects.delete_one({"id": object_id})
            database.db.data_objects.update_one(
                {"id": object_id}, {"$setOnInsert": data[object_id]}, upsert=True
            )
        print("duplicate updated:", object_id)
        print("database contents are :", database.db.data_objects.distinct("id"))
