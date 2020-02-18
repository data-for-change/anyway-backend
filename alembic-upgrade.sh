#!/bin/bash

set -e
env
which kubectl
export POD kubectl get pods -l app=anyway-backend -o custom-columns=:metadata.name
kubectl exec $POD -c anyway-backend -- alembic upgrade head'