# In file: tools/database_connector.py

import pandas as pd
import logging

class BaseConnector:
    """Base class for all database connectors."""
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def get_schema(self):
        """Retrieves the database schema."""
        raise NotImplementedError

class MockConnector(BaseConnector):
    """
    A mock database connector for development and testing.
    It simulates a connection and returns a predefined schema.
    """
    def connect(self):
        self.logger.info("Mock Connection Successful to 'mock-db'.")

    def disconnect(self):
        self.logger.info("Mock Disconnection Successful from 'mock-db'.")

    def get_schema(self) -> pd.DataFrame:
        """
        Returns a sample schema as a pandas DataFrame.
        This simulates what a real connector would fetch from a database.
        """
        self.logger.info("Fetching mock schema...")
        schema_data = {
            'table_name': ['users', 'users', 'orders', 'orders', 'orders'],
            'column_name': ['user_id', 'email', 'order_id', 'user_id', 'order_date'],
            'data_type': ['INTEGER', 'VARCHAR(255)', 'INTEGER', 'INTEGER', 'TIMESTAMP']
        }
        return pd.DataFrame(schema_data)