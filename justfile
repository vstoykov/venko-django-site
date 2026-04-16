start: runserver

runserver: compilemessages collectstatic migrate
    uv run manage.py runserver

test: collectstatic compilemessages 
    uv run -m pytest

shell:
    uv run manage.py shell_plus

migrate:
    uv run manage.py migrate

collectstatic:
    uv run manage.py collectstatic --no-input

makemessages:
    uv run manage.py makemessages -l bg

compilemessages:
    uv run manage.py compilemessages --ignore=.venv --ignore=.tox

upgrade-deps:
    uv lock --upgrade

