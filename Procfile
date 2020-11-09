release: python manage.py migrate
release: python scrape.py
web: gunicorn news_site.wsgi --log-file -
