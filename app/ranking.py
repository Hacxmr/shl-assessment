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

    query_embedding = list(
        embedding_model.embed([query])
    )[0]

    documents = []

    for item in retrieved:

        text = f"""
        Assessment: {item['name']}

        Description:
        {item['description']}

        Test Type:
        {item['test_type']}

        Skills:
        {item['keys']}
        """

        documents.append(text)

    doc_embeddings = list(
        embedding_model.embed(documents)
    )

    query_embedding = np.array(
        query_embedding
    )

    doc_embeddings = np.array(
        doc_embeddings
    )

    similarities = cosine_similarity_manual(
        query_embedding,
        doc_embeddings
    )

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

