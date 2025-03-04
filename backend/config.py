import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Global Variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "../data/products.json")

# Ensure API Key is available
if not OPENAI_API_KEY:
    raise ValueError("⚠️ OPENAI_API_KEY is missing from the .env file")
