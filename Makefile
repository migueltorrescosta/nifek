
.PHONY: run
run:
	docker-compose up

.PHONY: coverage
coverage:
	pip install coverage && coverage erase && coverage run manage.py test && coverage report && coverage html

.PHONY: perms
perms:
	sudo chown ${USER} -R . && sudo chgrp ${USER} -R .
