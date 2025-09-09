# In file: tests/test_validation_agent.py

import unittest
from unittest.mock import patch, mock_open, MagicMock
from agents.validation_agent import DataValidationAgent

class TestDataValidationAgent(unittest.TestCase):
    """
    Tests for the DataValidationAgent (Step 7).
    """

    def setUp(self):
        """Initializes the agent for testing."""
        self.agent = DataValidationAgent(
            model_name="test-model",
            project="test-project",
            location="us-central1"
        )
        # Mock the agent's LLM call
        self.agent._execute_prompt = MagicMock(return_value="-- Mocked Validation SQL")

    def test_run_generates_validation_sql(self):
        """
        Tests that the agent's run method correctly calls the SQL writer.
        """
        schema_analysis = {"summary": "A test schema"}
        output_path = "fake/output/validation.sql"

        # Mock the SqlWriter tool
        with patch("tools.sql_writer.SqlWriter.save_sql") as mock_save_sql:
            self.agent.run(schema_analysis, output_path)

            # Verify that the prompt was executed
            self.agent._execute_prompt.assert_called_once()
            
            # Verify that the save_sql method was called with the correct content
            mock_save_sql.assert_called_once_with(
                sql_content="-- Mocked Validation SQL",
                output_path=output_path
            )

if __name__ == "__main__":
    unittest.main()
