from fastapi import FastAPI
from contextlib import asynccontextmanager
import stanza

from app.routers import words
from app.data.dictionaries.WordDict import WordDict
from app.morphology.glosser.Glosser import Glosser
from app.lang_mappings.converter import Converter, Romanizer


tamil_dicts = {}
dict_names = ["mcalpin", "wiktionary"]
ROMANIZATION_MAPPING = "tamil-roman-mapping.csv"


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
        # uncomment for local development
        # download_method="reuse_resources"
        download_method=None,
    )
    app.state.stanza_pipeline = stanza_pipeline
    app.state.glosser = Glosser()
    app.state.romanizer = Romanizer("tamil", "romanization")
    app.state.tamilizer = Converter("romanization", "tamil")

    yield
    tamil_dicts.clear()


app = FastAPI(lifespan=lifespan)
app.include_router(words.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Kelvi"}
