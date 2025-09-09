# In file: tools/schema_parser.py

import pandas as pd
import json
import logging
from agents.base_agent import BaseAgent
from typing import Dict, Any

class SchemaParser:
    """
    Parses and analyzes a database schema using a generative model,
    now with structured JSON output.
    """
    def __init__(self, agent: BaseAgent):
        """
        Initializes the SchemaParser with an agent to use for analysis.
        Args:
            agent: An instance of a class that inherits from BaseAgent.
        """
        self.agent = agent
        self.logger = logging.getLogger(self.__class__.__name__)

    def analyze_schema(self, schema_df: pd.DataFrame, analysis_prompt: str) -> Dict[str, Any]:
        """
        Analyzes the schema by formatting it and sending it to the agent's model.
        It now expects and parses a JSON string response.

        Args:
            schema_df: A pandas DataFrame representing the database schema.
            analysis_prompt: The prompt template for the analysis.

        Returns:
            A dictionary containing the structured analysis from the model.
        """
        schema_json = schema_df.to_json(orient='records', indent=2)
        prompt = analysis_prompt.format(schema_json=schema_json)
        
        raw_response = self.agent._execute_prompt(prompt)
        
        try:
            # Clean the response to extract only the JSON part
            # The model might return the JSON inside a markdown code block (` ```json ... ``` `)
            if "```json" in raw_response:
                json_part = raw_response.split("```json")[1].split("```")[0]
            else:
                json_part = raw_response

            parsed_analysis = json.loads(json_part)
            self.logger.info("Successfully parsed structured JSON from model response.")
            return parsed_analysis
        except (json.JSONDecodeError, IndexError) as e:
            self.logger.error(f"Could not parse JSON from model response: {e}")
            self.logger.debug(f"Raw response was: {raw_response}")
            # Return a structured error message
            return {
                "error": "Failed to parse JSON response from the model.",
                "raw_response": raw_response
            }
