from app.models import InputWord

from fastapi import APIRouter, Request
from app.routers import e2e_testing

router = APIRouter()


@router.get("/word/{query}")
async def read_word(query: str, request: Request):
    raw_word_data = InputWord(user_input=query.strip())
    word_data = e2e_testing.process_input_word(
        raw_word_data,
        request.app.state.tamilizer,
        request.app.state.romanizer,
        request.app.state.stanza_pipeline,
        request.app.state.tamil_dicts,
        request.app.state.glosser,
    )
    return word_data
