
test:
	pytest -v

lint:
	python3 -m pylint web tests models db exceptions

run:
	cd web && python3 -m flask run
