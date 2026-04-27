#!make

IMAGE = saltyseadawg/kelvi-backend
IMAGE-TEST = saltyseadawg/kelvi-backend-test 

update-env:
	docker pull $(IMAGE)
	docker pull $(IMAGE-TEST)

build:
	docker build -t $(IMAGE) Dockerfile

build-test:
	docker build -t $(IMAGE-TEST) -f Dockerfile.dev .

mount:
	docker run --rm -v $(PWD):/code -it $(IMAGE-TEST)  /bin/bash

test:
	docker run --rm -v $(PWD):/code -it $(IMAGE-TEST) /bin/bash -c "pytest"

update-tamil-mapping:
	mkdir -p .venv/lib64/python3.11/site-packages/g2p/mappings/langs/tam
	cp -r mappings/* .venv/lib64/python3.11/site-packages/g2p/mappings/langs/tam
	g2p update