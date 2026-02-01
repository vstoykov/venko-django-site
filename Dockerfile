FROM python:3.14 as build

RUN set -eux; \
    export DEBIAN_FRONTEND=noninteractive; \
    apt-get update; \
    apt-get install --no-install-recommends --no-install-suggests --yes gettext; \
    apt-get clean;

COPY pyproject.toml uv.lock /app/
WORKDIR /app/

RUN --mount=type=cache,target=/root/.cache set -eux; \
    pip install --root-user-action=ignore uv; \
    uv sync --frozen --extra=uwsgi --extra=postgres --no-dev --link-mode=copy; \
    pip uninstall --root-user-action=ignore --yes uv;

COPY ./ /app/

ENV DJANGO_ENV=production
RUN set -eux; \
    # Set secret key in order to execute collectstatic and compilemessages
    # It's not set as ENV in order to be available only during build time
    # When container is running there will be no DJANGO_SECRET_KEY in
    # the environemnt. It should be explicitly set!
    export DJANGO_SECRET_KEY=management; \
    .venv/bin/python manage.py collectstatic --no-input; \
    .venv/bin/python manage.py compilemessages --ignore=.venv; \
    mkdir -p /app/www/media; \
    chown www-data:www-data /app/www/media; \
    chmod g+w /app/www/media;


FROM python:3.14-slim as production

RUN set -eux; \
    export DEBIAN_FRONTEND=noninteractive; \
    apt-get update; \
    apt-get install --no-install-recommends --no-install-suggests --yes libxml2 media-types; \
    apt-get clean;

COPY --from=build /app/ /app/
WORKDIR /app/
ENV DJANGO_ENV=production

CMD [ "/app/.venv/bin/uwsgi", "--master", "--ini=/app/uwsgi.ini", "--http=0.0.0.0:8000", "--uid=www-data", "--gid=www-data", "--env=HOME=/app"]
