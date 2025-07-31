from fastapi import FastAPI
from app.routers import words

app = FastAPI()

app.include_router(words.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Kelvi"}
