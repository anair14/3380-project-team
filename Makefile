clean:
	rm -rf migrations data/app.db

init-db:
	flask db init

migrate-db:
	flask db migrate

upgrade-db:
	flask db upgrade

cloc:
	pygount --format=summary app/
