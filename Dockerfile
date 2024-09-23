FROM python:3.12

RUN set -eux \
    export DEBIAN_FRONTEND=noninteractive; \
    apt-get update; \
    apt-get install --no-install-recommends --no-install-suggests --yes \
        gettext; \
    apt-get remove --purge --auto-remove --yes; \
    rm -rf /var/lib/apt/lists/*;

COPY Pipfile* /app/
WORKDIR /app/

RUN set -eux; \
    pip install --root-user-action=ignore --no-cache-dir uwsgi pipenv; \
    pipenv sync --system; \
    pip uninstall --root-user-action=ignore --yes pipenv virtualenv; \
    rm -rf /root/.cache;
    
COPY ./ /app/

ENV DJANGO_ENV=production
RUN set -eux \
    # Set secret key in order to execute collectstatic and compilemessages
    # It's not set as ENV in order to be available only during build time
    # When container is running there will be no DJANGO_SECRET_KEY in 
    # the environemnt. It should be explicitly set!
    export DJANGO_SECRET_KEY=management; \
    python manage.py collectstatic --no-input; \
    python manage.py compilemessages; \
    chown -R root:www-data /app; \
    chmod g+w /app; \
    chmod g+w /app/www;

CMD [ "uwsgi", "--master", "--ini=uwsgi.ini", "--http=0.0.0.0:8000", "--uid=www-data", "--gid=www-data", "--env=HOME=/app"]
