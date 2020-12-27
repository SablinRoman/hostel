
shell:
	@python3 manage.py shell

run:
	@python3 manage.py runserver

import:
	@python3 /home/roman/hostel/hostel/service/exel_work.py

mm:
	@python3 manage.py makemigrations

migrate:
	@python3 manage.py migrate

full_del_db:
	@rm -rf $$(pwd)/db.sqlite3
	@find $$(pwd)/hostel/migrations/* ! -name "__init__.py" -delete


