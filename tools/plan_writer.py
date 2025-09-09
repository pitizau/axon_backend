# In file: tools/plan_writer.py

import os
import logging

class PlanWriter:
    """A tool for saving generated migration plans to a file."""
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def save_plan(self, plan_content: str, output_path: str):
        """
        Saves the provided content to a specified file path.

        Args:
            plan_content: The string content of the migration plan.
            output_path: The path (including filename) where the plan should be saved.
        """
        self.logger.info(f"Attempting to save migration plan to {output_path}...")
        try:
            # Ensure the directory exists before writing the file
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, "w") as f:
                f.write(plan_content)
                
            self.logger.info(f"Successfully saved plan to {output_path}")
        except IOError as e:
            self.logger.error(f"Failed to write plan to file at {output_path}: {e}")
            raise
