#!/bin/bash

set -e
env
gcloud container clusters get-credentials anyway-dev-cluster-1 --zone europe-west3-a --project anyway-backend && kubectl get pods -l app=my-app -o custom-columns=:metadata.name
#echo $POD
#kubectl exec $POD -c anyway-backend -- alembic upgrade head