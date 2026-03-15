from flask import current_app
from pymongo import MongoClient

_client = None


def init_db(app):
    """
    Initialize MongoDB client using app config.
    Expects MONGO_URI and MONGO_DB_NAME in configuration.
    """
    global _client
    mongo_uri = app.config.get("MONGO_URI", "mongodb://localhost:27017/")
    _client = MongoClient(mongo_uri)
    app.config.setdefault("MONGO_DB_NAME", "college_fest_guide")


def get_db():
    """
    Return a handle to the configured MongoDB database.
    """
    db_name = current_app.config["MONGO_DB_NAME"]
    return _client[db_name]

