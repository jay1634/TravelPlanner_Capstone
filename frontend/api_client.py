import requests
from typing import Any, Dict, List

BACKEND_URL = "http://127.0.0.1:8000"


def api_chat(session_id: str, message: str, name: str | None = None) -> Dict[str, Any]:
    payload = {"session_id": session_id, "message": message, "name": name}
    r = requests.post(f"{BACKEND_URL}/chat", json=payload, timeout=300)
    r.raise_for_status()
    return r.json()


def api_generate_itinerary(
    session_id: str,
    destination: str,
    days: int,
    budget: float,
    interests: List[str],
    food_preferences: str | None,
) -> Dict[str, Any]:
    payload = {
        "session_id": session_id,
        "destination": destination,
        "days": days,
        "budget": budget,
        "interests": interests,
        "food_preferences": food_preferences,
    }
    r = requests.post(f"{BACKEND_URL}/generate_itinerary", json=payload, timeout=120)
    r.raise_for_status()
    return r.json()
