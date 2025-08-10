from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers import words
from app.data.dictionaries.WordDict import WordDict


tamil_dicts = {}
dict_names = ["mcalpin"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load dictionary
    for name in dict_names:
        tamil_dicts[name] = WordDict(name)
    app.state.tamil_dicts = tamil_dicts
    yield
    tamil_dicts.clear()


app = FastAPI(lifespan=lifespan)
app.include_router(words.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Kelvi"}
