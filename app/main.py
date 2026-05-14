from fastapi import FastAPI
import traceback

from app.schemas import (
    ChatRequest,
    ChatResponse,
    Recommendation
)

from app.guardrails import (
    detect_offtopic,
    detect_injection
)

from app.retriever import (
    hybrid_retrieve
)

from app.conversation import (
    extract_constraints,
    needs_clarification,
    is_comparison_query
)

from app.llm import (
    generate_response
)

from app.prompts import (
    build_recommendation_prompt,
    build_comparison_prompt,
    build_clarification_prompt
)



# FASTAPI APP


app = FastAPI(
    title="SHL Assessment Recommendation API",
    version="1.0.0"
)





# HEALTH CHECK


@app.get("/health")
def health():

    return {
        "status": "ok"
    }



# CHAT ENDPOINT


@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(req: ChatRequest):

    try:

        
        # Latest User Message
        

        latest_user = req.messages[-1].content

        
        # Guardrails
        

        if detect_offtopic(latest_user):

            return {
                "reply": (
                    "I only assist with "
                    "SHL assessment recommendations."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        if detect_injection(latest_user):

            return {
                "reply": (
                    "Prompt injection attempt detected."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        
        # Clarification Handling
        

        if needs_clarification(req.messages):

            prompt = build_clarification_prompt(
                req.messages
            )

            reply = generate_response(prompt)

            return {
                "reply": reply,
                "recommendations": [],
                "end_of_conversation": False
            }

        
        # Build Conversation Text
        

        full_text = " ".join(
            [
                m.content
                for m in req.messages
            ]
        )

        
        # Extract Constraints
        

        constraints = extract_constraints(
            req.messages
        )

        
        # Comparison Query
        

        if is_comparison_query(req.messages):

            results = hybrid_retrieve(
                query=full_text,
                constraints=constraints,
                k=5
            )

            prompt = build_comparison_prompt(
                full_text,
                results
            )

            reply = generate_response(prompt)

            recommendations = []

            for item in results[:2]:

                recommendations.append(
                    Recommendation(
                        name=item["name"],
                        url=item.get("url")
                        or "https://www.shl.com",
                        test_type=item["test_type"]
                    )
                )

            return {
                "reply": reply,
                "recommendations": recommendations,
                "end_of_conversation": False
            }

        
        # Retrieval
        

        results = hybrid_retrieve(
            query=full_text,
            constraints=constraints,
            k=5
        )

        
        # Recommendation Prompt
        

        prompt = build_recommendation_prompt(
            full_text,
            results
        )

        
        # Generate LLM Response
        

        reply = generate_response(prompt)

        
        # Structured Recommendations
        

        recommendations = []

        for item in results:

            recommendations.append(
                Recommendation(
                    name=item["name"],
                    url=item.get("url")
                    or "https://www.shl.com",
                    test_type=item["test_type"]
                )
            )

        
        # Final Response
        

        return {
            "reply": reply,
            "recommendations": recommendations,
            "end_of_conversation": True
        }

    except Exception as e:

        print("\n========== ERROR ==========")
        traceback.print_exc()
        print("===========================\n")

        return {
            "reply": str(e),
            "recommendations": [],
            "end_of_conversation": False
        }

