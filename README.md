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
2. Install pip
    ```
    uv add pip
    ```
3. Install requirements
    ```
    uv pip install -r requirements/requirements.txt
    ```
4. Install current package in developer mode
    ```
    uv pip install -e .
    ```
5. Run pre-commit hooks
    ```
    pre-commit run --all
    ```
6. Start the FastAPI server
    ```
    uv run fastapi run  app/main.py
    ```
