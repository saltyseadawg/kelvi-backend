from fastapi import APIRouter, HTTPException

from app.parsers.dict_parser import search_word

router = APIRouter()


@router.get("/word/{query}")
async def read_word(query):
    result = search_word(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Word not found")
    return result
