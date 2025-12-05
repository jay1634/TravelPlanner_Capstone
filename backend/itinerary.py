from .llm_client import chat_with_llm


def build_itinerary(
    destination: str,
    days: int,
    budget: float,
    interests: list,
    food_pref: str | None,
    rag_context: str,
) -> str:
    interests_text = ", ".join(interests) if interests else "general sightseeing"
    food_text = food_pref if food_pref else "no specific preference"

    system_prompt = (
        "You are a professional travel planner AI. "
        "You MUST generate a clean, well-structured, day-wise travel itinerary. "
        "Use bullet points, headings, budget breakdowns and timing blocks. "
        "Do NOT write long paragraphs. Keep it very easy to read."
    )

    user_prompt = f"""
Generate a {days}-day structured travel itinerary for:

Destination: {destination}
Total Budget: {budget}
Interests: {interests_text}
Food preference: {food_text}

You MUST follow this exact format:

==============================
DESTINATION OVERVIEW
==============================
• Best time to visit:
• Weather:
• Travel tips:

==============================
DAILY ITINERARY
==============================

DAY 1:
Morning:
• Activity 1
• Activity 2

Afternoon:
• Activity 1
• Activity 2

Evening:
• Activity 1
• Activity 2

Estimated Day 1 Cost: ₹XXX

DAY 2:
Morning:
• ...
Afternoon:
• ...
Evening:
• ...

Estimated Day 2 Cost: ₹XXX

(Repeat till Day {days})

==============================
FOOD & RESTAURANTS
==============================
• Breakfast:
• Lunch:
• Dinner:

==============================
LOCAL TRANSPORT
==============================
• Mode:
• Approx cost per day:

==============================
SAFETY & RULES
==============================
• Safety tips:
• Local rules:

==============================
FINAL BUDGET SUMMARY
==============================
• Stay:
• Food:
• Transport:
• Activities:
• Misc:
• TOTAL:

Now generate the itinerary using this document context:
{rag_context}
"""

    return chat_with_llm(
        prompt=user_prompt,
        system_message=system_prompt,
        history=None,
    )
