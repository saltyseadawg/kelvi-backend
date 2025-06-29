from fastapi import Depends, FastAPI
from .routers import words

app = FastAPI()

app.include_router(words.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Kelvi"}