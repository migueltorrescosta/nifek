
.PHONY: run
run:
	docker-compose up

.PHONY: coverage
coverage:
	pip install coverage && coverage erase && coverage run manage.py test && coverage report
