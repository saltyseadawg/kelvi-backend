FROM python:3.11.13

WORKDIR /code

COPY /requirements/requirements-prod.txt /code/requirements-prod.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements-prod.txt

COPY ./app /code/app

# download stanza resources into image build instead of image run to avoid server costs
RUN ["python", "-c", "import stanza; stanza.download('ta')"]

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]