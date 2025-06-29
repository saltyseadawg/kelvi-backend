from fastapi import APIRouter, HTTPException
from app.models import TamilHeadword, DictEntry

router = APIRouter()

#mock data
entry_data = {
    "id": 1,
    "lang": "eng",
    "pos": "verb",
    "definition": "graze"
}

mock_dict = DictEntry(**entry_data)

mock_headword = TamilHeadword(
    headword="மேய்ந்துவிடும்",
    definitions=[mock_dict]
)


@router.get("/word/{headword}")
async def read_word(headword):
    if headword != "மேய்ந்துவிடும்":
        raise HTTPException(status_code=404, detail="Word not found")
    return mock_headword
    