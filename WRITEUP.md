# WRITEUP.md

# SHL Conversational Assessment Recommendation Agent

Author: Mitali Raj

---

# 1. Problem Understanding

The objective was to build a conversational recommendation agent over the SHL assessment catalog that could:

* clarify vague hiring requests
* recommend grounded SHL assessments
* support conversational refinement
* compare assessments
* refuse off-topic or malicious requests

The system also had to remain stateless, expose FastAPI endpoints, and ensure all recommendations were strictly grounded in the SHL product catalog.

The core challenge was balancing:

* conversational flexibility
* retrieval quality
* grounding
* robustness

while operating under strict API and evaluation constraints.

---

# 2. Design Philosophy

The system prioritizes:

* grounding over generation
* deterministic control over fully autonomous reasoning
* retrieval precision over broad recommendation coverage
* conversational robustness over long-form reasoning

The overall design intentionally separates:

* deterministic logic
* retrieval
* prompt construction
* LLM response generation

This improved controllability, reduced hallucinations, and made conversational behavior easier to debug and evaluate.

---

# 3. System Architecture

The final system follows a retrieval-grounded conversational agent architecture.

Pipeline:

```text
User Query
↓
Guardrails
↓
Clarification Detection
↓
Constraint Extraction
↓
Hybrid Retrieval
↓
Prompt Construction
↓
LLM Response Generation
↓
Structured Recommendation Output
```

The architecture was designed to:

* minimize hallucinations
* preserve retrieval grounding
* support stateless conversations
* maintain predictable behavior during multi-turn interactions

---

# 4. Catalog Processing

The SHL catalog was scraped and converted into a structured JSON dataset.

Each assessment stores:

* assessment name
* description
* catalog URL
* test type
* remote support
* adaptive support
* job levels
* skills/categories

The processed catalog was serialized into metadata objects for retrieval.

---

# 5. Retrieval Strategy

The retrieval system evolved through multiple iterations.

## Initial Retrieval Approach

The first implementation relied primarily on:

* keyword matching
* TF-IDF similarity

This produced poor semantic generalization and frequently surfaced irrelevant assessments.

Example failure:

* software engineering queries retrieving unrelated engineering assessments.

---

## Final Retrieval Pipeline

The final retrieval pipeline combines:

### BM25 Retrieval

BM25 retrieval provides strong lexical matching for:

* exact skills
* assessment names
* technical terminology

This improved precision for:

* Java
* Python
* Agile
* leadership
* personality assessment queries

---

### Semantic Retrieval

Semantic retrieval uses:

* SentenceTransformers
* `BAAI/bge-small-en-v1.5`

This improved:

* synonym handling
* semantic understanding
* conversational robustness
* retrieval recall

---

### Hybrid Ranking

The final ranking combines:

* semantic similarity
* BM25 relevance
* metadata filtering

This hybrid setup produced substantially more stable recommendations than either approach independently.

---

### Metadata Filtering

Constraints extracted from conversation history are applied during retrieval.

Supported filters include:

* remote support
* adaptive testing
* personality testing
* seniority
* communication requirements

This improved conversational refinement quality.

---

### Diversity Penalty Filtering

Additional penalties suppress unrelated domains such as:

* instrumentation engineering
* geoinformatics
* chemical engineering

This reduced retrieval noise for software-focused queries.

---

# 6. Conversational Design

The system supports the four required conversational behaviors.

---

## Clarification Handling

The agent asks follow-up questions only when insufficient hiring context exists.

Example:

```text
User: I need an assessment
Assistant: Which role or skills are you hiring for?
```

The initial implementation used LLM-based clarification detection, but this caused:

* excessive questioning
* unnecessary latency
* unstable conversational flow

The final implementation uses lightweight deterministic logic based on:

* role signals
* skill constraints
* hiring intent

This significantly improved conversational stability.

---

## Conversational Refinement

The system supports conversational updates such as:

* “Actually include personality tests”
* “Add communication assessment”
* “Need remote-friendly options”

