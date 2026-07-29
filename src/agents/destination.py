import os
# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq
# pyrefly: ignore [missing-import]
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any

from src.state import TripState
from src.scraper import scrape_japan_travel_data

def run_destination_agent(state: TripState) -> Dict[str, Any]:
    """
    Uses Groq and live DuckDuckGo Search data to recommend POIs and neighborhoods.
    """
    print("Destination Agent: Searching live travel data...")
    cities = state.get("constraints", {}).get("cities", [])
    
    wiki_context = ""
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            for city in cities:
                query = f"top attractions, temples, and neighborhoods in {city} Japan"
                results = [r for r in ddgs.text(query, max_results=3)]
                wiki_context += f"\n\nSearch results for {city}:\n"
                for r in results:
                    wiki_context += f"- {r['title']}: {r['body']}\n"
    except Exception as e:
        print(f"Destination Agent: DuckDuckGo search failed ({e}). Falling back to WikiVoyage scraper...")
        scraped_data = scrape_japan_travel_data(cities)
        see_content = scraped_data.get("see", "")[:1500] 
        do_content = scraped_data.get("do", "")[:1500]
        wiki_context = f"SEE:\n{see_content}\n\nDO:\n{do_content}"
    
    # Trim to fit strictly within TPM limits if needed
    wiki_context = wiki_context[:3000]
    
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert local Japan travel guide. Based on the live search context below, recommend top neighborhoods, temples, and experiences tailored to the user's constraints. Provide a strong distinction between different neighborhoods. Suggest authentic off-the-beaten-path local experiences alongside major spots to give a true local flavor. Focus strictly on the cities requested. Provide a concise JSON structure of recommendations (e.g., {{'cities': [{{'name': 'Tokyo', 'neighborhoods': [], 'pois': []}}] }}).\n\nLive Search Context:\n{wiki_context}"),
        ("human", "My trip constraints: {constraints}")
    ])
    
    chain = prompt | llm
    
    print("Destination Agent: Generating recommendations...")
    response = chain.invoke({
        "wiki_context": wiki_context,
        "constraints": state.get("constraints", {})
    })
    
    return {"destination_plan": {"raw_recommendations": response.content}}

