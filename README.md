# Kelvi Backend

The backend for Kelvi, a "smart" Tamil dictionary.


## Dictionaries used
- [mcalpin](https://github.com/indic-dict/stardict-tamil)

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
4. Start the FastAPI server
    ```
    uv run fastapi run app/main.py
    ```
