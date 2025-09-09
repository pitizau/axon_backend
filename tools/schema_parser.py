# In file: tools/schema_parser.py

import pandas as pd
from agents.base_agent import BaseAgent

class SchemaParser:
    """
    Parses and analyzes a database schema using a generative model.
    """
    def __init__(self, agent: BaseAgent):
        """
        Initializes the SchemaParser with an agent to use for analysis.
        Args:
            agent: An instance of a class that inherits from BaseAgent.
        """
        self.agent = agent

    def analyze_schema(self, schema_df: pd.DataFrame, analysis_prompt: str) -> str:
        """
        Analyzes the schema by formatting it and sending it to the agent's model.

        Args:
            schema_df: A pandas DataFrame representing the database schema.
            analysis_prompt: The prompt template for the analysis.

        Returns:
            A string containing the model's analysis of the schema.
        """
        schema_json = schema_df.to_json(orient='records', indent=2)
        prompt = analysis_prompt.format(schema_json=schema_json)
        
        analysis = self.agent._execute_prompt(prompt)
        return analysis