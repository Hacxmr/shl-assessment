import os

from dotenv import load_dotenv
from groq import Groq



# LOAD ENV VARIABLES


load_dotenv()



# READ API KEY


GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

print("GROQ KEY FOUND:", bool(GROQ_API_KEY))



# VALIDATE


if not GROQ_API_KEY:

    raise ValueError(
        "GROQ_API_KEY missing in .env"
    )



# CREATE CLIENT


client = Groq(
    api_key=GROQ_API_KEY
)


MODEL_NAME = "llama-3.1-8b-instant"



# GENERATE RESPONSE


def generate_response(prompt):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

