# In file: tools/memory_manager.py

import json
import os
import logging
from typing import Dict, Any, List

class MemoryManager:
    """
    A tool to simulate a vector database for continuous learning.
    It saves and retrieves pipeline results from a JSON file.
    """
    def __init__(self, filepath: str = "output/memory.json"):
        self.filepath = filepath
        self.logger = logging.getLogger(self.__class__.__name__)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Ensures the memory file and its directory exist."""
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            if not os.path.exists(self.filepath):
                with open(self.filepath, 'w') as f:
                    json.dump([], f) # Start with an empty list
                self.logger.info(f"Created new memory file at {self.filepath}")
        except IOError as e:
            self.logger.error(f"Could not create memory file: {e}")
            raise

    def save_memory(self, memory_item: Dict[str, Any]):
        """
        Saves a new memory item (e.g., a pipeline run) to the memory file.

        Args:
            memory_item: A dictionary containing the data to be remembered.
        """
        self.logger.info("Saving new memory...")
        try:
            memories = self.load_memories()
            memories.append(memory_item)
            with open(self.filepath, 'w') as f:
                json.dump(memories, f, indent=2)
            self.logger.info(f"Successfully saved memory. Total memories: {len(memories)}")
        except (IOError, json.JSONDecodeError) as e:
            self.logger.error(f"Failed to save memory: {e}")

    def load_memories(self) -> List[Dict[str, Any]]:
        """
        Loads all memories from the JSON file.
        In a real system, this would query a vector DB.
        """
        self.logger.info("Loading memories...")
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            self.logger.error(f"Failed to load memories: {e}")
            return [] # Return empty list on failure

    def get_context_for_prompt(self) -> str:
        """
        Retrieves the most recent memory to use as context.
        This simulates a similarity search in a vector DB.
        """
        memories = self.load_memories()
        if not memories:
            return "No previous runs available for context."
        
        # Return the most recent memory as a JSON string
        latest_memory = memories[-1]
        return json.dumps(latest_memory, indent=2)
