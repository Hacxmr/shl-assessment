# SHL Conversational Assessment Recommendation Agent

A retrieval-grounded conversational AI agent for recommending SHL assessments through multi-turn dialogue.

Built for the SHL Labs AI Intern take-home assignment.

---

# Features

- Conversational assessment recommendation
- Semantic retrieval over SHL catalog
- Multi-turn clarification handling
- Query refinement support
- Assessment comparison support
- Prompt injection detection
- Off-topic refusal
- FastAPI REST API
- Groq-powered grounded response generation
- Recall@10 evaluation pipeline
- RAGAS evaluation support

---

# System Architecture
![System Architecture](https://raw.githubusercontent.com/Hacxmr/shl-assessment/main/diagram-shl.png)



---

# Tech Stack

## Backend

* FastAPI
* Python 3.11

## LLM

* Groq API
* llama-3.1-8b-instant

## Retrieval

* FastEmbed
* BAAI/bge-small-en-v1.5 embeddings
* BM25 retrieval
* Hybrid semantic ranking
* TF-IDF reranking

## Evaluation

* Recall@10
* RAGAS metrics

## Data

* SHL Product Catalog
* JSON-based catalog store

---

# API Endpoints

## GET `/health`

Health check endpoint.

### Response

```json
{
  "status": "ok"
}
```

---

## POST `/chat`

Stateless conversational recommendation endpoint.

### Request

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Need remote assessments for software engineers"
    }
  ]
}
```

### Response

```json
{
  "reply": "Recommended assessments include Agile Software Development and Business Communication.",
  "recommendations": [
    {
      "name": "Agile Software Development",
      "url": "https://www.shl.com/...",
      "test_type": "Knowledge & Skills"
    }
  ],
  "end_of_conversation": false
}
```

---

# Supported Behaviors

## Clarification Handling

The agent asks follow-up questions when insufficient hiring context exists.

### Example

```text
User: I need an assessment
Assistant: Which role or skills are you hiring for?
```

---

## Query Refinement

The agent updates recommendations when constraints change.

### Example

```text
User: Actually include personality assessments
```

---

## Assessment Comparison

The agent compares assessments using grounded catalog context.

### Example

```text
User: Compare OPQ and GSA
```

---

## Guardrails

The agent refuses:

* prompt injection attempts
* legal advice
* salary discussions
* unrelated queries
* non-SHL recommendations

---

# Retrieval Pipeline

1. BM25 retrieval
2. Semantic embedding retrieval
3. Hybrid ranking
4. TF-IDF reranking
5. Metadata filtering
6. Diversity penalty filtering

---

# Evaluation

## Recall@10

The retrieval system is evaluated using Recall@10 over manually curated benchmark queries.

### Current Performance

```text
Mean Recall@10 = 0.833
```

---

## RAGAS Metrics

Supported evaluation metrics:

* Faithfulness
* Context Precision
* Context Recall
* Answer Relevancy

---

# Project Structure

```text
app/
│
├── main.py
├── retriever.py
├── llm.py
├── prompts.py
├── schemas.py
├── conversation.py
├── guardrails.py
├── ranking.py
├── utils.py
├── config.py
│
data/
│
├── catalog_raw.json
├── metadata.pkl
│
evaluation/
│
├── test_cases.json
│
scripts/
│
├── evaluate_recall.py
├── evaluate_ragas.py
│
tests/
│
├── test_api.py
```

---

# Running Locally

## 1. Create Virtual Environment

### Windows PowerShell

```powershell
python -m venv shl_env
```

Activate:

```powershell
.\shl_env\Scripts\Activate.ps1
```

---

## 2. Install Dependencies

```bash
uv pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Create `.env`

```env
GROQ_API_KEY=your_key_here
```

---

## 4. Start FastAPI Server

```bash
uvicorn app.main:app --reload
```

Server:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

# Running Evaluation

## Recall@10

```bash
python -m scripts.evaluate_recall
```

---

## RAGAS Evaluation

```bash
python scripts.evaluate_ragas.py
```

---

# Deployment

Recommended deployment:

* Render
* Railway

## Start Command

```bash
uvicorn app.main:app --host 0.0.0.0 --port 10000
```

---

# Future Improvements

* Cross-encoder reranking
* Better ranking calibration
* Evaluation automation
* Streaming responses
* Catalog metadata enrichment
* Conversation replay benchmarking

---

# Author

Mitali Raj

