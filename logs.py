from typing import Dict
import datetime

from pymongo import MongoClient, database, collection


class Logs:
    def __init__(self, config: Dict[str, str]):
        self.collection = self.connect_db(config)

    def connect_db(self, config: Dict[str, str]) -> collection:
        client = self._get_client(config['HOST'], int(config['PORT']))
        db = self._get_database(client, config['DB'])
        collection = self._get_collection(db, config['COLLECTION'])

        return collection

    def _get_client(self, host: str, port: int) -> MongoClient:
        return MongoClient(host, port)

    def _get_database(self, client: MongoClient, database_name: str) -> database:
        return client[database_name]

    def _get_collection(self, db: database, collection_name: str) -> collection:
        return db[collection_name]

    def write_info(self, crawler_name: str, message: str):
        log_message = {
            "crawler": crawler_name,
            "type": "INFO",
            "message": message,
            "date": datetime.datetime.now(),
        }

        self.collection.insert_one(log_message)

    def write_error(self, crawler_name: str, message: str):
        log_message = {
            "crawler": crawler_name,
            "type": "ERROR",
            "message": message,
            "date": datetime.datetime.now(),
        }

        self.collection.insert_one(log_message)
