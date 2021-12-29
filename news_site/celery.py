import os
from celery import Celery
from celery.schedules import crontab
from news import tasks

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_site.settings')

app = Celery('news_site')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# register our tasks to the beat_schedule
app.conf.beat_schedule = {
    'add-every-three-hour-contrab': {
        'task': 'scrape_news',
        # 'schedule': crontab(minute=0, hour='*/3'),
        'schedule': crontab(minute=0, hour='*/1'),
        # 'schedule': crontab(minute='*/7'),
    },
}