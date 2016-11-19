@echo staging source
git add .
@echo commit
git commit -am %1
@echo heroku push
git push heroku master
@echo heroku db migration
heroku run python manage.py migrate