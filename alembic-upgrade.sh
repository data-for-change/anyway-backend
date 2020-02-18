#!/bin/bash

set -e
env
gcloud container clusters get-credentials anyway-dev-cluster-1 --zone europe-west3-a --project anyway-backend
POD=kubectl get pods -l app=anyway-backend -o custom-columns=:metadata.name
echo $POD
kubectl exec $POD -c anyway-backend -- alembic upgrade head