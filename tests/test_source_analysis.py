# In file: tests/test_source_analysis.py

import unittest
from unittest.mock import MagicMock
from agents.source_analysis import SourceAnalysisAgent
from tools.database_connector import MockConnector

class TestSourceAnalysisAgent(unittest.TestCase):
    """Unit tests for the SourceAnalysisAgent."""

    def test_run_full_process(self):
        """
        Tests that the agent can run its full analysis process.
        """
        # Use the MockConnector for this test
        mock_connector = MockConnector()
        
        # Create the agent
        agent = SourceAnalysisAgent(
            connector=mock_connector,
            model_name="test-model",
            project="test-project",
            location="test-location"
        )
        
        # Mock the _execute_prompt method to avoid a real API call
        agent._execute_prompt = MagicMock(return_value="This is a successful analysis.")
        
        # Run the agent
        result = agent.run()
        
        # Assertions
        self.assertIn("successful analysis", result)
        agent._execute_prompt.assert_called_once() # Verify the LLM was called

if __name__ == "__main__":
    unittest.main()