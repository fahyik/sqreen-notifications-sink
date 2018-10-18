#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset

exec gunicorn --config gunicorn_config.py sqreen_sink