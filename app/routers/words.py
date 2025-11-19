from fastapi import APIRouter, HTTPException, Request
from app.morphology import analyzer

router = APIRouter()


@router.get("/word/{query}")
async def read_word(query: str, request: Request):
    result = analyzer.analyze_word_stanza(
        query, pipeline=request.app.state.stanza_pipeline
    )
    tamil_dicts = request.app.state.tamil_dicts
    isFound = any(d.search_word(result) for d in tamil_dicts.values())
    if not isFound:
        result = analyzer.analyze_word_gramble(query, request.app.state.glosser)
        isFound = any(d.search_word(result) for d in tamil_dicts.values())
    if not isFound:
        raise HTTPException(status_code=404, detail="Word not found")
    return None