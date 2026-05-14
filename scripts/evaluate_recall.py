import json

from app.retriever import hybrid_retrieve


# =========================================
# LOAD TEST CASES
# =========================================

print("\nLOADING TEST CASES...\n")

with open(
    "evaluation/test_cases.json",
    encoding="utf-8"
) as f:

    test_cases = json.load(f)

print(
    f"Loaded {len(test_cases)} test cases\n"
)


# =========================================
# RECALL@10
# =========================================

all_scores = []

for case in test_cases:

    query = case["query"]

    # -------------------------------------
    # Normalize Ground Truth
    # -------------------------------------

    ground_truth = set(
        [
            x.lower().strip()
            for x in case["ground_truth"]
        ]
    )

    # -------------------------------------
    # Retrieval
    # -------------------------------------

    results = hybrid_retrieve(
        query=query,
        constraints={},
        k=10
    )

    # -------------------------------------
    # Normalize Predictions
    # -------------------------------------

    predicted = set(
        [
            item["name"].lower().strip()
            for item in results
        ]
    )

    # -------------------------------------
    # Partial Match Evaluation
    # -------------------------------------

    matched = 0

    for gt in ground_truth:

        for pred in predicted:

            if gt in pred or pred in gt:

                matched += 1
                break

    recall = (
        matched /
        len(ground_truth)
    )

    all_scores.append(recall)

    # -------------------------------------
    # Logging
    # -------------------------------------

    print("=" * 60)

    print("QUERY:")
    print(query)
    print()

    print("GROUND TRUTH:")
    print(ground_truth)
    print()

    print("PREDICTED:")
    print(predicted)
    print()

    print(
        f"Recall@10: "
        f"{recall:.2f}"
    )

    print()


# =========================================
# FINAL SCORE
# =========================================

if len(all_scores) > 0:

    mean_recall = (
        sum(all_scores) /
        len(all_scores)
    )

    print("=" * 60)

    print(
        f"Mean Recall@10: "
        f"{mean_recall:.3f}"
    )

else:

    print(
        "No evaluation scores generated."
    )

