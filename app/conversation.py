import json

from app.llm import generate_response


# =========================================
# CONSTRAINT EXTRACTION
# =========================================

def extract_constraints(messages):

    conversation = "\n".join(
        [
            f"{m.role}: {m.content}"
            for m in messages
        ]
    )

    prompt = f"""
Extract hiring constraints from the conversation.

Return ONLY valid JSON.

Schema:
{{
    "role": string or null,
    "seniority": string or null,
    "remote": boolean,
    "adaptive": boolean,
    "personality": boolean,
    "max_duration": integer or null,
    "skills": [string]
}}

Conversation:
{conversation}
"""

    response = generate_response(prompt)

    try:

        constraints = json.loads(
            response
        )

    except:

        constraints = {}

    return constraints


# =========================================
# CLARIFICATION DETECTION
# =========================================

def needs_clarification(messages):

    text = " ".join(
        [
            m.content.lower()
            for m in messages
        ]
    )

    # -------------------------------------
    # Role Signals
    # -------------------------------------

    role_terms = [

        "engineer",
        "developer",
        "manager",
        "analyst",
        "sales",
        "support",
        "software",
        "java",
        "python",
        "graduate",
        "executive"
    ]

    # -------------------------------------
    # Hiring Constraints
    # -------------------------------------

    constraint_terms = [

        "remote",
        "adaptive",
        "communication",
        "teamwork",
        "stakeholder",
        "personality",
        "leadership",
        "technical",
        "coding"
    ]

    has_role = any(
        term in text
        for term in role_terms
    )

    has_constraints = any(
        term in text
        for term in constraint_terms
    )

    # -------------------------------------
    # Clarify ONLY if insufficient info
    # -------------------------------------

    return not (
        has_role or has_constraints
    )


# =========================================
# COMPARISON QUERY
# =========================================

def is_comparison_query(messages):

    text = " ".join(
        [
            m.content.lower()
            for m in messages
        ]
    )

    comparison_terms = [

        "difference",
        "compare",
        "vs",
        "versus"
    ]

    return any(
        term in text
        for term in comparison_terms
    )


# =========================================
# REFINEMENT QUERY
# =========================================

def is_refinement_query(messages):

    text = " ".join(
        [
            m.content.lower()
            for m in messages
        ]
    )

    refinement_terms = [

        "also",
        "add",
        "instead",
        "actually",
        "update",
        "include"
    ]

    return any(
        term in text
        for term in refinement_terms
    )

