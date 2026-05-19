# Kelvi Backend

The backend for Kelvi, a "smart" Tamil dictionary.


## Dictionaries used
- [mcalpin](https://github.com/indic-dict/stardict-tamil)
- [wiktionary](https://www.wiktionary.org/) data obtained via [kaikki.org](https://kaikki.org/index.html)

## Setup
Prerequisites: Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/)

1. Create and activate a new environment
    ```
    uv venv .venv
    source .venv/bin/activate
    ```
2. Sync uv 
    ```
    uv sync
    ```
3. Run pre-commit hooks
    ```
    pre-commit run --all
    ```
4. Update mappings for `g2p` (note: your Python version might differ)
    ```
    mkdir .venv/lib/python3.13/site-packages/g2p/mappings/langs/tam
    cp mappings/* .venv/lib/python3.13/site-packages/g2p/mappings/langs/tam/
    g2p update
    ```
5. Start the FastAPI server
    ```
    uv run uvicorn app.main:app
    ```

## Testing
If using apple, use gmake instead of make. 

1. Update docker images 
   ``` 
   make update-test-env
   ```
2. Run test command
   ```
   make test 
   ```
