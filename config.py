# ============================================================
# config.py
# ============================================================
# STEP 1: Central Configuration Loader
#
# This is the first file that loads when the app starts.
# It reads all environment variables from the .env file and
# makes them available as Python constants to every module.
#
# WHY: Having a single config.py prevents scattered os.getenv()
# calls across files and makes it easy to change settings in
# one place.
# ============================================================

import os
from dotenv import load_dotenv

# --- STEP 1.1: Load the .env file ---
# load_dotenv() reads the .env file in the project root
# and injects all values into the system environment.
load_dotenv()

# ============================================================
# LLM PROVIDER SETTINGS
# ============================================================

# Groq API Key (required when using Groq as LLM provider)
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

# Default Groq model to use for extraction
GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Ollama base URL (required when using Local LLM as provider)
# Default: http://localhost:11434
OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Default local model name running inside Ollama
# Examples: llama3, mistral, phi3, gemma2
OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3")

# ============================================================
# DATABASE SETTINGS
# ============================================================

# SQLite database file URL (auto-created on first app run)
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///project_manager.db")

# ============================================================
# APPLICATION SETTINGS
# ============================================================

# Name of the app displayed in the Streamlit browser tab
APP_TITLE: str = "AI Project Manager"

# Subtitle shown under the main header
APP_SUBTITLE: str = "Transform Meeting Notes into Structured Tasks using LLMs"

# List of available LLM providers in the sidebar selector
LLM_PROVIDERS: list = ["Groq Cloud", "Local LLM (Ollama)"]

# Priority options for task dropdowns
PRIORITY_OPTIONS: list = ["High", "Medium", "Low"]

# Status options for task dropdowns
STATUS_OPTIONS: list = ["Todo", "In Progress", "Done"]

# Input source types for the input selector tabs
INPUT_SOURCES: list = ["📝 Text", "📄 PDF", "📃 DOCX", "📧 Email", "💬 Slack"]