The full conversation history is processed every turn, enabling stateless refinement without storing server-side session memory.

---

## Assessment Comparison

Comparison queries such as:

```text
Compare OPQ32r and MQM5
```

trigger a specialized comparison prompt using retrieved catalog context.

This prevents the LLM from relying on unsupported prior knowledge.

---

# 7. Guardrails

The system includes lightweight deterministic guardrails for:

* prompt injection attempts
* off-topic requests
* unrelated legal/salary advice

Examples refused:

* “Ignore previous instructions”
* “What salary should I offer?”
* “Recommend non-SHL products”

Deterministic keyword-based guardrails were preferred over LLM moderation to:

* reduce latency
* avoid unnecessary API calls
* improve reliability

---

# 8. Prompt Engineering

Prompt design focused heavily on grounding and scope control.

The prompts explicitly instruct the model to:

* recommend only retrieved assessments
* avoid hallucinating URLs or capabilities
* remain within SHL scope
* produce concise recruiter-friendly responses

Separate prompts are used for:

* recommendations
* clarification
* comparisons

This improved controllability and reduced hallucination frequency.

---

# 9. LLM Choice

The final implementation uses:

* Groq API
* `llama-3.1-8b-instant`

Reasons:

* low latency
* free access tier
* fast inference
* strong instruction following

Earlier experiments used deprecated Groq models which caused API failures and required migration.

---

# 10. API Design

The API follows the required stateless design.

Endpoints:

* `GET /health`
* `POST /chat`

The full conversation history is passed on every request.

Responses strictly follow the required schema.

---

# 11. Error Handling & Deployment

The system includes:

* structured exception handling
* URL fallback handling
* deployment-safe startup logic
* debugging tracebacks

The application was deployed publicly using Railway.

Deployment challenges included:

* embedding model memory usage
* cold-start latency
* dynamic port handling
* dependency conflicts

These were resolved through:

* lazy embedding loading
* optimized startup behavior
* Railway-compatible start commands
* dependency cleanup

---

# 12. Evaluation Strategy

The system was evaluated against:

* vague queries
* conversational refinement
* comparison requests
* prompt injection attempts
* off-topic requests
* conversational corrections

Evaluation focused on:

* schema compliance
* retrieval quality
* grounded recommendations
* conversational coherence
* hallucination prevention

---

## Recall@10 Evaluation

The retrieval pipeline was evaluated using manually curated benchmark queries.

Current performance:

```text
Mean Recall@10 = 0.833
```

Evaluation scenarios included:

* technical assessment recommendation
* personality assessment retrieval
* adaptive assessment retrieval
* comparison scenarios
* refinement scenarios

---

# 13. Challenges & Lessons

## Over-Clarification

Initial LLM-based clarification logic produced excessive follow-up questions.

Fix:

* deterministic clarification logic

---

## Retrieval Noise

Semantic retrieval occasionally surfaced irrelevant engineering assessments.

Fix:

* hybrid ranking
* metadata filtering
* diversity penalties

---

## Deployment Stability

Early deployment attempts failed due to:

* embedding memory usage
* dependency conflicts
* model deprecations
* environment configuration issues

Fix:

* lazy loading
* optimized embeddings
* safer dependency management
* Railway-compatible deployment configuration

---

# 14. Future Improvements

Potential future improvements include:

* cross-encoder reranking
* vector database integration
* streaming responses
* evaluation automation
* structured skill ontology
* embedding caching
* conversation replay benchmarking

---

# 15. Conclusion

The final system is a retrieval-grounded conversational recommendation agent that:

* supports realistic recruiter workflows
* remains grounded in the SHL catalog
* supports clarification and refinement
* compares assessments safely
* avoids hallucinations
* follows the required stateless API design

The implementation prioritizes grounding, controllability, and conversational robustness over purely generative behavior.

---

# Deployment

Public API Endpoint:

https://shl-agent-production-1576.up.railway.app

Swagger Docs:

https://shl-agent-production-1576.up.railway.app/docs
