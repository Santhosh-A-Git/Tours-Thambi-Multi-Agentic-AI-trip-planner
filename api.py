from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from src.graph import create_trip_graph

load_dotenv()

app = FastAPI(title="Agentic Trip Planner API")

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Keep graph in memory to avoid recompiling
graph = create_trip_graph()

class PlanRequest(BaseModel):
    request: str

@app.post("/plan")
async def generate_plan(payload: PlanRequest):
    try:
        inputs = {"request": payload.request}
        final_state = graph.invoke(inputs)
        
        # Determine success or failure
        review_status = final_state.get("review_status", "")
        if review_status == "terminal_failure":
            return {
                "success": False,
                "feedback": final_state.get("review_feedback", []),
                "itinerary": None
            }
        
        itinerary = final_state.get("draft_itinerary", {}).get("raw_itinerary", "No itinerary found.")
        feedback = final_state.get("review_feedback", [])
        
        return {
            "success": True,
            "itinerary": itinerary,
            "feedback": feedback
        }
        
    except Exception as e:
        return {
            "success": False,
            "feedback": [f"Internal Server Error: {str(e)}"],
            "itinerary": None
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
