# kids tv program manager

어린이들이 좋아하는 유투브 동영상 모음 사이트입니다.

## setup virtual environment up and git clone

	pip install virtualenv
	virtualenv venv
	cd venv\scripts
	activate
	git clone https://github.com/shsong97/kids-tv.git
	pip install -r requirements.txt

## database migrate and run test server

	python manage.py migrate
	python manage.py createsuperuser
	python manage.py runserver

## gmail setting

	fix your gmail accounts in "credentials.json"

## set up git and heroku config

	heroku login
	git remote -v ( git remote status ) 
	heroku git:remote kids-tv ( git remote setting )

## test run
	
	cd venv\scripts
	activate
	python manage.py runserver
	git push origin master
	git push heroku master ( if conflicts then set -f option )

	