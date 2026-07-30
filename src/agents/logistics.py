import os
# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq
# pyrefly: ignore [missing-import]
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any

from src.state import TripState
from src.scraper import scrape_japan_travel_data

def run_logistics_agent(state: TripState) -> Dict[str, Any]:
    """
    Uses Groq and live DuckDuckGo Search data to plan routes, transit, and hotel areas.
    """
    print("Logistics Agent: Searching live transit data...")
    cities = state.get("constraints", {}).get("cities", [])
    
    wiki_context = ""
    try:
        # pyrefly: ignore [missing-import]
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            # If there's more than one city, search for transit between them
            if len(cities) > 1:
                for i in range(len(cities) - 1):
                    query = f"how to travel from {cities[i]} to {cities[i+1]} Japan transit train shinkansen"
                    results = [r for r in ddgs.text(query, max_results=2)]
                    wiki_context += f"\n\nTransit {cities[i]} to {cities[i+1]}:\n"
                    for r in results:
                        wiki_context += f"- {r['title']}: {r['body']}\n"
            else:
                query = f"getting around in {cities[0]} Japan public transit"
                results = [r for r in ddgs.text(query, max_results=3)]
                wiki_context += f"\n\nTransit in {cities[0]}:\n"
                for r in results:
                    wiki_context += f"- {r['title']}: {r['body']}\n"
    except Exception as e:
        print(f"Logistics Agent: DuckDuckGo search failed ({e}). Falling back to WikiVoyage scraper...")
        scraped_data = scrape_japan_travel_data(cities)
        get_around = scraped_data.get("get_around", "")[:1500]
        wiki_context = get_around

    wiki_context = wiki_context[:3000]
    
    from src.llm import get_llm
    llm = get_llm(temperature=0.2)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Japan travel logistics planner. Based on the live search context below, formulate realistic transit plans between the user's cities, suggest the best transport methods (e.g. Shinkansen, planes), and recommend practical neighborhoods to stay in for easy transit access. Explicitly recommend whether the user should purchase a JR Pass (if doing expensive inter-city travel) or simply use a local IC Card like Suica/Pasmo (for local or single-city travel). Provide a concise JSON structure (e.g., {{'transit': [], 'hotels': [], 'pass_recommendation': ''}}).\n\nLive Search Context:\n{wiki_context}"),
        ("human", "My trip constraints: {constraints}")
    ])
    
    chain = prompt | llm
    
    print("Logistics Agent: Generating logistics plan...")
    response = chain.invoke({
        "wiki_context": wiki_context,
        "constraints": state.get("constraints", {})
    })
    
    return {"logistics_plan": {"raw_logistics": response.content}}

