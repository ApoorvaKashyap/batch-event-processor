# CBR Assignment

## Assignment Overview

You are tasked with building a batch-based event processing pipeline using **Python**, **Argo Workflows**, and **Kubernetes**, extended with **gVisor sandboxing** for enhanced security. The system should simulate events, process them in multiple workflow steps, store aggregated results in **PostgreSQL**, and demonstrate the security benefits of gVisor by running the same container both with and without sandboxing.

## Assignment Tasks

### 1. Environment Setup

- Use Minikube for Kubernetes cluster setup.
- Install Argo Workflows using the Quick Start manifest.
- Deploy a simple PostgreSQL instance to store aggregated results.
- Enable gVisor sandboxing:
  - If using Minikube: minikube addons enable gvisor.
  - Or manually install runsc and create a RuntimeClass named gvisor.

### 2. Event Simulation

Write a Python script (containerized) that generates a small set of fake events using the faker library, for example:

```json
{
  "timestamp": "2024-10-07T14:30:00",
  "userId": "user123",
  "eventType": "pageView",
  "productId": "product456",
  "sessionDuration": 180
}
```

Save these events to a shared volume or a local file accessible to other workflow steps.

### 3. Workflow Definition & Processing

Define an Argo Workflow with two steps:

1. Generate Events – run the Python event generator.
2. Aggregate & Store – read the generated file, calculate total session duration per user, and insert results into PostgreSQL.

You may use inline Python scripts in Argo Workflow or container images.

### 4. Triggering

Use a CronWorkflow to run the pipeline periodically (e.g., every 2–5 minutes).

### 5. gVisor Demonstration

Add two extra workflow steps to test security isolation:

- Pod A – Default Runtime: Tries to write a file to /host (mounted from the node).
- Pod B – gVisor Runtime: Runs the same command but with: runtimeClassName: gvisor

Compare results:

- Pod A should succeed in writing.
- Pod B should fail due to gVisor’s syscall interception.

Capture logs showing the difference.

### 6. Deployment

#### Containerize

1. Event generator (Python + Faker).
2. Aggregation script (Python).

#### Provide Kubernetes manifests

1. Argo Workflow & CronWorkflow.
2. PostgreSQL.
3. gVisor RuntimeClass (if manually configured).

### 7. Submission Guidelines

**GitHub repo** containing:

1. Argo Workflow YAML (main pipeline + gVisor demo).
2. Python scripts & Dockerfiles.
3. Kubernetes manifests (including gVisor RuntimeClass if required).
4. README with setup instructions and explanation of gVisor results.
5. If partial, list completed and pending tasks.
