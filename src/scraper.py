import requests
# pyrefly: ignore [missing-import]
from bs4 import BeautifulSoup
# pyrefly: ignore [missing-import]
from typing import Optional

def get_wikivoyage_section(soup: BeautifulSoup, section_id: str) -> Optional[str]:
    """
    Extracts the text from a heading down to the next heading of the same or higher level,
    given a BeautifulSoup object and the HTML id.
    """
    
    # Find the heading with the specific id
    heading = soup.find(id=section_id)
    if not heading:
        print(f"Could not find section with id: {section_id}")
        return None
        
    # If the heading is wrapped in a mw-heading div, we need to traverse the div's siblings
    wrapper = heading.parent if heading.parent and 'mw-heading' in heading.parent.get('class', []) else heading
    
    heading_level = int(heading.name[1]) if heading.name and heading.name.startswith('h') else 0
    
    content_parts = []
    
    # Iterate through siblings
    current_node = wrapper.find_next_sibling()
    while current_node:
        # Check if we hit another heading (either directly or wrapped in mw-heading)
        node_heading = current_node if current_node.name and current_node.name.startswith('h') else current_node.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if node_heading and node_heading.name and node_heading.name.startswith('h'):
            level = int(node_heading.name[1])
            if level <= heading_level:
                break
        
        if current_node.name not in ['script', 'style']: # Ignore scripts/styles
            text = current_node.get_text(separator=' ', strip=True)
            if text:
                content_parts.append(text)
                
        current_node = current_node.find_next_sibling()
        
    return "\n\n".join(content_parts)

def scrape_japan_travel_data(cities: list[str] = None):
    """
    Convenience function to grab necessary contexts for the agents.
    If cities are provided, it scrapes those specific WikiVoyage pages.
    Otherwise, it defaults to the macro 'Japan' page.
    Returns a dictionary of texts.
    """
    data = {
        "budget": "",
        "get_around": "",
        "see": "",
        "do": "",
        "eat": ""
    }
    
    locations_to_scrape = cities if cities else ["Japan"]
    
    for loc in locations_to_scrape:
        url = f"https://en.wikivoyage.org/wiki/{loc}"
        print(f"Scraping WikiVoyage for: {loc}")
        
        try:
            headers = {'User-Agent': 'TravelPlannerAgent/1.0 (contact@example.com)'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            continue
        
        # Budget section might be called 'Buy' on some pages and 'Budget' on others
        # We will try both, starting with 'Buy'
        budget_content = get_wikivoyage_section(soup, "Buy")
        if not budget_content:
            budget_content = get_wikivoyage_section(soup, "Budget")
            
        loc_data = {
            "budget": budget_content,
            "get_around": get_wikivoyage_section(soup, "Get_around"),
            "see": get_wikivoyage_section(soup, "See"),
            "do": get_wikivoyage_section(soup, "Do"),
            "eat": get_wikivoyage_section(soup, "Eat")
        }
        
        for key in data:
            if loc_data[key]:
                data[key] += f"\n\n--- {loc.upper()} ---\n{loc_data[key]}"
                
    return data

if __name__ == "__main__":
    # Test the scraper
    print("Scraping Tokyo and Kyoto WikiVoyage data...")
    test_data = scrape_japan_travel_data(["Tokyo", "Kyoto"])
    for section, content in test_data.items():
        if content:
            print(f"--- {section.upper()} ---")
            safe_content = content[:200].encode('ascii', 'ignore').decode()
            print(safe_content + "...\n")
        else:
            print(f"--- {section.upper()} --- NOT FOUND")
