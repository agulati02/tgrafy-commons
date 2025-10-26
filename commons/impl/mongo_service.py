from __future__ import annotations
import os
import certifi
from typing import Any, Optional, ClassVar
from ..interfaces import DatabaseServiceInterface
from pymongo import MongoClient
from pymongo.results import UpdateResult
from pymongo.database import Database


class MongoDBService(DatabaseServiceInterface):
    _instance: ClassVar[Optional[MongoDBService]] = None
    _client: ClassVar[Optional[MongoClient[dict[str, Any]]]] = None
    _db: ClassVar[Optional[Database[Any]]] = None

    def __new__(cls, *args, **kwargs) -> MongoDBService:    # type: ignore
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
            self, 
            conn_string: str, 
            db_name: str, 
            username: str,
            password: str,
        ) -> None:
        if not hasattr(self, 'initialized'):
            self.conn_string = conn_string
            self.db_name = db_name
            self.username = username
            self.password = password
            self.initialized = True
            self._connect()
    
    def _connect(self) -> None:
        if MongoDBService._client is None:
            ca_bundle = certifi.where()
            if not os.path.exists(ca_bundle):
                raise RuntimeError("certifi CA bundle not found")
            full_conn_string = self.conn_string.format(db_username=self.username, db_password=self.password)
            MongoDBService._client = MongoClient(
                full_conn_string,
                tls=True,
                tlsCAFile=ca_bundle,
                maxPoolSize=5,
                minPoolSize=0,
                serverSelectionTimeoutMS=3000,
                connectTimeoutMS=3000,
                socketTimeoutMS=3000,
                maxIdleTimeMS=15000,
                waitQueueTimeoutMS=3000
            )
            MongoDBService._db = MongoDBService._client.get_database(self.db_name)
    
    def __enter__(self) -> MongoDBService:
        self._connect()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None: # type: ignore
        """Return connection to pool but don't close"""
        # if self._client:
        #     self._client.close()
        pass

    @property
    def client(self) -> Optional[MongoClient[dict[str, Any]]]:
        return MongoDBService._client

    @property
    def db(self) -> Optional[Database[Any]]:
        return MongoDBService._db

    @classmethod
    def close_connection(cls) -> None:
        """Explicitly close the connection when needed"""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None

    def query(self, collection: str, filter: dict[str, Any], select: Optional[dict[str, Any]] = None) -> list[dict[str, Any]]:
        """Runs a query in MongoDB, based on the given filter"""
        if not isinstance(self._db, Database):
            raise ValueError("Database is not initialized.")

        return self._db.get_collection(collection).find(filter, projection=select).to_list()

    def save(self, collection: str, data: dict[str, Any]) -> None:
        """Saves a document to specified collection"""
        if not isinstance(self._db, Database):
            raise ValueError("Database is not initialized.")
        
        self._db.get_collection(collection).insert_one(data)
    
    def update(self, collection: str, filter: dict[str, Any], diff: dict[str, Any]) -> None:
        """Updates a document"""
        if not isinstance(self._db, Database):
            raise ValueError("Database is not initialized")
        
        update_result: UpdateResult = self._db.get_collection(collection).update_one(
            filter=filter,
            update={"$set": diff}
        )

        if update_result.modified_count == 0:
            raise Exception(f"Document update failed for filter: {filter} and diff: {diff}")
