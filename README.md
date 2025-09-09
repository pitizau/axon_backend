# Axon: An Agentic Backend for Automated Database Migration

**Project Status: Completed**

Axon is a sophisticated, multi-agent backend system designed to automate the complex process of database migration. Built entirely in Python and powered by Google's Vertex AI and Gemini models, Axon re-engineers a linear data analysis process into a dynamic, intelligent, and scalable pipeline. The system is managed and monitored through a real-time web interface.

This project was developed iteratively through a comprehensive 8-step plan, with each step building upon the last to create a robust and feature-complete application.

## Key Features

* **Multi-Agent Pipeline**: A coordinated team of specialized AI agents handles distinct tasks: schema analysis, migration planning, SQL code generation, validation, and optimization.

* **Live AI Integration**: The system is fully connected to Google's Vertex AI, leveraging the Gemini 1.5 Pro model for all intelligent tasks.

* **Continuous Learning**: Axon features a memory system (`output/memory.json`) that allows it to learn from previous runs, improving the context and quality of future outputs.

* **Modular and Scalable Architecture**: The codebase is organized into distinct modules for agents, tools, prompts, and configuration, making it easy to maintain and extend.

* **Live Web Dashboard**: A Flask and Socket.IO-based user interface provides real-time status updates and displays the generated artifacts as the pipeline runs.

* **Comprehensive Unit Testing**: The project includes a full suite of unit tests, ensuring the reliability and correctness of each component.

## Directory Structure

The project is organized into the following directories:

* `agents/`: Contains the core logic for each specialized AI agent.

* `config/`: Centralized configuration for GCP settings, model parameters, and logging.

* `data/`: Holds the input data sources (e.g., `source_schema.csv`).

* `logs/`: Stores detailed log files from application runs.

* `output/`: The destination for all generated artifacts, including the migration plan, SQL scripts, and memory file.

* `prompts/`: Manages the prompts used to instruct the language models.

* `tests/`: Contains all unit tests for the project.

* `tools/`: Reusable modules that provide capabilities to the agents (e.g., database connectors, file writers).

* `ui/`: Contains the Flask server and HTML/CSS/JS for the web dashboard.

## How to Run the Axon System

Follow these steps to set up and run the application.

### 1. Prerequisites

* Python 3.10+ and `pip` installed.

* A Google Cloud Platform (GCP) project with the Vertex AI API enabled.

* The `gcloud` CLI installed and authenticated on your local machine. Run `gcloud auth application-default login` to set up your credentials.

### 2. Install Dependencies

First, set up and activate a Python virtual environment:

```
# Create the virtual environment (only needs to be done once)
python -m venv venv

# Activate the virtual environment (do this every time you open a new terminal)
.\venv\Scripts\Activate.ps1

```

Then, install the required Python packages:

```
pip install -r requirements.txt

```

### 3. Run the Web UI

To run the full application with its real-time dashboard, start the Flask web server:

```
python ui/server.py

```

Now, open your web browser and navigate to **https://www.google.com/search?q=http://127.0.0.1:5001**. Click the "Run Pipeline" button to start the process.

### 4. Run the Verification Script (Tests Only)

If you only want to run the unit tests without starting the UI, you can use the PowerShell verification script:

```
powershell.exe -ExecutionPolicy Bypass -File .\vertify.ps1

```

## The Implementation Journey

The Axon backend was built by completing the following 8-step implementation plan:

| **Step** | **Description** | **Status** | 
| 1 | Foundational Setup & Base Agent | Complete | 
| 2 | Source Analysis Agent (Core) | Complete | 
| 3 | Source Analysis Agent (Advanced) | Complete | 
| 4 | Migration Planning Agent | Complete | 
| 5 | Schema Transformation Agent | Complete | 
| 6 | Vector DB & Continuous Learning | Complete | 
| 7 | Data Validation & Optimization | Complete | 
| 8 | Pipeline Orchestration & Live API | Complete | 