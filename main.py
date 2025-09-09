# In file: main.py

import logging
from config.logging_config import setup_logging
from config import settings
# Corrected import statement:
from agents.source_agent import SourceAnalysisAgent
from tools.database_connector import MockConnector

def main():
    """The main entry point for the application."""
    setup_logging()
    logging.info("Starting Axon application...")

    try:
        # 1. Create a database connector (using the mock for now)
        mock_connector = MockConnector()

        # 2. Create the SourceAnalysisAgent
        analysis_agent = SourceAnalysisAgent(
            connector=mock_connector,
            model_name=settings.GEMINI_MODEL_NAME,
            project=settings.GCP_PROJECT_ID,
            location=settings.GCP_REGION
        )
        
        # 3. Run the agent and get the report
        report = analysis_agent.run()
        
        logging.info("--- Schema Analysis Report ---")
        print(report)
        logging.info("--- End of Report ---")

    except Exception as e:
        logging.error(f"An application error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()