"""Utility functions for MongoDB document access and retrieval of DataObjects"""
import json
import os

from typing import List, Dict

from flask import Flask
from flask import current_app
from flask_pymongo import ASCENDING, PyMongo

from pymongo import InsertOne, DeleteOne, ReplaceOne
from pymongo.errors import DuplicateKeyError

from mock_drs.config.config_parser import get_conf


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


def insert_objects(clear: bool, objects_list: List):

    database = create_mongo_client(app= current_app, config= current_app.config).db.data_objects

    if clear:
        clear_mongo_database(database)

    data_objects_path = os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "data_objects.json")
    )

    for object in objects_list:
        try:
            database.insert(object)
            print("entry added:", object["id"])
        except DuplicateKeyError:
            database.delete_one({"id": object["id"]})
            database.update_one(
                {"id": object["id"]}, {"$setOnInsert": object}, upsert=True
            )
            print("duplicate updated:", object["id"])
        except KeyError:
            print("object not found, skipped:", object["id"])

    objects = database.distinct("id")
    print("database contents are :", objects)
    return objects
