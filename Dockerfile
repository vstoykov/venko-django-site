FROM python:3.8

RUN apt-get update \
    && apt-get install -y gettext \
    && apt-get clean \
    && pip install uwsgi "pipenv==2024.0.2" 

WORKDIR /app/
COPY Pipfile* /app/
RUN pipenv sync --system
COPY ./ /app/
ENV DJANGO_ENV=production
RUN DJANGO_SECRET_KEY=management python manage.py collectstatic --no-input \
    && DJANGO_SECRET_KEY=management python manage.py compilemessages \
    && chown -R root:www-data /app \
    && chmod g+w /app \
    && chmod g+w /app/www

CMD [ "uwsgi", "--master", "--ini=uwsgi.ini", "--http=0.0.0.0:8000", "--uid=www-data", "--gid=www-data"]
