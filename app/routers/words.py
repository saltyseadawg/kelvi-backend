from fastapi import APIRouter, HTTPException, Request
from app.morphology import analyzer

router = APIRouter()


@router.get("/word/{query}")
async def read_word(query: str, request: Request):
    result = analyzer.analyze_word(query, pipeline=request.app.state.stanza_pipeline)
    tamil_dicts = request.app.state.tamil_dicts
    for d in tamil_dicts.values():
        d.search_word(result)
    if not result.root_definition:
        raise HTTPException(status_code=404, detail="Word not found")
    return result


@router.get("/lemmatize/{query}")
async def lemmatize_word(query: str, request: Request):
    pass
