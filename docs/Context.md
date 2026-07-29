# Context

This document provides the complete context and problem statement for the Multi-Agentic Trip Planning project, specifically focusing on building the system for the **Japan location only**.

## Problem Statement
Planning a trip can quickly become overwhelming due to the need to combine different kinds of work, such as understanding traveler goals, researching destinations, comparing logistics, and staying within budget.

The goal is to design a **Travel Planning Multi-Agent System** that can automatically turn a short, natural-language travel request into a useful, day-by-day trip plan.

### Objective
Design a simple multi-agent system to showcase how specialized AI agents can work together on a real-world problem. The system will process user requests and produce:
- A day-by-day trip outline
- Suggested neighborhoods / areas to stay
- Travel logistics between cities (e.g., using the Shinkansen)
- Budget-friendly recommendations
- A final itinerary that respects the user's preferences and constraints

## Current Focus: Japan Location
Currently, the system is being built and optimized specifically for planning trips to **Japan**. All agent knowledge bases, API integrations (if any), and logic will prioritize Japanese geography, transit systems, culture, and pricing.

### Example Real-World Request (Japan)
*“Plan a 5-day trip to Japan. Tokyo + Kyoto. $3,000 budget. Love food and temples, hate crowds.”*

## Multi-Agent System Design (Japan Focus)

### 1. Orchestrator Agent
**Role**: Creates the master plan, assigns work, and combines outputs into the final itinerary.
- Reads the user request.
- Extracts key constraints (e.g., Destination: Japan, Duration: 5 days, Cities: Tokyo + Kyoto, Budget: $3,000).
- Delegates tasks to specialized agents.
- Synthesizes the final travel plan.

### 2. Destination Research Agent
**Role**: Finds the best places, experiences, and food ideas based on preferences, focusing on Japanese locales.
- Recommends specific neighborhoods, temples, food streets, and local experiences (e.g., quiet temple areas in Kyoto, food neighborhoods in Tokyo).
- Suggests less-crowded options and identifies “must-do” vs “nice-to-have” items in Japan.

### 3. Logistics Agent
**Role**: Handles the practical side of moving and staying within Japan.
- Suggests where to stay in each city.
- Estimates travel time between locations and recommends transit (e.g., Shinkansen between Tokyo and Kyoto).
- Builds a realistic sequence for each day to reduce backtracking.

### 4. Budget Agent
**Role**: Ensures the plan stays within budget (e.g., converting to/from JPY).
- Breaks the budget into categories (Stay, Transport, Food, Activities).
- Flags when the plan becomes too expensive (e.g., if central Tokyo hotels exceed budget) and suggests cheaper alternatives.

### 5. Review Agent
**Role**: Validates the final itinerary before it is shown to the user.
- Checks constraints: Fits into the requested days? Includes requested cities (Tokyo/Kyoto)? Within budget? Aligns with preferences (food/temples)? Avoids crowds? Realistic travel time?
- Acts as a quality checker before finalizing the output.

### Workflow
Orchestrator -> [Destination, Logistics, Budget in parallel] -> Review
