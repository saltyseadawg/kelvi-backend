from fastapi import APIRouter, HTTPException, Request

router = APIRouter()


@router.get("/word/{query}")
async def read_word(query: str, request: Request):
    result = []
    tamil_dicts = request.app.state.tamil_dicts
    for d in tamil_dicts.values():
        result.append(d.search_word(query))

    if not any(result):
        raise HTTPException(status_code=404, detail="Word not found")
    return result
