from typing import TypedDict, List, Dict, Any, Optional

class Constraints(TypedDict, total=False):
    destination: str
    cities: List[str]
    duration_days: int
    budget_usd: int
    preferences: List[str]
    avoid: List[str]

class TripState(TypedDict, total=False):
    request: str
    constraints: Constraints
    destination_plan: Dict[str, Any]
    logistics_plan: Dict[str, Any]
    budget_plan: Dict[str, Any]
    draft_itinerary: Dict[str, Any]
    final_itinerary: Dict[str, Any]
    review_status: str
    review_feedback: List[str]
    retry_count: int
