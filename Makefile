#!make

IMAGE = saltyseadawg/kelvi-backend

build:
	docker build -t $(IMAGE) .

update-tamil-mapping:
	mkdir -p .venv/lib64/python3.11/site-packages/g2p/mappings/langs/tam
	cp -r mappings/* .venv/lib64/python3.11/site-packages/g2p/mappings/langs/tam
	g2p update