# In file: main.py

import logging
import os
import json
import datetime
from config.logging_config import setup_logging
from config import settings
from agents.source_agent import SourceAnalysisAgent
from agents.planning_agent import MigrationPlanAgent
from agents.transformation_agent import SchemaTransformationAgent
from tools.csv_connector import CsvConnector
from tools.memory_manager import MemoryManager # Import the new tool

def main():
    """The main entry point for the application."""
    setup_logging()
    logging.info("Starting Axon application pipeline...")

    try:
        # --- Setup Tools ---
        memory_manager = MemoryManager()
        
        # --- Create a dummy CSV file for the CsvConnector to use ---
        schema_csv_path = "data/source_schema.csv"
        os.makedirs(os.path.dirname(schema_csv_path), exist_ok=True)
        with open(schema_csv_path, "w") as f:
            f.write("table_name,column_name,data_type\n")
            f.write("customers,customer_id,INTEGER\n")
            f.write("customers,customer_name,VARCHAR\n")
            f.write("orders,order_id,INTEGER\n")
            f.write("orders,customer_id,INTEGER\n")
            f.write("orders,order_date,TIMESTAMP\n")

        # === PRE-PIPELINE: Load Context from Memory ===
        logging.info("\n[PIPELINE] Loading context from memory...")
        context = memory_manager.get_context_for_prompt()

        # === STEP 1: Run Source Analysis Agent ===
        logging.info("\n[PIPELINE] Running Step 1: Source Analysis...")
        csv_connector = CsvConnector(filepath=schema_csv_path)
        analysis_agent = SourceAnalysisAgent(
            connector=csv_connector,
            model_name=settings.GEMINI_MODEL_NAME,
            project=settings.GCP_PROJECT_ID,
            location=settings.GCP_REGION
        )
        analysis_report_str = analysis_agent.run(context=context)
        analysis_report_dict = json.loads(analysis_report_str)
        
        logging.info("--- Schema Analysis Report (Advanced) ---")
        print(analysis_report_str)
        
        if "error" in analysis_report_dict:
            logging.error("Source analysis failed. Halting pipeline.")
            return

        # === STEP 2: Run Migration Planning Agent ===
        logging.info("\n[PIPELINE] Running Step 2: Migration Planning...")
        planning_agent = MigrationPlanAgent(
            model_name=settings.GEMINI_MODEL_NAME,
            project=settings.GCP_PROJECT_ID,
            location=settings.GCP_REGION
        )
        plan_output_path = "output/migration_plan.md"
        planning_agent.run(
            schema_analysis=analysis_report_dict,
            output_path=plan_output_path,
            context=context
        )
        logging.info(f"--- Migration Plan Generated ---")
        logging.info(f"Plan saved to: {plan_output_path}")
        
        # === STEP 3: Run Schema Transformation Agent ===
        logging.info("\n[PIPELINE] Running Step 3: Schema Transformation...")
        transformation_agent = SchemaTransformationAgent(
            model_name=settings.GEMINI_MODEL_NAME,
            project=settings.GCP_PROJECT_ID,
            location=settings.GCP_REGION
        )
        sql_output_path = "output/schema.sql"
        transformation_agent.run(
            schema_analysis=analysis_report_dict,
            output_path=sql_output_path,
            context=context
        )
        logging.info(f"--- SQL Schema Generated ---")
        logging.info(f"SQL script saved to: {sql_output_path}")

        # === POST-PIPELINE: Save Results to Memory ===
        logging.info("\n[PIPELINE] Saving results to memory...")
        new_memory = {
            "timestamp": datetime.datetime.now().isoformat(),
            "analysis": analysis_report_dict,
            "plan_file": plan_output_path,
            "sql_file": sql_output_path
        }
        memory_manager.save_memory(new_memory)

    except Exception as e:
        logging.error(f"An application pipeline error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()

