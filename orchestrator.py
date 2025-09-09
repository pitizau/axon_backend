# In file: orchestrator.py

import json
import logging
from typing import Dict, Any

from agents.source_agent import SourceAnalysisAgent
from agents.planning_agent import MigrationPlanAgent
from agents.transformation_agent import SchemaTransformationAgent
from agents.validation_agent import DataValidationAgent
from agents.optimization_agent import QueryOptimizationAgent
from tools.memory_manager import MemoryManager
from tools.database_connector import BaseConnector

class PipelineOrchestrator:
    """
    Orchestrates the entire multi-agent pipeline for database migration.
    """
    def __init__(
        self,
        connector: BaseConnector,
        memory_manager: MemoryManager,
        analysis_agent: SourceAnalysisAgent,
        planning_agent: MigrationPlanAgent,
        transformation_agent: SchemaTransformationAgent,
        validation_agent: DataValidationAgent,
        optimization_agent: QueryOptimizationAgent
    ):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.connector = connector
        self.memory_manager = memory_manager
        self.analysis_agent = analysis_agent
        self.planning_agent = planning_agent
        self.transformation_agent = transformation_agent
        self.validation_agent = validation_agent
        self.optimization_agent = optimization_agent
        
        # Define output paths
        self.plan_output_path = "output/migration_plan.md"
        self.sql_output_path = "output/schema.sql"
        self.validation_output_path = "output/validation_queries.sql"
        self.optimization_output_path = "output/optimization_suggestions.sql"

    def run_pipeline(self):
        """
        Executes the full, multi-step agentic pipeline.
        """
        self.logger.info("Starting Axon application pipeline...")
        full_context = ""
        try:
            # Load context from past runs
            self.logger.info("\n[PIPELINE] Loading context from memory...")
            past_runs = self.memory_manager.load_memories()
            if past_runs:
                full_context = json.dumps(past_runs, indent=2)

            # Step 1: Source Analysis
            self.logger.info("\n[PIPELINE] Running Step 1: Source Analysis...")
            analysis_report_str = self.analysis_agent.run(context=full_context)
            analysis_report_dict = json.loads(analysis_report_str)
            self.logger.info("--- Schema Analysis Report (Advanced) ---")
            self.logger.info(json.dumps(analysis_report_dict, indent=2))

            if analysis_report_dict.get("error"):
                raise ValueError("Source analysis failed. Halting pipeline.")

            # Step 2: Migration Planning
            self.logger.info("\n[PIPELINE] Running Step 2: Migration Planning...")
            self.planning_agent.run(
                schema_analysis=analysis_report_dict,
                output_path=self.plan_output_path,
                context=full_context
            )
            self.logger.info("--- Migration Plan Generated ---")
            self.logger.info(f"Plan saved to: {self.plan_output_path}")

            # Step 3: Schema Transformation
            self.logger.info("\n[PIPELINE] Running Step 3: Schema Transformation...")
            self.transformation_agent.run(
                schema_analysis=analysis_report_dict,
                output_path=self.sql_output_path,
                context=full_context
            )
            self.logger.info("--- SQL Schema Generated ---")
            self.logger.info(f"SQL script saved to: {self.sql_output_path}")
            
            # Step 4: Data Validation
            self.logger.info("\n[PIPELINE] Running Step 4: Data Validation...")
            self.validation_agent.run(
                schema_analysis=analysis_report_dict,
                generated_sql=analysis_report_dict.get("generated_sql", ""), # Placeholder
                output_path=self.validation_output_path,
                context=full_context
            )
            self.logger.info("--- Validation Queries Generated ---")
            self.logger.info(f"Validation script saved to: {self.validation_output_path}")

            # Step 5: Query Optimization
            self.logger.info("\n[PIPELINE] Running Step 5: Query Optimization...")
            self.optimization_agent.run(
                generated_sql=analysis_report_dict.get("generated_sql", ""), # Placeholder
                output_path=self.optimization_output_path,
                context=full_context
            )
            self.logger.info("--- Optimization Suggestions Generated ---")
            self.logger.info(f"Optimization script saved to: {self.optimization_output_path}")


            # Save the results of this run to memory
            self.logger.info("\n[PIPELINE] Saving results to memory...")
            self.memory_manager.save_memory({
                "source_analysis": analysis_report_dict,
                "migration_plan_path": self.plan_output_path,
                "generated_sql_path": self.sql_output_path,
                "validation_queries_path": self.validation_output_path,
                "optimization_suggestions_path": self.optimization_output_path
            })

        except Exception as e:
            self.logger.error(f"An application pipeline error occurred: {e}", exc_info=True)
