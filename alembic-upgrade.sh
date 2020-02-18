#!/bin/bash

set -e
env
which kubectl
POD=$(kubectl get pod -l app=my-app -o jsonpath="{.items[0].metadata.name}")
kubectl exec $POD -c anyway-backend -- alembic upgrade head'