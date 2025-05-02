from typing import List, Optional, Annotated
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Query, status
from fastapi.responses import JSONResponse

app = FastAPI()

# Data Models


class Event(BaseModel):
    id: int
    title: str
    description: str
    date: str
    location: str
    flyer_filename: Optional[str] = None
    rsvps: List[str] = []


# Response data Model
class Response(BaseModel):
    message: Optional[str] = None
    has_error: bool = False
    error_message: Optional[str] = None
    data: Optional[Event] = None


class GuestBase(BaseModel):
    name: str
    email: EmailStr


class GuestCreate(GuestBase):
    event_id: int
    user_id: Optional[int] = None


class GuestRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    rsvp_status: str
    event_id: int
    user_id: Optional[int] = None
    created_at: datetime


class RSVPResponse(BaseModel):
    guest_id: int
    rsvp_status: str
    message: str


# In-memory Data Storage
events: dict[str, Event] = {}
guests: List[GuestRead] = []


# Helper functions
def get_guest(guest_id: int):
    for guest in guests:
        if guest.id == guest_id:
            return guest
    return None


def create_guest(guest: GuestCreate):
    new_guest = GuestRead(
        id=len(guests) + 1,
        name=guest.name,
        email=guest.email,
        rsvp_status="pending",
        event_id=guest.event_id,
        user_id=guest.user_id,
        created_at=datetime.now()
    )
    guests.append(new_guest)
    return new_guest


def update_guest_rsvp_status(guest_id: int, rsvp_status: str):
    existing_guest = get_guest(guest_id=guest_id)
    if not existing_guest:
        return None

    index = -1
    for i, g in enumerate(guests):
        if g.id == guest_id:
            index = i
            break

    if index == -1:
        return None

    updated_guest = GuestRead(
        id=existing_guest.id,
        name=existing_guest.name,
        email=existing_guest.email,
        rsvp_status=rsvp_status,
        event_id=existing_guest.event_id,
        user_id=existing_guest.user_id,
        created_at=existing_guest.created_at,
    )
    guests[index] = updated_guest
    return updated_guest


def get_guests_by_event(event_id: int):
    return [guest for guest in guests if guest.event_id == event_id]


# Endpont to create events
@app.get("/")
def home():
    return "WELCOME TO RSVP SYSTEM ASSIGNMENT"


@app.post("/events")
async def create_event(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    date: Annotated[str, Form()],
    location: Annotated[str, Form()],
    flyer: Optional[UploadFile] = None,
) -> Response:
    if title in events:
        return Response(
            has_error=True,
            error_message="Event with this title already exists.",
        )
    flyer_filename = None
    if flyer:
        flyer_filename = flyer.filename
        await save_file_to_disk(flyer)

    event = Event(
        id=len(events) + 1,
        title=title,
        description=description,
        date=date,
        location=location,
        flyer_filename=flyer_filename,
        rsvps=[],
    )
    events[title] = event
    return Response(message="Event created successfully", data=event)


async def save_file_to_disk(uploaded_file: UploadFile):
    with open(uploaded_file.filename, "wb+") as file_object:
        file_content = await uploaded_file.read()
        file_object.write(file_content)


@app.post("/guests/", response_model=GuestRead, status_code=status.HTTP_201_CREATED)
async def create_guest_endpoint(guest: GuestCreate) -> GuestRead:
    db_guest = create_guest(guest=guest)
    return db_guest


@app.post("/guests/{guest_id}/rsvp", response_model=RSVPResponse)
async def rsvp_status_endpoint(
    guest_id: int,
    rsvp_status: Annotated[str,
                           Query(..., enum=["attending", "not_attending"])]
) -> RSVPResponse:
    db_guest = get_guest(guest_id=guest_id)
    if db_guest is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Guest not found"
        )

    updated_guest = update_guest_rsvp_status(guest_id, rsvp_status)
    if updated_guest is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Guest not found"
        )
    return RSVPResponse(
        guest_id=guest_id,
        rsvp_status=rsvp_status,
        message=f"Guest {updated_guest.name} is {rsvp_status} to the event.",
    )


@app.get("/events/{event_id}/guests", response_model=List[GuestRead])
async def read_guests_by_event_endpoint(event_id: int) -> List[GuestRead]:
    event_guests = get_guests_by_event(event_id=event_id)
    return event_guests
