from fastapi import FastAPI, File, UploadFile, Form

from pydantic import BaseModel

from typing import Annotated, Optional



app = FastAPI()

#Data Models
#Event schema
class Event(BaseModel):
    # id : int
    title: str
    description: str
    date: str
    location: str
    flyer_filename: Optional[str] = None
    # rsvps: list[str]= []

    
#Response data Model
class Response(BaseModel):
    message: Optional[str] = None
    has_error: bool = False
    error_message: Optional[str] = None
    data: Optional[Event] = None

#Inmemory database for events
events: dict[str, Event] = {}

#Endpont to create new events
@app.post("/events")
async def create_event(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    date: Annotated[str, Form()],
    location: Annotated[str, Form()],
    flyer: Optional[UploadFile] = None
):
    #Handle if the title of the event is already in the events database 
    if title in events:
        return Response(
            has_error=True,
            error_message="Event with this title already exists."
        )
    
    #Condition to check if the flyer  file was uploaded
    if flyer:
        flyer_filename = flyer.filename
        save_file_to_disk(flyer)
    else :
        flyer_filename = "No file"
    
    #creation of an object event and add it to the database (events)
    event = Event(
        title=title,
        description=description,
        date=date,
        location=location,
        flyer_filename=flyer_filename
    )
    events[title] = event
    return Response(message="Event created successfully", data=event)

#Function that save file to disk
def save_file_to_disk(uploaded_file: UploadFile):
    with open(uploaded_file.filename, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
