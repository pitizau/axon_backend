# In file: agents/validation_agent.py

import json
from typing import Dict, Any
from agents.base_agent import BaseAgent
from prompts.validation_prompt import VALIDATION_PROMPT
from tools.sql_writer import SqlWriter

class DataValidationAgent(BaseAgent):
    """
    An agent that generates SQL validation queries based on a schema analysis.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sql_writer = SqlWriter()
        self.logger.info("DataValidationAgent initialized.")

    def run(self, schema_analysis: Dict[str, Any], output_path: str, context: str = "") -> None:
        """
        Generates and saves SQL validation queries.

        Args:
            schema_analysis: The structured analysis from the SourceAnalysisAgent.
            output_path: The file path for the validation SQL script.
            context: Optional context from previous runs.
        """
        self.logger.info("Starting data validation planning...")
        try:
            analysis_json_str = json.dumps(schema_analysis, indent=2)
            
            prompt = VALIDATION_PROMPT.format(
                schema_analysis_json=analysis_json_str,
                context=context
            )

            validation_sql = self._execute_prompt(prompt)
            
            self.sql_writer.save_sql(
                sql_content=validation_sql,
                output_path=output_path
            )
            self.logger.info(f"Validation SQL successfully generated and saved to {output_path}")

        except Exception as e:
            self.logger.error(f"An error occurred during data validation: {e}", exc_info=True)
            error_content = f"-- Validation SQL Generation Failed\n-- An error occurred: {e}"
            self.sql_writer.save_sql(sql_content=error_content, output_path=output_path)
