import pickle
import numpy as np

from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer





# LOAD METADATA


with open("data/metadata.pkl", "rb") as f:

    metadata = pickle.load(f)



# BUILD DOCUMENTS


documents = []

for item in metadata:

    text = f"""
    Assessment: {item.get('name', '')}

    Description:
    {item.get('description', '')}

    Suitable For:
    {item.get('job_levels', '')}

    Categories:
    {item.get('test_type', '')}

    Skills:
    {item.get('keys', '')}

    Languages:
    {item.get('languages', '')}
    """

    documents.append(text)



# BM25 INDEX


tokenized_docs = [
    doc.lower().split()
    for doc in documents
]

bm25 = BM25Okapi(tokenized_docs)



# EMBEDDING MODEL


print("Loading embedding model...")

embedding_model = TextEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
)



# DOCUMENT EMBEDDINGS


print("Generating semantic embeddings...")

doc_embeddings = list(
    embedding_model.embed(documents)
)

doc_embeddings = np.array(
    doc_embeddings
)



# EXACT MATCH


catalog_by_name = {

    item["name"].lower(): item
    for item in metadata
}



# COSINE SIMILARITY


def cosine_similarity_manual(
    query_vec,
    doc_matrix
):

    query_norm = np.linalg.norm(
        query_vec
    )

    doc_norms = np.linalg.norm(
        doc_matrix,
        axis=1
    )

    similarities = np.dot(
        doc_matrix,
        query_vec
    ) / (
        doc_norms * query_norm + 1e-10
    )

    return similarities



# DOMAIN DETECTION


def detect_domain(query):

    query = query.lower()

    domain_map = {

        "software": [

            "software",
            "developer",
            "engineer",
            "programming",
            "coding",
            "backend",
            "frontend",
            "java",
            "python",
            "cloud",
            "agile"
        ],

        "finance": [

            "finance",
            "banking",
            "accounting",
            "audit"
        ],

        "sales": [

            "sales",
            "retail",
            "customer support"
        ],

        "leadership": [

            "leadership",
            "manager",
            "executive",
            "stakeholder"
        ]
    }

    for domain, terms in domain_map.items():

        for term in terms:

            if term in query:
                return domain

    return "general"



# DOMAIN BOOSTING


def apply_domain_boost(
    results,
    domain,
    query
):

    domain_terms = {

        "software": [

            "software",
            "developer",
            "technical",
            "programming",
            "coding",
            "java",
            "python",
            "agile",
            "automation",
            "testing"
        ],

        "finance": [

            "finance",
            "banking",
            "accounting"
        ],

        "sales": [

            "sales",
            "retail",
            "customer"
        ],

        "leadership": [

            "leadership",
            "manager",
            "executive",
            "stakeholder"
        ]
    }

    allowed_terms = domain_terms.get(
        domain,
        []
    )

    query_lower = query.lower()

    for item in results:

        combined = (
            str(item.get("name", ""))
            + " " +
            str(item.get("description", ""))
            + " " +
            str(item.get("keys", ""))
        ).lower()

        boost = 0

        for term in allowed_terms:

            if term in combined:
                boost += 0.05

        # ---------------------------------
        # Extra Technical Boost
        # ---------------------------------

        technical_terms = [

            "java",
            "python",
            "coding",
            "programming",
            "developer",
            "software"
        ]

        for term in technical_terms:

            if term in query_lower:

                if term in combined:

                    boost += 0.15

        item["semantic_score"] = (
            item.get("semantic_score", 0)
            + boost
        )

    return results



# BM25 SEARCH


def bm25_search(query, k=50):

    tokenized_query = (
        query.lower().split()
    )

    scores = bm25.get_scores(
        tokenized_query
    )

    top_indices = np.argsort(
        scores
    )[::-1][:k]

    results = []

    for idx in top_indices:

        item = metadata[idx].copy()

        item["bm25_score"] = float(
            scores[idx]
        )

        results.append(item)

    return results



