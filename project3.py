from fastapi import FastAPI, File, UploadFile, Form
from typing import Annotated
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

#pydantic schema
# class Event(BaseModel):
#     id: int
#     title: str
#     description: str
#     date: str
#     location: str
#     flyer_filename: Optional[str] = None
#     rsvps: list[str] = []
    
# class RSVP(BaseModel):
#     name: str
#     email: str

#In-memeory events database
events = {}
#Event creation and file handling
#Endpoint to the event creation form
@app.post("/events/")
async def events(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    date: Annotated[str, Form()],
    location: Annotated[str, Form()],
    flyer: Optional[UploadFile] = None
):
    
    async def creat_flyer(file: UploadFile):
        save_file_to_disk(file)
    def save_file_to_disk(uploaded_file: UploadFile):
        with open(uploaded_file.filename, "wb+") as file_object:
            file_object.write(uploaded_file.file.read())
            
            
    return {"message" : "Event successfully created"}


