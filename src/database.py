import logging

from tinydb import TinyDB
from typing import Optional

from mapping import Directory


class DatabaseUtil:
    def __init__(self):
        logging.info(f"↳ Extension {__name__} initialized.")
        self.database: Optional[TinyDB] = None

    @staticmethod
    def initialization() -> TinyDB:
        logging.info(rf"Initializing database. Creating database {Directory.DATABASE.value}")
        database: TinyDB = TinyDB(Directory.DATABASE.value)
        initial_config: list = [{"name": "headers", "value": {}}, {"name": "snowflake", "value": 0}]
        for data in initial_config:
            database.insert(data)
        return database

    @staticmethod
    def processing() -> TinyDB:
        logging.info(rf"Found database, Loading {Directory.DATABASE.value}")
        database: TinyDB = TinyDB(Directory.DATABASE.value)
        return database
