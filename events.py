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
    Event(id=1, title="Bridal Shower", description="Obong's bridal shower", date="2025-05-01", location="Lagos"),
    Event(id=2, title="Birthday Party", description="A birthday party", date="2025-05-03", location="Abuja"),
    Event(id=3, title="Tech Party", description="All-night coding", date="2025-05-01", location="Port Harcourt"),
]