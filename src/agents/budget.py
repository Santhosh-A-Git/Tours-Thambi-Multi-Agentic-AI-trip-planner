import os
import requests
# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq
# pyrefly: ignore [missing-import]
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any

from src.state import TripState
from src.scraper import scrape_japan_travel_data

def get_exchange_rate() -> float:
    try:
        response = requests.get("https://api.frankfurter.app/latest?from=USD&to=JPY")
        data = response.json()
        return data["rates"]["JPY"]
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return 150.0  # Fallback rough estimate

def run_budget_agent(state: TripState) -> Dict[str, Any]:
    """
    Uses Groq, scraped WikiVoyage data, and live exchange rates to estimate costs.
    """
    print("Budget Agent: Fetching budget and exchange rate data...")
    cities = state.get("constraints", {}).get("cities", [])
    scraped_data = scrape_japan_travel_data(cities)
    
    budget_content = scraped_data.get("budget", "")[:1500]
    
    exchange_rate = get_exchange_rate()
    print(f"Budget Agent: Current USD to JPY exchange rate is {exchange_rate}")
    
    from src.llm import get_llm
    llm = get_llm(temperature=0.2)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Japan travel budget planner. Based on the scraped WikiVoyage 'Budget' text below, estimate the daily and total costs for the user's trip. Break down the costs into Stay, Transport, Food, and Activities. Flag if the plan is too expensive based on their constraints. The current exchange rate is 1 USD = {exchange_rate} JPY. Output a concise JSON structure (e.g., {{'total_cost': 0, 'breakdown': {{}}, 'is_over_budget': false, 'flags': []}}).\n\nWikiVoyage Context:\n{wiki_context}"),
        ("human", "My trip constraints: {constraints}")
    ])
    
    chain = prompt | llm
    
    print("Budget Agent: Generating budget plan...")
    response = chain.invoke({
        "wiki_context": budget_content,
        "exchange_rate": exchange_rate,
        "constraints": state.get("constraints", {})
    })
    
    return {"budget_plan": {"raw_budget": response.content}}

