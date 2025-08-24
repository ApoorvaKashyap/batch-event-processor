# CBR Take Home Assignment

## 1. Introduction

## 2. Setup

Tested on **Ubuntu Server 24.04 LTS**.

### 2.1. Installations

#### 2.1.1. uv

_uv_ is a Python package and project manager.

It can be installed using the following command ([Documentation](https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_1)):

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 2.1.2. Docker

Install the _docker.io_ and related packages from Ubuntu repos.

```sh
sudo apt install containerd docker.io docker-buildx
```

Add your user to the `docker` group or run the docker commands with `sudo`.

```sh
sudo usermod -aG docker $USER && newgrp docker
```

#### 2.1.3. Minikube

Install the minikube binaries ([Documentation](https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download)):

```sh
curl -LO "https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64"
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
```

#### 2.1.4. kubectl

Install the kubectl executable ([Documentation](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)):

```sh
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && rm ./kubectl
```

Check the documentation linked above if any issues arise.

#### 2.1.5. Argo CLI

Install the _Argo CLI_ for submitting argo workflows ([Documentation](https://github.com/argoproj/argo-workflows/releases/)).

```sh
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
mv "./argo-$ARGO_OS-amd64" /usr/local/bin/argo
```

#### 2.1.6. Testing Installations

Check if the installed programs are working as expected by checking their versions:

```sh
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
```

### 2.2. Setting up Scripts

There are two scripts in the workflow:

1. **fake_gen**: Generates the fake events and stores them in a _events.jsonl_ file that is stored on a shared volume.
2. **aggregator**: Reads the _events.jsonl_ file and calculation the total session duration per user and saves it in a postgres database.

Before beginning, clone the repo using _git clone_:

```sh
git clone https://github.com/ApoorvaKashyap/batch-event-processor.git && cd batch-event-processor
```

Follow the steps below or alternatively run `run.sh` included in the repo.

#### 2.2.1. fake_gen

Run the following commands to generate a docker image for _fake_gen_:

```sh
docker build -t fake_gen:latest -f ./fake_gen/Dockerfile ./fake_gen/
```

#### 2.2.2. aggregator

Run the following commands to generate a docker image for _aggregator_:

```sh
docker build -t aggregator:latest -f ./aggregator/Dockerfile ./aggregator/
```

### 2.3. Setting up the Kubernetes Cluster

#### 2.3.1. Setting up Minikube

Start the Minikube cluster with the following command:

```sh
minikube start --driver=docker --container-runtime=containerd
```

#### 2.3.2. Setting up Argo

Create the argo namespace.

```sh
kubectl create namespace argo
```

Install Argo Workflows using the Quick Start manifest:

```sh
export ARGO_WORKFLOWS_VERSION="v3.7.1" # Set the desired version of Argo Workflows
kubectl apply -n argo -f "https://github.com/argoproj/argo-workflows/releases/download/${ARGO_WORKFLOWS_VERSION}/quick-start-minimal.yaml"
```

#### 2.3.3. Setting up Argo Service Account

Set up argo service account so that the workflows can access the default namespace.

```sh
kubectl create serviceaccount argo-workflow -n default
kubectl create rolebinding argo-workflow-rb --clusterrole=admin --serviceaccount=default:argo-workflow -n default
```

#### 2.3.4. Setting up PostgreSQL

The manifest for the postgres deployment is located in the `k8_manifests/postgres/postgres17.yaml` file.

Apply the PostgreSQL manifest to deploy a PostgreSQL instance:

```sh
kubectl apply -f k8_manifests/postgres/postgres17.yaml
```

#### 2.3.5. Enabling gvisor

Run the following command to enable gvisor for the Minikube cluster:

```sh
minikube addons enable gvisor
```

### 2.4. Running the Workflow

#### 2.4.1. Loading the built Docker images

To load the Docker images into the Minikube cluster, run the following commands:

```sh
minikube image load fake_gen:latest
minikube image load aggregator:latest
```

#### 2.4.2. Submitting the Workflow

To run the workflow, you can use the `argo` CLI to submit the workflow manifest located in `argo_workflows/task1.yaml`.

```sh
argo submit -n argo --watch argo_workflows/single_run.yaml
```

#### 2.4.1. Accessing the Argo UI

To access the Argo UI, you can use the following command to start a port-forwarding session:

```sh
kubectl port-forward -n argo svc/argo-server 2746:2746
```

Then, open your web browser and navigate to `http://localhost:2746` to access the Argo UI.
