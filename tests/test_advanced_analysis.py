# In file: tests/test_advanced_analysis.py

import unittest
import pandas as pd
import json
from unittest.mock import MagicMock, patch
from agents.source_agent import SourceAnalysisAgent
from tools.csv_connector import CsvConnector
from tools.schema_parser import SchemaParser

class TestAdvancedAnalysis(unittest.TestCase):
    """
    Tests for the advanced source analysis capabilities (Step 3).
    """

    def setUp(self):
        """Set up a mock agent and connector for testing."""
        self.mock_connector = CsvConnector(filepath="dummy_path.csv")
        
        self.agent = SourceAnalysisAgent(
            connector=self.mock_connector,
            model_name="test-model",
            project="test-project",
            location="us-central1"
        )

    def test_csv_connector_get_schema(self):
        """Tests that the CsvConnector can read a schema from a CSV."""
        csv_data = "table_name,column_name,data_type\nusers,id,int\nusers,name,string"
        
        # We use patch from unittest.mock to simulate reading a file
        with patch("pandas.read_csv", return_value=pd.read_csv(pd.io.common.StringIO(csv_data))) as mock_read_csv:
            schema = self.mock_connector.get_schema()
            self.assertIsInstance(schema, pd.DataFrame)
            self.assertEqual(len(schema), 2)
            mock_read_csv.assert_called_with("dummy_path.csv")

    def test_schema_parser_handles_structured_json(self):
        """Tests that the SchemaParser can correctly parse a JSON response."""
        # This is the kind of raw response we expect from the LLM
        mock_llm_response = """
        ```json
        {
          "summary": "Test summary.",
          "key_tables": [],
          "relationships": []
        }
        ```
        """
        self.agent._execute_prompt = MagicMock(return_value=mock_llm_response)
        
        parser = SchemaParser(agent=self.agent)
        schema_df = pd.DataFrame({'a': [1]}) # Dummy dataframe
        
        result = parser.analyze_schema(schema_df, "dummy prompt")
        
        self.assertIsInstance(result, dict)
        self.assertIn("summary", result)
        self.assertEqual(result["summary"], "Test summary.")

    def test_agent_run_produces_json_string(self):
        """Tests that the agent's final output is a valid JSON string."""
        mock_analysis = {
            "summary": "Database for customers and orders.",
            "key_tables": [{"table_name": "orders", "role": "Fact", "description": "Stores order data."}],
            "relationships": []
        }
        # Mock the schema parser to return a dictionary directly
        self.agent.schema_parser.analyze_schema = MagicMock(return_value=mock_analysis)
        # Mock the connector to prevent file operations
        self.agent.connector.connect = MagicMock()
        self.agent.connector.disconnect = MagicMock()
        self.agent.connector.get_schema = MagicMock(return_value=pd.DataFrame({'a': [1]}))
        
        result_str = self.agent.run()
        
        self.assertIsInstance(result_str, str)
        # Verify it's a valid JSON string
        result_dict = json.loads(result_str)
        self.assertEqual(result_dict["summary"], "Database for customers and orders.")


if __name__ == "__main__":
    unittest.main()
