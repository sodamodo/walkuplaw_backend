#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset


celery -A bretflix.taskapp worker -l INFO
