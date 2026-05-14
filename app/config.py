import os

from dotenv import load_dotenv



# LOAD ENV


load_dotenv()



# GROQ


GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)



# MODELS


LLM_MODEL = "llama-3.1-8b-instant"

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"



# RETRIEVAL


TOP_K = 10

