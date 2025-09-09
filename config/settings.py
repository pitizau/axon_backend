# In file: config/settings.py

import os

# Google Cloud Platform settings
GCP_PROJECT_ID = "ncau-data-nprod-aitrain"
GCP_REGION = "us-central1"

# Gemini Model Configuration
GEMINI_MODEL_NAME = "gemini-2.5-pro"
GEMINI_TEMPERATURE = 0.5
GEMINI_MAX_OUTPUT_TOKENS = 8192

# Logging Configuration
LOGS_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
LOG_FILE = os.path.join(LOGS_DIR, "axon.log")
