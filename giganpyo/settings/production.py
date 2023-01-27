from .base import *

env = environ.Env(Debug=(bool, True),)  # set default values and casting
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env.prod')
)

CELERY_BROKER_URL = env("CELERY_BROKER_URL")
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")
CELERY_CACHE_BACKEND = env("CELERY_CACHE_BACKEND")