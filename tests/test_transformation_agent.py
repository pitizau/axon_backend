# In file: tests/test_transformation_agent.py

import unittest
from unittest.mock import MagicMock, patch, mock_open
from agents.transformation_agent import SchemaTransformationAgent

class TestSchemaTransformationAgent(unittest.TestCase):
    """
    Tests for the SchemaTransformationAgent (Step 5).
    """

    def setUp(self):
        """Set up a mock agent for testing."""
        self.agent = SchemaTransformationAgent(
            model_name="test-model",
            project="test-project",
            location="us-central1"
        )

    def test_run_generates_and_saves_sql(self):
        """
        Tests the full run process of the transformation agent.
        """
        # 1. Mock the input schema analysis
        mock_schema_analysis = {
            "summary": "A test database.",
            "key_tables": [
                {"table_name": "customers", "role": "Dimension", "description": "Stores customer data."}
            ],
            "relationships": []
        }
        
        # 2. Mock the LLM response (the SQL script)
        mock_sql_script = "-- This is a test SQL script.\nCREATE TABLE customers (customer_id INTEGER PRIMARY KEY);"
        self.agent._execute_prompt = MagicMock(return_value=mock_sql_script)
        
        # 3. Mock the file writing operation
        with patch("builtins.open", mock_open()) as mocked_file:
            # 4. Run the agent
            output_path = "fake/output/schema.sql"
            self.agent.run(mock_schema_analysis, output_path)

            # 5. Assertions
            # Check that the LLM was called once
            self.agent._execute_prompt.assert_called_once()
            
            # Check that the file was opened for writing at the correct path
            mocked_file.assert_called_once_with(output_path, "w")
            
            # Check that the correct content was written to the file
            mocked_file().write.assert_called_once_with(mock_sql_script)

if __name__ == "__main__":
    unittest.main()
