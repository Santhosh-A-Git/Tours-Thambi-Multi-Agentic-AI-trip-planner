# Phase-Wise Implementation Plan

This document outlines the step-by-step approach to building the Multi-Agent Trip Planning System for Japan, based on the `Context.md` and `architecture.md`.

## Phase 1: Foundation and State Design
**Goal:** Set up the project structure, dependencies, and the core data structures that will flow through the system.
- **1.1 Environment Setup:** Initialize the repository (e.g., Python virtual environment), install core frameworks (e.g., `langgraph`, `langchain`), and install SDKs for `groq` and `google-generativeai` (Gemini).
- **1.2 State Definition:** Define the typed `State` object (as outlined in `architecture.md`) using `TypedDict` or Pydantic models.
- **1.3 Orchestrator Skeleton:** Build the initial Orchestrator agent that can take a natural language prompt, use **Groq** to parse it into the `constraints` dictionary, and initialize the state.

## Phase 2: Agent Development with Scraped Data
**Goal:** Build the individual worker agents to use real scraped data from reliable sources like WikiVoyage instead of relying on mock data.
- **2.1 Destination Agent (Data-Driven):** Create an agent using **Groq** that scrapes data from [WikiVoyage Japan](https://en.wikivoyage.org/wiki/Japan) to recommend real POIs, neighborhoods, and experiences based on user preferences.
- **2.2 Logistics Agent (Data-Driven):** Create an agent using **Groq** that scrapes travel guides (e.g., from WikiVoyage 'Get around' sections) to estimate realistic travel times (e.g., Shinkansen routes) and recommend practical hotel locations.
- **2.3 Budget Agent (Data-Driven):** Create an agent that uses **Groq** to process scraped data from the [WikiVoyage Japan Budget Section](https://en.wikivoyage.org/wiki/Japan#Budget) to accurately estimate costs.
- **2.4 Review Agent (Gemini 1.5 Pro):** Build the Review agent using **Gemini 1.5 Pro** (or the most advanced Gemini reasoning model available) to evaluate the drafted itinerary and intelligently check if it meets all constraints and preferences.

## Phase 3: Graph Integration and Workflow (The Orchestration)
**Goal:** Connect the agents using the LangGraph framework to enable parallel execution and cyclical feedback loops.
- **3.1 Parallel Execution Node:** Configure the graph so that the Orchestrator passes the state to Destination, Logistics, and Budget agents simultaneously.
- **3.2 State Synthesis:** Create a node/function for the Orchestrator to combine the parallel outputs into a single `draft_itinerary`.
- **3.3 The Review Loop:** Connect the `draft_itinerary` to the Review Agent. Implement the conditional edge:
  - If Approved -> End State (Final Itinerary).
  - If Rejected -> Route back to the Orchestrator/Worker agents with `review_feedback`.

## Phase 4: Live API Integrations
**Goal:** Replace mock data with live API calls to make the system dynamic and real-world ready.
- **4.1 Destination API:** Integrate Tavily Search API or Google Places API for real-time Japanese attraction and restaurant data.
- **4.2 Logistics API:** Integrate Google Maps Distance Matrix or a transit API for accurate Shinkansen/local train schedules.
- **4.3 Financial API:** Integrate a currency conversion API (ExchangeRate-API) to dynamically convert USD to JPY.
- **4.4 Error Handling:** Add `try/except` blocks and fallback mechanisms (returning to mock data if an API rate limits or fails).

## Phase 5: Refinement, Testing, and UI
**Goal:** Polish the output, handle edge cases, and make it usable.
- **5.1 Prompt Tuning:** Refine the LLM prompts for the Destination and Logistics agents to ensure they behave like local Japan experts (e.g., knowing the difference between JR Pass and regular tickets).
- **5.2 Edge Case Testing:** Test the system with impossible constraints (e.g., "$100 budget for 5 days in Tokyo") to ensure the Review loop handles it gracefully (e.g., maxing out at 3 retries and returning a failure explanation).
- **5.3 User Interface (Optional):** Wrap the multi-agent backend in a simple Streamlit or Gradio UI so users can easily input requests and read the final itinerary.

## Phase 6: Frontend Web Application
**Goal:** Build a visually stunning, dynamic, and responsive web frontend for the Trip Planner.
- **6.1 Stack Selection:** Choose a frontend architecture. Options include a polished Python-native UI (Streamlit) or a decoupled modern stack (FastAPI backend + Vite/React frontend).
- **6.2 Design Aesthetics:** Implement a premium design system (vibrant colors, glassmorphism, modern typography like 'Inter') to WOW the user.
- **6.3 Backend Integration:** Connect the frontend to the `main.py` LangGraph workflow. Provide streaming updates or a loading state while the multi-agent pipeline processes the request.
- **6.4 Itinerary Presentation:** Render the generated Markdown itinerary in a beautiful, highly scannable UI, potentially with interactive maps or image placeholders for the generated cities.
