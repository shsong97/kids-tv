git add .
git commit -am "$1"
git push heroku master
heroku run python manage.py migrate