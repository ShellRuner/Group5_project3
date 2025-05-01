from fastapi import FastAPI
from events import router as events_router

app = FastAPI()

app.include_router(events_router)
