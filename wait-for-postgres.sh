#!/bin/bash
# wait-for-postgres.sh

set -e

host="$1"
shift
cmd="$@"

echo "Starting alembic migration. Checking if db is up....."
until pg_isready -d $DATABASE_URL -q; do
  >&2 echo "db is not up yet - sleeping"
  sleep 10
done

>&2 echo "db is up and running - executing migration command"
exec $cmd