# SEMANTIC SEARCH


def semantic_search(query, k=50):

    try:
        query_embedding = model.encode(
        [query],
        convert_to_numpy=True
        )[0]



        similarities = cosine_similarity_manual(
            query_embedding,
            doc_embeddings
        )

        top_indices = np.argsort(
            similarities
        )[::-1][:k]

        results = []

        for idx in top_indices:

            item = metadata[idx].copy()

            item["semantic_score"] = float(
                similarities[idx]
            )

            results.append(item)

        return results

    except Exception as e:

        print(
            "Semantic search error:",
            e
        )

        return []



# METADATA FILTERING


def filter_results(
    results,
    constraints=None
):

    if constraints is None:
        return results

    filtered = []

    for item in results:

        keep = True

        # -----------------------------
        # Remote
        # -----------------------------

        if constraints.get("remote"):

            if (
                str(
                    item.get("remote", "")
                ).lower()
                != "yes"
            ):

                keep = False

        # -----------------------------
        # Adaptive
        # -----------------------------

        if constraints.get("adaptive"):

            if (
                str(
                    item.get("adaptive", "")
                ).lower()
                != "yes"
            ):

                keep = False

        # -----------------------------
        # Personality
        # -----------------------------

        if constraints.get("personality"):

            combined = (
                str(item.get("keys", ""))
                + " " +
                str(item.get("test_type", ""))
            ).lower()

            if "personality" not in combined:

                keep = False

        if keep:

            filtered.append(item)

    return filtered



# PENALTIES


def apply_penalties(results):

    irrelevant_terms = [

        "geoinformatics",
        "instrumentation",
        "statistics",
        "call center",
        "chemical engineering",
        "civil engineering",
        "mechanical engineering"
    ]

    for item in results:

        combined = (
            str(item.get("name", ""))
            + " " +
            str(item.get("description", ""))
        ).lower()

        penalty = 0

        for term in irrelevant_terms:

            if term in combined:

                penalty -= 0.15

        item["hybrid_score"] += penalty

    return results



# HYBRID RETRIEVAL


def hybrid_retrieve(
    query,
    constraints=None,
    k=10
):

    bm25_results = bm25_search(
        query,
        k=50
    )

    semantic_results = semantic_search(
        query,
        k=50
    )

    merged = {}

    # -------------------------------------
    # Merge BM25
    # -------------------------------------

    for item in bm25_results:

        name = item["name"]

        if name not in merged:

            merged[name] = item

        merged[name]["bm25_score"] = (
            item.get("bm25_score", 0)
        )

    # -------------------------------------
    # Merge Semantic
    # -------------------------------------

    for item in semantic_results:

        name = item["name"]

        if name not in merged:

            merged[name] = item

        merged[name]["semantic_score"] = (
            item.get("semantic_score", 0)
        )

    results = list(
        merged.values()
    )

    # -------------------------------------
    # Domain Boosting
    # -------------------------------------

    domain = detect_domain(query)

    results = apply_domain_boost(
        results,
        domain,
        query
    )

    # -------------------------------------
    # Metadata Filtering
    # -------------------------------------

    results = filter_results(
        results,
        constraints
    )

    # -------------------------------------
    # Hybrid Scoring
    # -------------------------------------

    for item in results:

        semantic_score = item.get(
            "semantic_score",
            0
        )

        bm25_score = item.get(
            "bm25_score",
            0
        )

        item["hybrid_score"] = (
            semantic_score * 0.85
            +
            bm25_score * 0.15
        )

    # -------------------------------------
    # Penalties
    # -------------------------------------

    results = apply_penalties(
        results
    )

    # -------------------------------------
    # Final Sorting
    # -------------------------------------

    results.sort(
        key=lambda x: x["hybrid_score"],
        reverse=True
    )

    return results[:k]



# EXACT MATCH


def exact_match(name):

    return catalog_by_name.get(
        name.lower()
    )
