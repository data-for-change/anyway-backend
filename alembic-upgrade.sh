#!/bin/bash

set -e
env
gcloud container clusters get-credentials anyway-dev-cluster-1 --zone europe-west3-a --project anyway-backend
POD=$(kubectl get pod -l app=my-app -o jsonpath="{.items[0].metadata.name}")
kubectl exec $POD -c anyway-backend -- alembic upgrade head'