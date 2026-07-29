import os
from typing import List
# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq
# pyrefly: ignore [missing-import]
from langchain_core.prompts import ChatPromptTemplate
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field

from src.state import TripState

class ConstraintsModel(BaseModel):
    destination: str = Field(description="The destination country or region, e.g., Japan")
    cities: List[str] = Field(description="List of cities to visit")
    duration_days: int = Field(description="Total duration of the trip in days")
    budget_usd: int = Field(description="Total budget for the trip in USD")
    preferences: List[str] = Field(description="List of user preferences, e.g., food, temples")
    avoid: List[str] = Field(description="List of things the user wants to avoid, e.g., crowds")

def parse_request(request: str) -> TripState:
    """
    Takes a natural language request, uses Groq to parse it into constraints,
    and returns an initialized TripState.
    """
    # Initialize Groq LLM (Ensure GROQ_API_KEY is in environment variables)
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0) 
    
    # Use structured output to force the LLM to return data in the ConstraintsModel format
    structured_llm = llm.with_structured_output(ConstraintsModel)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert travel project manager. Extract the travel constraints from the user's request. If a specific budget is not given, default to 3000. If cities are not given but a country is, extract the country."),
        ("human", "{request}")
    ])
    
    chain = prompt | structured_llm
    
    constraints_output = chain.invoke({"request": request})
    
    # Initialize the state
    state: TripState = {
        "request": request,
        "constraints": constraints_output.dict(),
        "destination_plan": {},
        "logistics_plan": {},
        "budget_plan": {},
        "draft_itinerary": {},
        "final_itinerary": {},
        "review_status": "pending",
        "review_feedback": [],
        "retry_count": 0
    }
    
    return state
