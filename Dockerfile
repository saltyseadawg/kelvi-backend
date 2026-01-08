FROM python:3.11.13

WORKDIR /code

COPY /requirements/requirements-prod.txt /code/requirements-prod.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements-prod.txt

COPY ./app /code/app

# download stanza resources into image build instead of image run to avoid server costs
RUN ["python", "-c", "import stanza; stanza.download('ta')"]

# update g2p
RUN ["mkdir", "-p", "/usr/local/lib/python3.11/site-packages/g2p/mappings/langs/tam"]
COPY ./mappings/* /usr/local/lib/python3.11/site-packages/g2p/mappings/langs/tam
RUN ["g2p", "update"]

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]