# pyrefly: ignore [missing-import]
from langgraph.graph import StateGraph, END
from typing import TypedDict

from src.state import TripState
from src.orchestrator import parse_request
from src.agents.destination import run_destination_agent
from src.agents.logistics import run_logistics_agent
from src.agents.budget import run_budget_agent
from src.synthesizer import run_synthesizer
from src.agents.review import run_review_agent

def create_trip_graph():
    """
    Constructs the LangGraph for the Multi-Agent Trip Planner.
    """
    # Initialize the graph with our state schema
    workflow = StateGraph(TripState)

    # 1. Add nodes
    workflow.add_node("orchestrator", parse_request)
    workflow.add_node("destination", run_destination_agent)
    workflow.add_node("logistics", run_logistics_agent)
    workflow.add_node("budget", run_budget_agent)
    workflow.add_node("synthesizer", run_synthesizer)
    workflow.add_node("review", run_review_agent)

    # 2. Define edges (The Execution Flow)
    
    # Entry point
    workflow.set_entry_point("orchestrator")
    
    # Orchestrator branches out to the 3 parallel worker agents
    workflow.add_edge("orchestrator", "destination")
    workflow.add_edge("orchestrator", "logistics")
    workflow.add_edge("orchestrator", "budget")
    
    # All 3 workers converge on the synthesizer
    # In LangGraph, when multiple edges point to the same node, it waits for all to complete.
    workflow.add_edge("destination", "synthesizer")
    workflow.add_edge("logistics", "synthesizer")
    workflow.add_edge("budget", "synthesizer")
    
    # Synthesizer moves to Review
    workflow.add_edge("synthesizer", "review")
    
    # 3. Define Conditional Edges for the Review Loop
    def review_decision(state: TripState) -> str:
        if state.get("review_status") == "terminal_failure":
            print("Graph: Terminal failure reached. Ending workflow.")
            return "approved" # Routes to END

        # Check the status from the review agent
        feedback_str = "".join(state.get("review_feedback", [])).lower()
        if "failed" in feedback_str or "fix" in feedback_str:
            print("Graph: Itinerary REJECTED by Review Agent. Looping back...")
            return "rejected"
        else:
            print("Graph: Itinerary APPROVED by Review Agent.")
            return "approved"
            
    workflow.add_conditional_edges(
        "review",
        review_decision,
        {
            "approved": END,
            "rejected": "synthesizer" # Alternatively, route back to 'orchestrator' or 'destination'
        }
    )

    # Compile the graph
    app = workflow.compile()
    
    return app
