from fastapi import APIRouter, HTTPException, Request
from app.models import InputWord, TamilForm
from app.utils.pipeline import get_first_word_from_pipeline

router = APIRouter()


@router.get("/word/{query}")
async def read_word(query: str, request: Request):
    doc = request.app.state.nlp(query)
    word = get_first_word_from_pipeline(doc)
    result = InputWord(user_input=query, root=TamilForm(tamil=word.lemma))
    tamil_dicts = request.app.state.tamil_dicts
    for d in tamil_dicts.values():
        d.search_word(result)
    if not result.root_definition:
        raise HTTPException(status_code=404, detail="Word not found")
    return result


@router.get("/lemmatize/{query}")
async def lemmatize_word(query: str, request: Request):
    pass
