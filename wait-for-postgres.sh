#!/bin/bash
# wait-for-postgres.sh

set -e

host="$1"
shift
cmd="$@"

until pg_isready -d $DATABASE_URL -q; do
  >&2 echo "Postgres is not ready to recieve connections yet - sleeping"
  sleep 10
done

>&2 echo "Postgres is up and running - executing migration command"
if $cmd; then
    echo command returned true
	docker commit workspace_db_1 $ANYWAY_BACKEND_DB_IMG
else
    echo $cmd failed
fi