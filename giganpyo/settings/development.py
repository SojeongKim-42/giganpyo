from .base import *

env = environ.Env(Debug=(bool, True),)  # set default values and casting
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env.dev')
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")
BASE_URL = "http://127.0.0.1:8000"
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

EMAIL_PORT = env("EMAIL_PORT") # gmail과 통신하는 포트
EMAIL_HOST_USER = env("EMAIL_HOST_USER")# 발신할 이메일
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD") # 발신할 메일의 비밀번호

CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")
CELERY_CACHE_BACKEND = env("CELERY_CACHE_BACKEND")

CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")

SITE_ID=1