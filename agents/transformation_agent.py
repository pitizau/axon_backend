# In file: agents/transformation_agent.py

import json
from typing import Dict, Any
from agents.base_agent import BaseAgent
from prompts.transformation_prompt import TRANSFORMATION_PROMPT
from tools.sql_writer import SqlWriter

class SchemaTransformationAgent(BaseAgent):
    """
    An agent that transforms a JSON schema analysis into SQL DDL statements.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sql_writer = SqlWriter()
        self.logger.info("SchemaTransformationAgent initialized.")

    def run(self, schema_analysis: Dict[str, Any], output_path: str) -> None:
        """
        Executes the schema to SQL transformation process.

        Args:
            schema_analysis: The structured schema analysis from the SourceAnalysisAgent.
            output_path: The file path to save the generated SQL DDL.
        """
        self.logger.info("Starting schema to SQL transformation...")

        try:
            # Convert the analysis dictionary back to a JSON string for the prompt
            analysis_json_str = json.dumps(schema_analysis, indent=2)
            
            # Create the prompt for the transformation agent
            prompt = TRANSFORMATION_PROMPT.format(schema_analysis_json=analysis_json_str)

            # Execute the prompt to get the SQL DDL
            generated_sql = self._execute_prompt(prompt)
            
            # Use the SqlWriter tool to save the SQL
            self.sql_writer.save_sql(
                sql_content=generated_sql,
                output_path=output_path
            )

            self.logger.info(f"SQL DDL successfully generated and saved to {output_path}")

        except Exception as e:
            self.logger.error(f"An error occurred during schema transformation: {e}", exc_info=True)
            error_content = f"-- SQL Generation Failed\n-- An error occurred: {e}"
            self.sql_writer.save_sql(sql_content=error_content, output_path=output_path)
