# Multi-Agent Trip Planner: Evaluation Criteria

This document defines the metrics and evaluation framework used to assess the performance of the LangGraph Multi-Agent Trip Planner (Phase 5).

## 1. Core Output Metrics

### 1.1 Constraint Adherence Rate (Strict Pass/Fail)
The most critical metric is whether the final itinerary strictly obeys the Orchestrator's parsed constraints.
- **Budget Variance:** The total calculated cost by the Budget Agent must be $\le$ the user's `budget_usd`.
- **Duration Match:** The number of planned days must exactly match `duration_days`.
- **City Fulfillment:** Every city listed in the user's prompt MUST have at least one scheduled activity.

### 1.2 Hallucination Rate
Because the system heavily relies on RAG (Retrieval-Augmented Generation) via WikiVoyage scraping, we must evaluate if the agents are inventing places.
- **Metric:** % of recommended POIs (Points of Interest), transit routes, and hotels that actually exist in the scraped context or real world.
- **Testing Method:** Manual sampling of the generated itineraries cross-referenced with Google Maps.

## 2. Architectural & Graph Metrics

### 2.1 Review Loop Efficiency
The LangGraph uses a cyclical Review loop where the Review Agent can reject the draft and send it back to the Synthesizer/Workers.
- **Metric:** Average number of graph cycles per user request.
- **Target:** $\le 1.5$ cycles average. If the system is constantly looping 3+ times, the worker agent prompts (Destination/Logistics) are not strict enough.

### 2.2 Parallel Execution Speed
- **Metric:** Total End-to-End Latency.
- **Target:** Since the Destination, Logistics, and Budget agents run in parallel via LangGraph on Groq's high-speed inference engine, the system should generate a full itinerary in $< 15$ seconds (excluding the initial WikiVoyage scraping latency).

## 3. Future Evaluation Tools (Phase 5)

To automate these evaluations, we will implement an overarching "Eval Agent" (or use LangSmith) that runs headless tests overnight against a golden dataset of 50 varied travel prompts.

**Example Eval Dataset:**
1. *Standard:* "7 days in Tokyo and Osaka, $3000 budget."
2. *Budget-Restricted:* "14 days in Tokyo, $500 budget." (Expectation: System flags as impossible or heavily relies on free parks/walking).
3. *Preference-Heavy:* "3 days in Kyoto, avoid shrines, focus only on modern architecture." (Expectation: Destination agent successfully filters out traditional POIs).
