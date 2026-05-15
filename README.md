# SHL Conversational Assessment Recommendation Agent

<p align="center">

<img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python" />
<img src="https://img.shields.io/badge/FastAPI-API-green?style=for-the-badge&logo=fastapi" />
<img src="https://img.shields.io/badge/Groq-LLM-orange?style=for-the-badge" />
<img src="https://img.shields.io/badge/SentenceTransformers-Embeddings-red?style=for-the-badge" />
<img src="https://img.shields.io/badge/BM25-Retrieval-purple?style=for-the-badge" />
<img src="https://img.shields.io/badge/Railway-Deployed-black?style=for-the-badge&logo=railway" />

</p>

A retrieval-grounded conversational AI agent for recommending SHL assessments through multi-turn dialogue.

Built for the SHL Labs AI Intern take-home assignment.

---

# Live Deployment

## API Base URL

https://shl-agent-production-1576.up.railway.app

## Swagger Documentation

https://shl-agent-production-1576.up.railway.app/docs

---

# Features

- Conversational SHL assessment recommendation
- Multi-turn dialogue support
- Semantic + BM25 hybrid retrieval
- Constraint-aware recommendations
- Query refinement handling
- Assessment comparison support
- Prompt injection detection
- Off-topic query refusal
- Grounded response generation
- Recall@10 evaluation pipeline
- RAGAS evaluation support
- FastAPI REST API deployment

---

# System Architecture

![System Architecture](https://raw.githubusercontent.com/Hacxmr/shl-assessment/main/diagram-shl.png)

The system combines BM25 lexical retrieval with semantic embedding retrieval to ground recommendations in the SHL assessment catalog. Retrieved assessments are reranked using semantic similarity and filtered through conversational constraints before grounded response generation using Groq-hosted LLMs.

---

# Tech Stack

## Backend

- FastAPI
- Python 3.11

## LLM

- Groq API
- llama-3.1-8b-instant

## Retrieval

- SentenceTransformers
- BAAI/bge-small-en-v1.5 embeddings
- BM25 retrieval
- Hybrid semantic ranking
- Cosine similarity reranking
- Metadata filtering

## Evaluation

- Recall@10
- RAGAS metrics

## Data

- SHL Product Catalog
- JSON-based catalog store

---

# Deployment Status

- Public API deployed on Railway
- Swagger documentation enabled
- Multi-turn conversational support enabled
- Retrieval evaluation pipeline included

---

# API Endpoints

## GET `/`

Root endpoint.

### Response

```json
{
  "message": "SHL Assessment Recommendation API is running"
}
```

---

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

Conversational recommendation endpoint.

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

# Example Queries

- Need adaptive coding assessments for backend engineers
- Compare OPQ32r and MQM5
- Need remote assessments for graduate software engineers
- Need leadership assessments for senior managers
- Include personality and communication testing

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
User: Compare OPQ32r and MQM5
```

---

## Guardrails

The agent refuses:

- prompt injection attempts
- legal advice
- salary discussions
- unrelated queries
- non-SHL recommendations

---

# Retrieval Pipeline

1. BM25 retrieval
2. Semantic embedding retrieval
3. Hybrid ranking
4. Cosine similarity reranking
5. Metadata filtering
6. Diversity-aware ranking

---

# Evaluation

## Recall@10

The retrieval system is evaluated using manually curated benchmark queries.

### Current Performance

```text
Mean Recall@10 = 0.833
```

### Evaluation Coverage

- technical assessment recommendation
- personality assessment retrieval
- adaptive assessment retrieval
- conversational refinement
- comparison scenarios
- guardrail robustness

---

## RAGAS Metrics

Supported evaluation metrics:

- Faithfulness
- Context Precision
- Context Recall
- Answer Relevancy

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
│
README.md
DOCUMENTATION.md
Dockerfile
requirements.txt
.gitignore
diagram-shl.png
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

---

## Local Server

```text
http://127.0.0.1:8000
```

## Swagger Docs

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

# Railway Deployment

## Railway Start Command

```bash
sh -c 'uvicorn app.main:app --host 0.0.0.0 --port $PORT'
```

---

# Future Improvements

- Cross-encoder reranking
- Better ranking calibration
- Evaluation automation
- Streaming responses
- Catalog metadata enrichment
- Conversation replay benchmarking
- Caching semantic embeddings

---

# Author

Mitali Raj
