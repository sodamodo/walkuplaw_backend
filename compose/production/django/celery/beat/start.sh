#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset


celery -A walkuplaw.walkuplaw beat -l INFO
