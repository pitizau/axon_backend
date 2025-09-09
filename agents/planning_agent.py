# In file: agents/planning_agent.py

import json
from typing import Dict, Any
from agents.base_agent import BaseAgent
from prompts.planning_prompt import MIGRATION_PLAN_PROMPT
from tools.plan_writer import PlanWriter

class MigrationPlanAgent(BaseAgent):
    """
    An agent that takes a schema analysis and generates a high-level
    migration plan.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plan_writer = PlanWriter()
        self.logger.info("MigrationPlanAgent initialized.")

    def run(self, schema_analysis: Dict[str, Any], output_path: str) -> None:
        """
        Executes the full migration planning process.

        Args:
            schema_analysis: The structured schema analysis from the SourceAnalysisAgent.
            output_path: The file path to save the generated migration plan.
        """
        self.logger.info("Starting migration planning...")

        try:
            # Convert the analysis dictionary back to a JSON string for the prompt
            analysis_json_str = json.dumps(schema_analysis, indent=2)
            
            # Create the prompt for the planning agent
            prompt = MIGRATION_PLAN_PROMPT.format(schema_analysis_json=analysis_json_str)

            # Execute the prompt to get the migration plan
            migration_plan_markdown = self._execute_prompt(prompt)
            
            # Use the PlanWriter tool to save the plan
            self.plan_writer.save_plan(
                plan_content=migration_plan_markdown,
                output_path=output_path
            )

            self.logger.info(f"Migration plan successfully generated and saved to {output_path}")

        except Exception as e:
            self.logger.error(f"An error occurred during migration planning: {e}", exc_info=True)
            # As a fallback, save an error message to the output file
            error_content = f"# Migration Plan Generation Failed\n\nAn error occurred: {e}"
            self.plan_writer.save_plan(plan_content=error_content, output_path=output_path)
