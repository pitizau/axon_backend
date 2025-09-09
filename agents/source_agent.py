# In file: agents/source_agent.py

import json
from agents.base_agent import BaseAgent
from tools.database_connector import BaseConnector
from tools.schema_parser import SchemaParser
from prompts.source_analysis_prompt import SCHEMA_ANALYSIS_PROMPT_ADVANCED

class SourceAnalysisAgent(BaseAgent):
    """
    An agent that analyzes the schema of a source database system.
    """
    def __init__(self, connector: BaseConnector, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connector = connector
        self.schema_parser = SchemaParser(agent=self)
        self.logger.info("SourceAnalysisAgent initialized.")

    # CORRECTED: Added context parameter with a default value
    def run(self, context: str = "") -> str:
        """
        Executes the full schema analysis process.
        
        Args:
            context: Optional context from previous pipeline runs.

        Returns:
            A string containing the final schema analysis report as a JSON object.
        """
        self.logger.info("Starting source analysis...")
        
        try:
            self.connector.connect()
            schema_df = self.connector.get_schema()
            
            if schema_df.empty:
                self.logger.warning("Schema is empty. No analysis to perform.")
                return json.dumps({"status": "error", "message": "Schema is empty."})

            self.logger.info(f"Schema retrieved with {len(schema_df)} columns.")
            
            # Pass the context to the schema parser
            analysis_report_dict = self.schema_parser.analyze_schema(
                schema_df, 
                SCHEMA_ANALYSIS_PROMPT_ADVANCED,
                context
            )
            
            self.logger.info("Schema analysis complete.")
            return json.dumps(analysis_report_dict, indent=2)
            
        except Exception as e:
            self.logger.error(f"An error occurred during source analysis: {e}", exc_info=True)
            return json.dumps({"status": "error", "message": str(e)})
        finally:
            self.connector.disconnect()

