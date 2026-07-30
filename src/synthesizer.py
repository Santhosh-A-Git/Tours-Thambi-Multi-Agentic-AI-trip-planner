import os
# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq
# pyrefly: ignore [missing-import]
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any

from src.state import TripState

def run_synthesizer(state: TripState) -> Dict[str, Any]:
    """
    Takes the outputs from Destination, Logistics, and Budget agents,
    and synthesizes them into a single coherent draft itinerary.
    """
    print("Synthesizer: Compiling draft itinerary...")
    
    from src.llm import get_llm
    llm = get_llm(temperature=0.3)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a master travel itinerary compiler. Combine the destination, logistics, and budget plans into a single, cohesive, day-by-day draft itinerary. Ensure all constraints are respected. Output the itinerary ONLY in a beautifully formatted Markdown layout that is easy to review. Do NOT output JSON."),
        ("human", "Constraints: {constraints}\n\nDestination Plan:\n{destination}\n\nLogistics Plan:\n{logistics}\n\nBudget Plan:\n{budget}")
    ])
    
    chain = prompt | llm
    
    response = chain.invoke({
        "constraints": state.get("constraints", {}),
        "destination": state.get("destination_plan", {}),
        "logistics": state.get("logistics_plan", {}),
        "budget": state.get("budget_plan", {})
    })
    
    return {"draft_itinerary": {"raw_itinerary": response.content}}
