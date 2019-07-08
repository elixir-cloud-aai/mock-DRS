import string

from flask import current_app

from database.register_mongodb import create_mongo_client


def GetServiceInfo():
    return {
        "version": "string",
        "title": "string",
        "description": "string",
        "contact": {},
        "license": {},
    }, 200


def GetBundle(bundle_id):
    return None


def GetObject(object_id: string):

    mongo = create_mongo_client(app=current_app, config=current_app.config)
    obj = mongo.db.data_objects.find_one_or_404({"id": object_id})
    obj.pop("_id")
    return obj, 200


def GetAccessURL(object_id, access_id):
    # to-do : implement this endpoint
    return None
