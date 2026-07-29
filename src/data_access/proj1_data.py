import sys
from typing import Any, Optional
import numpy as np
import pandas as pd

from src.configuration.mongo_db_connection import MongoDBClient
from src.constants import DATABASE_NAME
from src.exception import MyException


class Proj1Data:

    def __init__(self) -> None:
        try:
            # Initializes the MongoDB custom client wrapper
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
            
            # Extract the raw pymongo client if your class wraps it, 
            # otherwise default directly to the object instance
            self.client: Any = getattr(self.mongo_client, "client", self.mongo_client)
        except Exception as e:
            raise MyException(e, sys) from e

    def export_collection_as_dataframe(
        self, collection_name: str, database_name: Optional[str] = None
    ) -> pd.DataFrame:
        try:
            # 1. Resolve the correct database context cleanly
            db_name = database_name if database_name is not None else DATABASE_NAME
            collection = self.client[db_name][collection_name]

            # 2. Fetch records and safely check for empty collections
            records = list(collection.find())
            if not records:
                # Return a safe empty dataframe instead of crashing later
                return pd.DataFrame()

            df = pd.DataFrame(records)

            # 3. FIX: Drop standard MongoDB '_id' column if it exists
            if "_id" in df.columns:
                df = df.drop(columns=["_id"], axis=1)
                
            # Keep your check for "id" just in case your data explicitly has it
            if "id" in df.columns:
                df = df.drop(columns=["id"], axis=1)

            # 4. Standardize missing value placeholders to NumPy NaN
            df.replace({"na": np.nan}, inplace=True)

            return df
        except Exception as e:
            raise MyException(e, sys) from e
