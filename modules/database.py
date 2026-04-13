import sqlite3

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection = cls._instance._create_connection()
        return cls._instance

    def _create_connection(self):
        # Database connection
        conn = sqlite3.connect('my_database.db')
        return conn

    def get_connection(self):
        return self.connection

    # Add any additional methods for caching or handling database queries

