import os

# Google Cloud Platform settings
GCP_PROJECT_ID = "ncau-data-nprod-aitrain"
GCP_REGION = "us-central1"

# Gemini Model Configuration
GEMINI_MODEL_NAME = "gemini-1.5-pro"

# Vector Search Configuration
VECTOR_SEARCH_ENDPOINT = "your-vector-search-endpoint"

# Logging Configuration
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
LOG_FILE = os.path.join(LOGS_DIR, "axon.log")