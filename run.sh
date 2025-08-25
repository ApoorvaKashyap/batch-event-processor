#!/usr/bin/bash

set -eux

minikube start --addons gvisor --container-runtime=containerd --docker-opt containerd=/var/run/containerd/containerd.sock

# Create the docker images for fake-gen and aggregator
docker build -t fake_gen:latest -f ./fake_gen/Dockerfile ./fake_gen/
docker build -t aggregator:latest -f ./aggregator/Dockerfile ./aggregator/

# Load the images into minikube
minikube image load fake_gen:latest
minikube image load aggregator:latest

# Create a namespace for argo and install argo workflows
export ARGO_WORKFLOWS_VERSION="v3.7.1"
kubectl create namespace argo
kubectl apply -n argo -f "https://github.com/argoproj/argo-workflows/releases/download/$ARGO_WORKFLOWS_VERSION/quick-start-minimal.yaml"

# Create a service account for argo
kubectl create serviceaccount argo-workflow -n default
kubectl create rolebinding argo-workflow-rb --clusterrole=admin --serviceaccount=default:argo-workflow -n default

# Wait for services to be up and running
kubectl wait --for=condition=available --timeout=600s deployment/argo-server -n argo
kubectl wait --for=condition=available --timeout=600s deployment/workflow-controller -n argo
kubectl wait --for=condition=available --timeout=600s deployment/minio -n argo
kubectl wait --for=condition=available --timeout=600s deployment/httpbin -n argo

# Deploy Postgres 17
kubectl apply -f k8_manifests/postgres/postgres17.yaml

# Wait for Postgres to be up and running
kubectl wait --for=condition=available --timeout=600s deployment/postgres -n default

# Apply Argo Workflow Manifests
argo submit argo_workflows/single_run.yaml
argo cron create argo_workflows/cron_run.yaml
argo submit argo_workflows/gvisor_run.yaml

# Port forwards
kubectl port-forward -n argo deployment/argo-server 2746:2746 &
kubectl port-forward -n default deployment/postgres 5432:5432 &


