FROM python:3.14 AS build

RUN pip install --root-user-action=ignore --no-cache-dir uv;

COPY pyproject.toml uv.lock /app/
WORKDIR /app/

RUN --mount=type=cache,target=/root/.cache set -eux; \
    uv sync --frozen --extra=uwsgi --extra=postgres --no-dev --link-mode=copy;

FROM python:3.14-slim AS production

RUN set -eux; \
    export DEBIAN_FRONTEND=noninteractive; \
    apt-get update; \
    apt-get install --no-install-recommends --no-install-suggests --yes libxml2 media-types gettext curl; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists;

COPY --from=build /app/.venv /app/.venv
COPY ./ /app/

WORKDIR /app/
ENV PATH=/app/.venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_ENV=production
ENV DJANGO_DATA_DIR=/var/www

RUN set -eux; \
    # Set secret key in order to execute collectstatic and compilemessages
    # It's not set as ENV in order to be available only during build time
    # When container is running there will be no DJANGO_SECRET_KEY in
    # the environemnt. It should be explicitly set!
    export DJANGO_SECRET_KEY=management; \
    .venv/bin/python manage.py collectstatic --no-input; \
    .venv/bin/python manage.py compilemessages --ignore=.venv; \
    mkdir -p /var/www/media; \
    chown -R www-data:www-data /var/www/; \
    chmod g+w /var/www/media;

USER www-data:www-data

CMD [ "/app/runserver" ]

