import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# Ensure environment variables are loaded (GROQ_API_KEY, GOOGLE_API_KEY)
load_dotenv()

from src.graph import create_trip_graph

def main():
    print("Initializing Multi-Agent Trip Planner (Phase 3)...")
    app = create_trip_graph()
    
    # The initial request
    user_request = "I want to visit Tokyo and Kyoto for 7 days. My budget is $3000. I love traditional temples and eating sushi, but I want to avoid heavily crowded tourist traps where possible."
    
    # Initial state
    inputs = {"request": user_request}
    
    print(f"\nUser Request: {user_request}\n")
    print("-" * 50)
    
    # Execute graph
    # We use stream to see the outputs of each node as they run
    for output in app.stream(inputs):
        for key, value in output.items():
            print(f"Node '{key}' completed.")
            
    print("-" * 50)
    
    # After completion, we can extract the final state
    # Actually app.stream yields the state after each node, so we can just run invoke to get final state.
    # To get final output easily:
    final_state = app.invoke(inputs)
    
    print("\n" + "="*50)
    print("FINAL ITINERARY & FEEDBACK:")
    print("="*50)
    print(final_state.get("draft_itinerary", {}).get("raw_itinerary", "No itinerary found"))
    print("\nREVIEW STATUS:")
    print(final_state.get("review_feedback", []))
    
if __name__ == "__main__":
    main()
