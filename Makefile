setup:
	python -m venv venv
	pip install -r requirements.txt -r requirements-dev.txt

## sourcing doesn't work like it should, research
# venv-activate:
# ifeq ($(OS), Windows_NT)
# 	.\venv\Script\activate;
# else
# 	. ./venv/bin/activate;
# endif

mail-run-server:
	python -m smtpd -n -c DebuggingServer localhost:8025

db-clean:
	rm -rf migrations data/app.db

db-init:
	flask db init

db-migrate:
	flask db migrate

db-upgrade:
	flask db upgrade

db-re: db-clean db-init db-migrate db-upgrade

cloc:
	pygount --format=summary app/ scripts/ config.py manage.py

# vim: ft=make ts=4 sw=4 sts=4 noet
