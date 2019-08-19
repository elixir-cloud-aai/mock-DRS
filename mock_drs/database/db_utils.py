"""Utility functions for MongoDB document access and retrieval of DataObjects"""
import json
import os

from typing import List, Dict

from flask import Flask
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


def insert_objects(objects_list:List):
    # TO-DO :
    #   add option to post a dict to the database here

    database = create_mongo_client(app=Flask.current_app, config=Flask.current_app.config)
    data_objects_path = os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "data_objects.json")
    )
    data = json.loads(open(data_objects_path, "r").read())

    for object_id in objects_list:
        try:
            database.db.data_objects.insert(data[object_id])
            print("entry added:", object_id)
        except DuplicateKeyError:
            database.db.data_objects.delete_one({"id": object_id})
            database.db.data_objects.update_one(
                {"id": object_id}, {"$setOnInsert": data[object_id]}, upsert=True
            )
            print("duplicate updated:", object_id)
        except KeyError:
            print("object not found, skipped:", object_id)
        print("database contents are :", database.db.data_objects.distinct("id"))
