# Cloud Native DevOps Skill

This skill provides expertise in Docker, Kubernetes (Minikube/DOKS), Helm, and Dapr for containerization, orchestration, and event-driven architecture.

## Overview

The Cloud Native DevOps skill transforms Claude into an expert for cloud-native development tasks, particularly for implementing:
- Application containerization with Docker and Gordon AI Agent
- Kubernetes deployments and management with kubectl-ai and kagent
- Helm chart creation for local and cloud deployment
- Dapr for service invocation, state management, and Kafka pub/sub

## Components

### SKILL.md
Main skill definition with capabilities and guidelines

### References
- `docker_containerization.md` - Docker best practices and Gordon AI Agent integration
- `kubernetes_deployment.md` - Kubernetes deployment patterns and kubectl-ai/kagent usage
- `helm_charts.md` - Helm chart creation and management
- `dapr_integration.md` - Dapr for service invocation, state management, and pub/sub

### Scripts
- `init_cloud_native_project.py` - Scaffold a new cloud native project with Docker, Kubernetes, Helm, and Dapr

### Assets
- `sample_app.js` - Sample Node.js application demonstrating cloud native patterns

### Tests
- `test_cloud_native_setup.py` - Validation tests for cloud native setup

## Usage

This skill should be invoked when working on:
- Docker containerization with Gordon AI Agent
- Kubernetes cluster management with Minikube/DOKS
- Helm chart creation and deployment
- Dapr integration for microservices
- Cloud-native CI/CD pipelines
- Event-driven architecture with Kafka

## Key Guidelines

1. Containerize applications using Docker and Gordon (AI Agent) [cite: 827]
2. Create Helm charts for local and cloud deployment [cite: 827]
3. Manage Kubernetes resources using kubectl-ai and kagent [cite: 827]
4. Implement Dapr for service invocation, state management, and Kafka pub/sub [cite: 497, 505]
5. Follow security best practices for containers and orchestration
6. Use proper resource management and monitoring