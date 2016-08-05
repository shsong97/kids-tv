# kids tv program manager

어린이들이 좋아하는 유투브 동영상 모음 사이트입니다.

## install

	pip install virtualenv
	virtualenv venv
	cd venv\scripts
	activate
	git clone https://github.com/shsong97/kids-tv.git
	pip install -r requirements.txt

## setup and test

	python manage.py migrate
	python manage.py createsuperuser
	python manage.py runserver



