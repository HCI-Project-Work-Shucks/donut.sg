
test:
	pytest -v

lint:
	python3 -m pylint web tests models db exceptions

run:
	cd web && python3 -m flask run

deps:
	python3 -m pip install -r requirements.txt
