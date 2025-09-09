# In file: tests/test_source_analysis.py

import unittest
import json
from unittest.mock import MagicMock
from agents.source_agent import SourceAnalysisAgent
from tools.database_connector import MockConnector

class TestSourceAnalysisAgent(unittest.TestCase):
    """Unit tests for the SourceAnalysisAgent."""

    def test_run_full_process(self):
        """
        Tests that the agent can run its full analysis process and now
        returns a structured JSON error if the model response is bad.
        """
        # Use the MockConnector for this test
        mock_connector = MockConnector()
        
        # Create the agent
        agent = SourceAnalysisAgent(
            connector=mock_connector,
            model_name="test-model",
            project="test-project",
            location="us-central1"
        )
        
        # Mock the _execute_prompt to return a valid JSON string this time
        mock_llm_response = """
        ```json
        {
          "summary": "This is a successful analysis.",
          "key_tables": [],
          "relationships": []
        }
        ```
        """
        agent._execute_prompt = MagicMock(return_value=mock_llm_response)
        
        # Run the agent
        result = agent.run()
        
        # Assertions
        # Check that the result is a valid JSON string
        report_dict = json.loads(result)
        self.assertIn("summary", report_dict)
        self.assertEqual(report_dict["summary"], "This is a successful analysis.")
        agent._execute_prompt.assert_called_once() # Verify the LLM was called

if __name__ == "__main__":
    unittest.main()
