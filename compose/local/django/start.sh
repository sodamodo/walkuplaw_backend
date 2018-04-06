#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete


python manage.py makemigrations
python manage.py migrate
#python manage.py makemigrations television
#python manage.py migrate television
#python manage.py runserver_plus 0.0.0.0:8000
python manage.py test
