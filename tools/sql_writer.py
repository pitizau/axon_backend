# In file: tools/sql_writer.py

import os
import logging

class SqlWriter:
    """A tool for saving generated SQL to a file."""
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def save_sql(self, sql_content: str, output_path: str):
        """
        Saves the provided SQL content to a specified file path.

        Args:
            sql_content: The string content of the SQL script.
            output_path: The path (including filename) where the script should be saved.
        """
        self.logger.info(f"Attempting to save SQL script to {output_path}...")
        try:
            # Ensure the directory exists before writing the file
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, "w") as f:
                f.write(sql_content)
                
            self.logger.info(f"Successfully saved SQL script to {output_path}")
        except IOError as e:
            self.logger.error(f"Failed to write SQL script to file at {output_path}: {e}")
            raise
