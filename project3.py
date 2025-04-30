from fastapi import FastAPI, File, UploadFile, Form

from pydantic import BaseModel

from typing import Annotated, Optional



app = FastAPI()

class Event(BaseModel):
    title: str
    description: str
    date: Optional[str] = None
    location: str
    flyer: Optional[str] = None

    

class Response(BaseModel):
    message: Optional[str] = None
    has_error: bool = False
    error_message: Optional[str] = None
    data: Optional[Event] = None

events: dict[str, Event] = {}


@app.post("/create_event")
async def create_event(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    date: Annotated[str, Form()],
    location: Annotated[str, Form()],
    flyer: Annotated[Optional[UploadFile], File()] = None
):
    if title in events:
        return Response(
            has_error=True,
            error_message="Event with this title already exists."
        )
    
    flyer_filename = flyer.filename if flyer else None
    
    event = Event(
        title=title,
        description=description,
        date=date,
        location=location,
        flyer=flyer_filename
    )
    events[title] = event
    return Response(message="Event created successfully", data=event)
