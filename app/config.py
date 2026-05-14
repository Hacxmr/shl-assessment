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

EMBED_MODEL = "BAAI/bge-small-en-v1.5"



# RETRIEVAL


TOP_K = 10

