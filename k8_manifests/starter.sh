#!/usr/bin/bash
minikube start --addons gvisor --driver docker --disk-size 25g

# Deploy Postgres 17
minikube kubectl -- apply -f postgres/postgres17.yaml

# Create a namespace for argo
ARGO_WORKFLOWS_VERSION="v3.7.1"
minikube kubectl -- create namespace argo
kubectl apply -n argo -f "https://github.com/argoproj/argo-workflows/releases/download/$ARGO_WORKFLOWS_VERSION/quick-start-minimal.yaml"

