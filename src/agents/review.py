import os
# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq
# pyrefly: ignore [missing-import]
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any

from src.state import TripState

def run_review_agent(state: TripState) -> Dict[str, Any]:
    """
    Uses Groq to review the synthesized draft itinerary against original constraints.
    """
    retry_count = state.get("retry_count", 0) + 1
    
    if retry_count >= 3:
        print("Review Agent: Maximum retry limit reached. Forcing terminal failure.")
        return {
            "review_status": "terminal_failure",
            "review_feedback": ["Maximum retry limit reached. The requested constraints might be impossible."],
            "retry_count": retry_count,
            "final_itinerary": state.get("draft_itinerary", {})
        }
        
    from src.llm import get_llm
    llm = get_llm(temperature=0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are the final Quality Assurance Reviewer for a travel planning agency. Your job is to strictly evaluate the draft itinerary against the user's original constraints. Check if the trip fits within the requested days, visits the required cities, stays within budget, aligns with preferences, and avoids what they want to avoid. If it passes, output a final approved JSON itinerary. If it fails, output specific feedback on what needs to be fixed. Output JSON strictly like: {{'status': 'passed' or 'failed', 'feedback': [], 'final_itinerary': {{}}}}"),
        ("human", "Original Constraints: {constraints}\n\nDraft Itinerary Context (Destination, Logistics, Budget):\n{draft}")
    ])
    
    chain = prompt | llm
    
    print(f"Review Agent: Evaluating draft itinerary (Attempt {retry_count})...")
    draft_str = f"Destination Plan: {state.get('destination_plan')}\n" \
                f"Logistics Plan: {state.get('logistics_plan')}\n" \
                f"Budget Plan: {state.get('budget_plan')}"
                
    response = chain.invoke({
        "constraints": state.get("constraints", {}),
        "draft": draft_str
    })
    
    return {
        "review_status": "evaluated",
        "review_feedback": [response.content],
        "retry_count": retry_count
    }
