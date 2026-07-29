# Multi-Agent Trip Planner: Edge Cases and Error Handling

This document outlines the known edge cases and potential failure states for the Japan Trip Planner, as well as the architectural mechanisms designed to handle them.

## 1. User Constraint Edge Cases

### 1.1 Unrealistic Budget or Duration
**Scenario:** The user requests a "$100 budget for 7 days in Tokyo" or "Visit Tokyo, Kyoto, Osaka, and Sapporo in 3 days."
**Handling Mechanism:**
- The **Budget Agent** and **Logistics Agent** will generate their respective plans based on reality (e.g. noting that trains cost $130 alone).
- The **Review Agent** will detect that the realistic plan breaches the user's constraints.
- **Resolution:** The LangGraph cyclical loop triggers. To prevent an infinite loop of impossible requests, the Orchestrator will maintain a `retry_count`. If `retry_count > 3`, the system will exit the loop and present the user with a partial itinerary, alongside an explicit explanation that their constraints were impossible.

### 1.2 Underspecified Requests
**Scenario:** The user simply says "I want to go to Japan" without providing a budget, cities, or duration.
**Handling Mechanism:** 
- The **Orchestrator** utilizes a strict prompt with defaults (as defined in Phase 1). It will extract "Japan", default the budget to $3000, and assume a standard 7-day duration if none is provided.

### 1.3 Over-Constrained Preferences
**Scenario:** "I only want to eat vegan ramen for under $3 in Shibuya while avoiding all tourists."
**Handling Mechanism:** 
- The **Destination Agent** relies on scraped WikiVoyage data. If it cannot find exact matches in the context window, it is prompted to provide the "next best alternative" rather than hallucinating fake restaurants. 

## 2. Technical & API Edge Cases

### 2.1 API Rate Limits (TPM/RPM)
**Scenario:** The system utilizes Groq's `llama-3.3-70b-versatile` which has a strict 12,000 Tokens Per Minute limit on the free tier. When the Orchestrator delegates to Destination, Logistics, and Budget agents simultaneously, the parallel API calls exceed the limit, causing a `429 RESOURCE_EXHAUSTED` error.
**Handling Mechanism:** 
- **Context Trimming:** The Scraper aggressively slices the HTML/Markdown context (e.g., `[:1500]` characters per section) before passing it to the worker agents.
- **Model Fallbacks:** Future updates (Phase 4) will implement `try/except` blocks in LangGraph nodes to automatically failover to smaller models (e.g. `llama-3.1-8b`) if the 70B model rate-limits.

### 2.2 Live Scraping Failures
**Scenario:** WikiVoyage structure changes, or the scraper gets temporarily IP-blocked (403 Forbidden).
**Handling Mechanism:**
- The `scraper.py` script wraps the HTTP requests in a `try/except` block with a timeout. If the scrape fails, it returns empty strings for the context. 
- The worker agents are prompted to fall back on their own internal parametric knowledge (LLM pre-training) if the `{wiki_context}` is completely empty, ensuring the pipeline doesn't completely crash.

### 2.3 Invalid JSON Output
**Scenario:** An agent (like the Review Agent) is prompted to return strict JSON, but wraps it in Markdown ```json blocks or includes conversational filler.
**Handling Mechanism:**
- The Orchestrator utilizes `.with_structured_output()` via LangChain to enforce schema on the constraints. 
- Custom agents use string parsing heuristics (e.g. `output.strip("```json")`) to sanitize outputs before feeding them to the next node.
