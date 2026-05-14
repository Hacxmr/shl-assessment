# Approach Document

## SHL Conversational Assessment Recommendation Agent

Author: Mitali Raj

---

# 1. Problem Understanding

The task was to build a conversational recommendation agent over the SHL assessment catalog that could:

- Clarify vague hiring requests
- Recommend grounded SHL assessments
- Handle conversational refinements
- Compare assessments
- Refuse off-topic or malicious requests

The system also had to remain stateless, operate through FastAPI endpoints, and ensure all recommendations were strictly grounded in the SHL catalog.

---

# 2. System Design

The final system follows a retrieval-grounded conversational agent architecture.

Pipeline:

```text id="hbjlwm"
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
````

The architecture intentionally separates:

* deterministic logic
* retrieval
* LLM reasoning

This reduced hallucinations and improved controllability.

---

# 3. Catalog Processing

The SHL catalog was scraped and converted into a structured JSON dataset.

Each assessment stores:

* name
* description
* URL
* test type
* remote support
* adaptive support
* job levels
* skills/categories

The catalog was indexed for semantic retrieval.

---

# 4. Retrieval Strategy

The retrieval system evolved through multiple iterations.

## Initial Version

The first implementation relied heavily on:

* keyword matching
* TF-IDF similarity

This produced weak semantic generalization and irrelevant recommendations.

Example failure:

* software engineering queries retrieving unrelated engineering assessments.

---

## Final Retrieval Pipeline

The final retrieval pipeline combines:

### Semantic Embeddings

Using:

* FastEmbed
* `BAAI/bge-small-en-v1.5`

This improved:

* semantic understanding
* synonym handling
* conversational robustness

---

### Hybrid Retrieval

The system combines:

* semantic similarity
* metadata filtering
* reranking

Constraints such as:

* remote support
* personality testing
* adaptive testing
* seniority

are applied during retrieval.

---

### TF-IDF Reranking

Retrieved results are reranked using TF-IDF cosine similarity to improve precision.

This reduced retrieval noise and improved Recall@10.

---

### Diversity Penalty Filtering

Additional penalties suppress unrelated domains such as:

* instrumentation
* geoinformatics
* chemical engineering

This improved recommendation quality for software engineering roles.

---

# 5. Conversational Design

The system supports four required behaviors.

---

## Clarification

The agent asks follow-up questions only when insufficient hiring context exists.

Example:

* “I need an assessment”

Clarification detection was initially implemented using the LLM directly, but this caused excessive questioning and latency.

The final implementation uses lightweight deterministic logic based on:

* role signals
* hiring constraints

This improved responsiveness and conversational stability.

---

## Refinement

The agent supports conversational updates such as:

* “Actually include personality tests”
* “Add communication assessment”

The full conversation history is processed each turn to support stateless refinement.

---

## Comparison

Comparison queries such as:

* “Compare OPQ and GSA”

trigger a specialized comparison prompt using grounded catalog retrieval.

This avoids relying on LLM prior knowledge.

---

# 6. Guardrails

The system includes lightweight guardrails for:

* prompt injection attempts
* off-topic requests
* unrelated legal/salary advice

Examples refused:

* “Ignore previous instructions”
* “What salary should I offer?”

The guardrails intentionally use deterministic keyword matching rather than LLM moderation to reduce latency and prevent unnecessary API calls.

---

# 7. Prompt Engineering

Prompt design focused heavily on grounding.

The prompts explicitly instruct the model to:

* recommend only retrieved assessments
* avoid hallucination
* remain within SHL scope
* generate concise recruiter-friendly responses

Separate prompts are used for:

* recommendations
* clarification
* comparisons

---

# 8. LLM Choice

The final implementation uses:

* Groq API
* `llama-3.1-8b-instant`

Reasons:

* low latency
* free access tier
* strong instruction following
* fast conversational inference

Earlier experiments used deprecated Groq models which caused API failures and were replaced.

---

# 9. API Design

The API follows the required stateless design.

Endpoints:

* `GET /health`
* `POST /chat`

The full conversation history is sent on every request.

Responses strictly follow the required schema.

---

# 10. Error Handling

The system includes:

* exception handling
* URL fallback handling
* safe response generation
* debugging tracebacks

This improved robustness during evaluation and deployment.

---

# 11. Evaluation Strategy

The system was manually tested against:

* vague queries
* multi-turn refinement
* comparison requests
* prompt injection attempts
* off-topic requests
* conversational corrections

Evaluation focused on:

* schema compliance
* grounded recommendations
* conversational coherence
* retrieval quality
* hallucination prevention

---

# 12. Challenges & Lessons

## Main Challenges

### Over-clarification

The initial LLM-based clarification logic asked too many follow-up questions.

Fix:

* deterministic clarification logic

---

### Retrieval Noise

Semantic retrieval occasionally surfaced unrelated engineering assessments.

Fix:

* reranking
* metadata filtering
* diversity penalties

---

### API Stability

Early implementations crashed due to:

* invalid URLs
* model deprecations
* missing environment variables

Fix:

* safer validation
* exception handling
* updated Groq models

---

# 13. Future Improvements

Potential future improvements include:

* cross-encoder reranking
* evaluation automation
* conversation memory scoring
* better ranking calibration
* structured skill ontology
* streaming responses
* vector database integration

---

# 14. Conclusion

The final system is a retrieval-grounded conversational recommendation agent that:

* supports realistic recruiter workflows
* remains grounded in the SHL catalog
* handles refinement and comparison
* avoids hallucinations
* follows the required stateless API design

The project prioritizes controllability, grounding, and conversational robustness over purely generative behavior.


