#!/usr/bin/env bash

set -e

alembic upgrade head

cd /app

python3 -m app.core.database.resources.initial_data.main