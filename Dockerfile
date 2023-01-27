FROM python:3.8.16

RUN apt update

WORKDIR /srv/

RUN mkdir .virtualenvs

WORKDIR /srv/.virtualenvs/

RUN pip install virtualenv

RUN virtualenv giganpyo

SHELL ["/bin/bash", "-c"]

RUN source giganpyo/bin/activate

SHELL ["/bin/sh", "-c"]

WORKDIR /srv/giganpyo-server/

COPY ./ /srv/giganpyo-server/

RUN pip install gunicorn

RUN pip install --upgrade google-api-python-client

RUN pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2

RUN pip install -r /srv/giganpyo-server/requirements.txt

RUN python manage.py collectstatic --settings=giganpyo.settings.production --noinput

EXPOSE 8000

CMD ["bash", "-c", "python manage.py makemigrations --settings=giganpyo.settings.production --noinput && python manage.py migrate --settings=giganpyo.settings.production && gunicorn -w 4 --env DJANGO_SETTINGS_MODULE=giganpyo.settings.production giganpyo.wsgi --bind 0.0.0.0:8000 --timeout=30"]
