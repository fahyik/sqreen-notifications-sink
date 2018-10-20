#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

sqreen-start gunicorn 'sqreen_sink:create_app()' \
    --config='/gunicorn_config.py' \
	--log-config='/gunicorn_logging.conf'

