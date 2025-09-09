# In file: tests/test_memory_manager.py

import unittest
import os
import json
from unittest.mock import patch, mock_open, call
from tools.memory_manager import MemoryManager

class TestMemoryManager(unittest.TestCase):
    """
    Tests for the MemoryManager tool (Step 6).
    """
    
    def setUp(self):
        """Setup a temporary file path for tests."""
        self.test_filepath = "fake/memory/test_memory.json"

    @patch("os.makedirs")
    def test_save_and_load_memory(self, mock_makedirs):
        """
        Tests that saving and loading memories works correctly.
        """
        # Mock the file I/O operations
        m = mock_open(read_data='[]')
        with patch("builtins.open", m):
            manager = MemoryManager(filepath=self.test_filepath)
            
            # 1. Test saving a new memory
            new_memory = {"id": 1, "data": "test"}
            manager.save_memory(new_memory)
            
            # Check if open was called correctly for writing
            m.assert_called_with(self.test_filepath, 'w')
            
            # CORRECTED: Join all calls to write() to get the full string
            # This handles cases where a function writes in chunks, like json.dump()
            all_written_calls = m().write.call_args_list
            written_content = "".join(call.args[0] for call in all_written_calls)
            
            self.assertIn('"id": 1', written_content)
            self.assertIn('"data": "test"', written_content)
            
            # 2. Test loading memories
            # Simulate reading the data we just "wrote"
            m.return_value.read.return_value = '[{"id": 1, "data": "test"}]' 
            memories = manager.load_memories()
            self.assertEqual(len(memories), 1)
            self.assertEqual(memories[0]["data"], "test")

    def tearDown(self):
        """Clean up any created fake files if necessary (though mock prevents it)."""
        if os.path.exists(self.test_filepath):
            os.remove(self.test_filepath)

