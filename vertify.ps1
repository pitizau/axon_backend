#
# Axon Project Verification Script (for Windows PowerShell)
# This script sets up the environment, runs the main application,
# and executes the unit tests.
#

# Stop the script if any command fails
$ErrorActionPreference = "Stop"

Write-Host "========================================="
Write-Host "  AXON PROJECT VERIFICATION SCRIPT       "
Write-Host "========================================="

# --- 1. Environment Setup ---
Write-Host "`n[STEP 1/4] Setting up Python virtual environment..."
if (-not (Test-Path -Path "venv")) {
    python -m venv venv
    Write-Host "  -> Virtual environment 'venv' created."
} else {
    Write-Host "  -> Virtual environment 'venv' already exists."
}

# Activate the virtual environment (Windows syntax)
. .\venv\Scripts\Activate.ps1
Write-Host "  -> Virtual environment activated."


# --- 2. Install Dependencies ---
Write-Host "`n[STEP 2/4] Installing project dependencies..."
pip install -q -r requirements.txt
Write-Host "  -> Dependencies from requirements.txt are installed."


# --- 3. Run the Main Application ---
Write-Host "`n[STEP 3/4] Running the main application (main.py)..."
Write-Host "-------------------------------------------------"
python main.py
Write-Host "-------------------------------------------------"
Write-Host "  -> Main application executed."


# --- 4. Run Unit Tests ---
Write-Host "`n[STEP 4/4] Discovering and running unit tests..."
Write-Host "-------------------------------------------------"
python -m unittest discover tests
Write-Host "-------------------------------------------------"
Write-Host "  -> Unit tests executed."


Write-Host "`n========================================="
Write-Host "  VERIFICATION COMPLETE                  "
Write-Host "========================================="