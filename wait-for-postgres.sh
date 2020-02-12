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
# if $cmd; then
	# echo before commit $ANYWAY_BACKEND_DB_IMG
	# docker commit workspace_db_1 $ANYWAY_BACKEND_DB_IMG
# else
    # echo $cmd failed
# fi