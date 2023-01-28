import os

from celery import Celery
from giganpyo.settings import base as settings

# if settings.DEBUG:
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'giganpyo.settings.development')
# # Set the default Django settings module for the 'celery' program.
# else:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'giganpyo.settings.production')

app = Celery('giganpyo')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('giganpyo.settings.production', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')