import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_groq_client():
    """
    Returns a Groq client instance if the API key is set.
    Otherwise, raises a ValueError during runtime instead of at import time.
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set in the environment variables.")
    
    return Groq(api_key=GROQ_API_KEY)


if not GROQ_API_KEY:
    print("⚠️ Warning: GROQ_API_KEY not set")
