import numpy as np

from fastembed import TextEmbedding


embedding_model = TextEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)


def cosine_similarity_manual(query_vec, doc_matrix):

    query_norm = np.linalg.norm(query_vec)

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

def rerank(query, retrieved):

    if not retrieved:
        return []

    # =========================================
    # QUERY EMBEDDING
    # =========================================

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True
    )[0]

    # =========================================
    # BUILD DOCUMENTS
    # =========================================

    documents = []

    for item in retrieved:

        text = f"""
        Assessment: {item['name']}

        Description:
        {item['description']}

        Test Type:
        {item['test_type']}

        Skills:
        {item.get('keys', '')}
        """

        documents.append(text)

    # =========================================
    # DOCUMENT EMBEDDINGS
    # =========================================

    doc_embeddings = embedding_model.encode(
        documents,
        convert_to_numpy=True
    )

    # =========================================
    # COSINE SIMILARITY
    # =========================================

    similarities = cosine_similarity_manual(
        query_embedding,
        doc_embeddings
    )

    # =========================================
    # RANKING
    # =========================================

    ranked = []

    for score, item in zip(
        similarities,
        retrieved
    ):

        item["rerank_score"] = float(score)

        ranked.append(item)

    ranked.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return ranked[:10]

