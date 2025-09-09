# In file: tests/test_planning_agent.py

import unittest
import os
from unittest.mock import MagicMock, patch, mock_open
from agents.planning_agent import MigrationPlanAgent

class TestPlanningAgent(unittest.TestCase):
    """
    Tests for the MigrationPlanAgent (Step 4).
    """

    def setUp(self):
        """Set up a mock agent for testing."""
        self.agent = MigrationPlanAgent(
            model_name="test-model",
            project="test-project",
            location="us-central1"
        )

    def test_run_generates_and_saves_plan(self):
        """
        Tests the full run process of the planning agent.
        """
        # 1. Mock the input schema analysis
        mock_schema_analysis = {
            "summary": "A test database.",
            "key_tables": [],
            "relationships": []
        }
        
        # 2. Mock the LLM response (the markdown plan)
        mock_markdown_plan = "## 1. Executive Summary\nThis is a test plan."
        self.agent._execute_prompt = MagicMock(return_value=mock_markdown_plan)
        
        # 3. Mock the file writing operation
        # 'patch' intercepts the built-in 'open' function
        with patch("builtins.open", mock_open()) as mocked_file:
            # 4. Run the agent
            output_path = "fake/output/plan.md"
            self.agent.run(mock_schema_analysis, output_path)

            # 5. Assertions
            # Check that the LLM was called once
            self.agent._execute_prompt.assert_called_once()
            
            # Check that the file was opened for writing at the correct path
            mocked_file.assert_called_once_with(output_path, "w")
            
            # Check that the correct content was written to the file
            mocked_file().write.assert_called_once_with(mock_markdown_plan)

if __name__ == "__main__":
    unittest.main()
