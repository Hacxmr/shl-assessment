# SHL Assessment Recommendation Agent Documentation

Author: Mitali Raj

---

# Overview

This project implements a retrieval-grounded conversational AI agent for recommending SHL assessments using FastAPI, semantic retrieval, Groq LLMs, and hybrid ranking.

The system supports:
- conversational recommendations
- clarification handling
- query refinement
- assessment comparison
- prompt injection protection
- evaluation using Recall@10 and RAGAS metrics

---

# Tech Stack

## Backend
- FastAPI
- Python 3.11

## Retrieval
- FastEmbed
- BM25
- Hybrid semantic ranking

## LLM
- Groq API
- llama-3.1-8b-instant

## Evaluation
- Recall@10
- RAGAS

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
├── config.py
│
scripts/
│
├── evaluate_recall.py
├── evaluate_ragas.py
│
evaluation/
│
├── test_cases.json
│
data/
│
├── metadata.pkl
├── catalog_raw.json
````

---

# Local Setup

## Clone Repository

```bash
git clone <repo_url>
cd shl-agent
```

---

# Create Virtual Environment

## Windows PowerShell

```powershell
python -m venv shl_env
```

Activate:

```powershell
.\shl_env\Scripts\Activate.ps1
```

---

# Install Dependencies

Using uv:

```bash
uv pip install -r requirements.txt
```

---

# Environment Variables

Create `.env`

```env
GROQ_API_KEY=your_groq_api_key
```

---

# Run FastAPI Server

```bash
uvicorn app.main:app
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

# API Endpoints

## GET /health

Health check endpoint.

### Response

```json
{
  "status": "ok"
}
```

---

## POST /chat

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

# Running Evaluation

## Recall@10

Run:

```bash
python -m scripts.evaluate_recall
```

Example:

```text
Mean Recall@10: 0.833
```

---

## RAGAS Metrics

Run:

```bash
python scripts/evaluate_ragas.py
```

Metrics:

* faithfulness
* answer relevancy
* context precision
* context recall

---

# Deployment

## Render Deployment

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
uvicorn app.main:app --host 0.0.0.0 --port 10000
```

### Environment Variables

```text
GROQ_API_KEY
```

---

# Public Endpoints

```text
https://your-app.onrender.com
```

Swagger Docs:

```text
https://your-app.onrender.com/docs
```

---

# Common Issues

## PowerShell Execution Policy

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

---

## Missing Module Errors

Always run evaluation scripts using:

```bash
python -m scripts.evaluate_recall
```

NOT:

```bash
python scripts/evaluate_recall.py
```

---

## ONNX Memory Errors

Close running uvicorn servers before evaluation:

```powershell
taskkill /F /IM python.exe
```

---

# Evaluation Summary

Current retrieval performance:

```text
Mean Recall@10 = 0.833
```

The system demonstrates:

* semantic retrieval
* grounded recommendation generation
* conversational clarification
* multi-turn refinement
* assessment comparison
* hallucination prevention


