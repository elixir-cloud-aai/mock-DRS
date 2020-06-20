import string
import sys

from flask import current_app
from connexion import request

from mock_drs.database.register_mongodb import create_mongo_client
from mock_drs.database.db_utils import insert_objects


def GetServiceInfo():
    return (
        {
            "version": "string",
            "title": "string",
            "description": "string",
            "contact": {},
            "license": {},
        },
        200,
    )


def GetBundle(bundle_id):
    return None


def GetObject(object_id: string):
    sys.stdout = open('file', 'w')
    # create a client for the database
    mongo = create_mongo_client(app=current_app, config=current_app.config)

    # retrieve the object by id or throw a 404
    obj = mongo.db.data_objects.find_one_or_404({"id": object_id})
    obj.pop("_id")
    print("obj: ", obj)
    return obj, 200


def PostObject():
    database = create_mongo_client(app=current_app, config=current_app.config)
    database.db.data_objects.insert(request.json)
    return request.json


def GetAccessURL(object_id, access_id):

    # create a client for the database
    mongo = create_mongo_client(app=current_app, config=current_app.config)

    # retrieve the object or throw a 404
    obj = mongo.db.data_objects.find_one_or_404({"id": object_id})
    # create the response
    access_methods = obj["access_methods"]

    response = {
        "detail": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
        "status": 404,
        "title": "Not Found",
        "type": "about:blank"
    }
    found = False
    for access_method in access_methods:
        if access_method["access_id"] == access_id:
            response = access_method["access_url"]
            found = True
            break
    if found:
        return response, 200
    else:
        return response, 404


def updateDatabaseObjects(body):
    current_objects = insert_objects(body["clear_db"], body["data_objects"])

    return {'objects': current_objects}, 200
