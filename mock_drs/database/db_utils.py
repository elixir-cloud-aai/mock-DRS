"""Utility functions for MongoDB document access and retrieval of DataObjects"""
import json
import os

from typing import List, Dict

from flask import Flask
from flask import current_app
from flask_pymongo import ASCENDING, PyMongo

from pymongo import InsertOne, DeleteOne, ReplaceOne
from pymongo.errors import DuplicateKeyError

from config.config_parser import get_conf


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
    # TO-DO :
    #   fix print while docker image is used

    database = create_mongo_client(app= current_app, config= current_app.config).db.data_objects

    if clear:
        clear_mongo_database(database)

    data_objects_path = os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "data_objects.json")
    )

    data = json.loads(open(data_objects_path, "r").read())
    data = {x["id"]: x for x in data}
    for object_id in objects_list:
        try:
            database.insert(data[object_id])
            print("entry added:", object_id)
        except DuplicateKeyError:
            database.delete_one({"id": object_id})
            database.update_one(
                {"id": object_id}, {"$setOnInsert": data[object_id]}, upsert=True
            )
            print("duplicate updated:", object_id)
        except KeyError:
            print("object not found, skipped:", object_id)

    objects = database.distinct("id")
    print("database contents are :", objects)
    return objects
