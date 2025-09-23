from fastapi import FastAPI
from contextlib import asynccontextmanager
import stanza

from app.routers import words
from app.data.dictionaries.WordDict import WordDict


tamil_dicts = {}
dict_names = ["mcalpin", "wiktionary"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load dictionary
    for name in dict_names:
        tamil_dicts[name] = WordDict(name)
    app.state.tamil_dicts = tamil_dicts
    # Initialize Stanza pipeline
    # can write a custom lemmatizer if we need it: https://stanfordnlp.github.io/stanza/pipeline.html
    stanza_pipeline = stanza.Pipeline(
        lang="ta",
        processors="tokenize,mwt,pos,lemma",
        download_method="reuse_resources",
    )
    app.state.stanza_pipeline = stanza_pipeline

    yield
    tamil_dicts.clear()


app = FastAPI(lifespan=lifespan)
app.include_router(words.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Kelvi"}
