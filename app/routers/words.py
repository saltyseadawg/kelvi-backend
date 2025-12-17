import logging

from fastapi import APIRouter, HTTPException, Request
from app.morphology import analyzer

router = APIRouter()


@router.get("/word/{query}")
async def read_word(query: str, request: Request):
    # try lemmatizer
    result = analyzer.analyze_word_stanza(
        query, pipeline=request.app.state.stanza_pipeline
    )
    tamil_dicts = request.app.state.tamil_dicts
    isFound = any([d.search_word(result) for d in tamil_dicts.values()])
    if not isFound:
        # try using gramble to find suffix
        result = analyzer.analyze_word_gramble(query, request.app.state.glosser)
        isFound = any([d.search_word(result) for d in tamil_dicts.values()])
    if not isFound:
        # try add back to find lemma
        analyzer.analyze_word_add_back(result, request.app.state.glosser)
        isFound = any([d.search_word(result) for d in tamil_dicts.values()])
    if not isFound:
        raise HTTPException(status_code=404, detail="Word not found")
    if isFound:        
        try:
            request.app.state.romanizer.romanize_query(result)
        except Exception:
            logging.error(f"Word: {query}")
    return result
