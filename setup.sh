#!/usr/bin/env bash

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Minikube
curl -LO "https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64"
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && rm ./kubectl

# Install Argo CLI
# Detect OS
ARGO_OS="darwin"
if [[ "$(uname -s)" != "Darwin" ]]; then
  ARGO_OS="linux"
fi

# Download the binary
curl -sLO "https://github.com/argoproj/argo-workflows/releases/download/v3.7.1/argo-$ARGO_OS-amd64.gz"

# Unzip
gunzip "argo-$ARGO_OS-amd64.gz"

# Make binary executable
chmod +x "argo-$ARGO_OS-amd64"

# Move binary to path
sudo mv "./argo-$ARGO_OS-amd64" /usr/local/bin/argo

# Remove the downloaded file
rm "argo-$ARGO_OS-amd64.gz"


# Check Installations
# uv
uv --version

# Docker
docker version

# Minikube
minikube version

# kubectl
kubectl version --client

# Argo Workflow CLI
argo version

