import json

from datasets import Dataset

from ragas import evaluate

from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)

from app.retriever import hybrid_retrieve
from app.prompts import build_recommendation_prompt
from app.llm import generate_response



# LOAD TEST CASES


with open(
    "evaluation/test_cases.json",
    encoding="utf-8"
) as f:

    test_cases = json.load(f)



# BUILD RAGAS DATASET


samples = []

print(result)