# In file: agents/source_analysis.py

from agents.base_agent import BaseAgent
from tools.database_connector import BaseConnector
from tools.schema_parser import SchemaParser
from prompts.source_analysis_prompt import SCHEMA_ANALYSIS_PROMPT

class SourceAnalysisAgent(BaseAgent):
    """
    An agent that analyzes the schema of a source database system.
    """
    def __init__(self, connector: BaseConnector, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connector = connector
        self.schema_parser = SchemaParser(agent=self)
        self.logger.info("SourceAnalysisAgent initialized.")

    def run(self) -> str:
        """
        Executes the full schema analysis process.
        
        Returns:
            A string containing the final schema analysis report.
        """
        self.logger.info("Starting source analysis...")
        
        try:
            self.connector.connect()
            schema_df = self.connector.get_schema()
            
            if schema_df.empty:
                self.logger.warning("Schema is empty. No analysis to perform.")
                return "Schema is empty. No analysis performed."

            self.logger.info(f"Schema retrieved with {len(schema_df)} columns.")
            
            analysis_report = self.schema_parser.analyze_schema(
                schema_df, 
                SCHEMA_ANALYSIS_PROMPT
            )
            
            self.logger.info("Schema analysis complete.")
            return analysis_report
            
        except Exception as e:
            self.logger.error(f"An error occurred during source analysis: {e}")
            return f"Error: {e}"
        finally:
            self.connector.disconnect()