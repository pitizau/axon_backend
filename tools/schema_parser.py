# In file: tools/schema_parser.py

import pandas as pd
import json
import logging
from agents.base_agent import BaseAgent
from typing import Dict, Any

class SchemaParser:
    """
    Parses and analyzes a database schema using a generative model.
    """
    def __init__(self, agent: BaseAgent):
        self.agent = agent
        self.logger = logging.getLogger(self.__class__.__name__)

    # CORRECTED: Added the 'context' parameter to the function definition
    def analyze_schema(self, schema_df: pd.DataFrame, analysis_prompt: str, context: str = "") -> Dict[str, Any]:
        """
        Analyzes the schema by formatting it and sending it to the agent's model.

        Args:
            schema_df: A pandas DataFrame representing the database schema.
            analysis_prompt: The prompt template for the analysis.
            context: Optional context from previous pipeline runs.
        """
        try:
            schema_json = schema_df.to_json(orient='records', indent=2)
            
            prompt = analysis_prompt.format(
                schema_json=schema_json,
                context=context
            )
            
            analysis_str = self.agent._execute_prompt(prompt)
            
            analysis_dict = json.loads(analysis_str)
            self.logger.info("Successfully parsed structured JSON from model response.")
            return analysis_dict
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Could not parse JSON from model response: {e}")
            return {
                "error": "Failed to parse JSON response from the model.",
                "raw_response": analysis_str
            }
        except Exception as e:
            self.logger.error(f"An unexpected error occurred in schema analysis: {e}")
            return {
                "error": "An unexpected error occurred.",
                "details": str(e)
            }

