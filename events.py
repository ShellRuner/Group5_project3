from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Optional

# Event model
class Event(BaseModel):
    id: int
    title: str
    description: str
    date: str
    location: str
    flyer_filename: Optional[str] = None
    rsvps: List[str] = []

# Event Database
events_db = [
    Event(id=1, title="Open day", description="School", date="2025-05-01", location="Lagos"),
    Event(id=2, title="Birthday Party", description="A birthday party", date="2025-05-03", location="Abuja"),
    Event(id=3, title="Tech Party", description="All-night coding", date="2025-05-01", location="Port Harcourt"),
]

# FastAPI router
router = APIRouter()

# Event listing + filtering endpoint
@router.get("/events/", response_model=List[Event])
def list_events(
    date: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: Optional[str] = Query("date"),
    order: Optional[str] = Query("asc")
):
    # Start with all events
    filtered_events = events_db

    # Filter by date
    if date:
        filtered_events = [e for e in filtered_events if e.date == date]

    # Filter by location
    if location:
        filtered_events = [e for e in filtered_events if location.lower() in e.location.lower()]

    # Search title or description
    if search:
        filtered_events = [e for e in filtered_events if search.lower() in e.title.lower() or search.lower() in e.description.lower()]

    # Sort results
    if sort_by in ["title", "date", "location"]:
        reverse = (order == "desc")
        filtered_events = sorted(filtered_events, key=lambda e: getattr(e, sort_by), reverse=reverse)

    return filtered_events