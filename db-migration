#!/bin/bash

set -e

gcloud container clusters get-credentials $CLOUDSDK_CONTAINER_CLUSTER --zone $CLOUDSDK_COMPUTE_ZONE --project anyway-backend
POD=$(kubectl get pods -l app=anyway-backend -o custom-columns=:metadata.name)
echo $POD
kubectl exec $POD -c anyway-backend -- alembic upgrade head