#!/usr/bin/env bash

set -e

alembic upgrade head

cd /app

python3 -m app.resources.initial_data.initial_data