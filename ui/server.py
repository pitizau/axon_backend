# In file: ui/server.py

from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import sys
import os

# Adjust path to import from the root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from orchestrator import PipelineOrchestrator
from config import settings
from tools.csv_connector import CsvConnector
from tools.memory_manager import MemoryManager
from agents.source_agent import SourceAnalysisAgent
from agents.planning_agent import MigrationPlanAgent
from agents.transformation_agent import SchemaTransformationAgent
from agents.validation_agent import DataValidationAgent
from agents.optimization_agent import QueryOptimizationAgent
from main import setup_data_source

app = Flask(__name__, template_folder='.')
socketio = SocketIO(app, cors_allowed_origins="*")

def run_axon_pipeline():
    """Initializes and runs the full Axon pipeline, emitting status updates."""
    
    socketio.emit('status_update', {'step': 'setup', 'status': 'running', 'message': 'Setting up components...'})
    
    # 1. Setup external components
    schema_file_path = setup_data_source()
    connector = CsvConnector(file_path=schema_file_path)
    memory_manager = MemoryManager(memory_file="output/memory.json")

    # 2. Initialize all agents
    analysis_agent = SourceAnalysisAgent(connector=connector, model_name=settings.GEMINI_MODEL_NAME, project=settings.GCP_PROJECT_ID, location=settings.GCP_REGION)
    planning_agent = MigrationPlanAgent(model_name=settings.GEMINI_MODEL_NAME, project=settings.GCP_PROJECT_ID, location=settings.GCP_REGION)
    transformation_agent = SchemaTransformationAgent(model_name=settings.GEMINI_MODEL_NAME, project=settings.GCP_PROJECT_ID, location=settings.GCP_REGION)
    validation_agent = DataValidationAgent(model_name=settings.GEMINI_MODEL_NAME, project=settings.GCP_PROJECT_ID, location=settings.GCP_REGION)
    optimization_agent = QueryOptimizationAgent(model_name=settings.GEMINI_MODEL_NAME, project=settings.GCP_PROJECT_ID, location=settings.GCP_REGION)
    
    # 3. Initialize the orchestrator, passing the socketio instance
    orchestrator = PipelineOrchestrator(
        connector=connector,
        memory_manager=memory_manager,
        analysis_agent=analysis_agent,
        planning_agent=planning_agent,
        transformation_agent=transformation_agent,
        validation_agent=validation_agent,
        optimization_agent=optimization_agent,
        socketio=socketio # Pass socketio for real-time updates
    )
    
    orchestrator.run_pipeline()
    socketio.emit('status_update', {'step': 'finished', 'status': 'complete', 'message': 'Pipeline finished.'})


@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@socketio.on('start_pipeline')
def handle_start_pipeline():
    """Handles the start event from the client and runs the pipeline in a new thread."""
    print("Client requested to start the pipeline. Starting in a new thread.")
    thread = threading.Thread(target=run_axon_pipeline)
    thread.start()

if __name__ == '__main__':
    print("Starting Axon UI server at http://127.0.0.1:5001")
    socketio.run(app, port=5001, debug=True, allow_unsafe_werkzeug=True)
