#!/bin/bash
# wait-for-postgres.sh

set -e

host="$1"
shift
cmd="$@"

until pg_isready -d $DATABASE_URL -q; do
  >&2 echo "Postgres is not ready to receive connections yet - sleeping"
  sleep 10
done

>&2 echo "Postgres is up and running - executing migration command"
exec $cmd
# if $cmd; then
	# echo before commit $ANYWAY_BACKEND_DB_IMG
	# docker ps
	# docker images
	# docker commit workspace_db_1 $ANYWAY_BACKEND_DB_IMG
	# echo after commit $ANYWAY_BACKEND_DB_IMG
	# docker ps
	# docker images
# else
    # echo $cmd failed
# fi