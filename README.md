# Kelvi Backend

The backend for Kelvi, a "smart" Tamil dictionary.
See the frontend [here](https://github.com/saltyseadawg/kelvi-frontend).

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

## Usage
After starting the FastApi server, interact with the API by launching a web browser and navigating to the (localhost:8000/docs)[localhost:8000/docs].

## Citation

Please cite us if you use this work in a project. 

Shankhalika Srikanth, Sabrina Yu, Sophia Chan, and Madeline Solis de Ovando. 2026. [Kelvi: A Morphological Parser to Support Tamil Literacy](https://aclanthology.org/2026.bea-1.21/). In Proceedings of the 21st Workshop on Innovative Use of NLP for Building Educational Applications (BEA 2026), pages 281–291, San Diego, California, USA. Association for Computational Linguistics.

## License

This repository is licensed under MIT. See the LICENSE file for more details.