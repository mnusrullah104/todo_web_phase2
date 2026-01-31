#!/usr/bin/env python3
"""
Script to initialize a new Cloud Native DevOps project with Docker, Kubernetes, Helm, and Dapr
"""

import os
import sys
from pathlib import Path
import yaml
import json

def create_project_structure(project_name):
    """Create the basic project structure"""
    base_path = Path(project_name)
    base_path.mkdir(exist_ok=True)

    # Create directories
    (base_path / ".gordon").mkdir(exist_ok=True)
    (base_path / ".kagent").mkdir(exist_ok=True)
    (base_path / "dapr-components").mkdir(exist_ok=True)
    (base_path / "helm-chart").mkdir(exist_ok=True)
    (base_path / "helm-chart" / "templates").mkdir(exist_ok=True)
    (base_path / "k8s-manifests").mkdir(exist_ok=True)
    (base_path / "scripts").mkdir(exist_ok=True)
    (base_path / "tests").mkdir(exist_ok=True)

    return base_path

def create_dockerfile(base_path):
    """Create a Dockerfile for the application"""
    dockerfile_content = '''# This Dockerfile is managed by Gordon AI Agent
FROM node:18-alpine AS base
LABEL maintainer="gordon-ai-agent"

# Install dependencies with security in mind
RUN apk add --no-cache dumb-init curl

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install production dependencies only
RUN npm ci --only=production --audit=false && npm cache clean --force

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \\
    adduser -S nextjs -u 1001

# Copy application code
COPY --chown=nextjs:nodejs . .

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]
CMD ["npm", "start"]

# Add health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
  CMD curl -f http://localhost:3000/health || exit 1
'''

    with open(base_path / "Dockerfile", "w") as f:
        f.write(dockerfile_content)

def create_gordon_config(base_path):
    """Create Gordon AI Agent configuration"""
    gordon_config = {
        "gordon": {
            "version": "1.0",
            "project": {
                "name": project_name,
                "type": "nodejs",
                "language_version": "18"
            },
            "build": {
                "strategy": "multi-stage",
                "platforms": [
                    "linux/amd64",
                    "linux/arm64"
                ],
                "cache": {
                    "enabled": True,
                    "from": ["myapp:latest"]
                },
                "args": {
                    "NODE_ENV": "production"
                }
            },
            "security": {
                "scan_enabled": True,
                "severity_threshold": "HIGH",
                "allow_failure": False
            },
            "deployment": {
                "registry": "docker.io/username",
                "tags": [
                    "latest",
                    "{{.ShortCommit}}",
                    "{{.Tag}}"
                ]
            }
        }
    }

    with open(base_path / ".gordon" / "config.yaml", "w") as f:
        yaml.dump(gordon_config, f, default_flow_style=False)

def create_kagent_config(base_path):
    """Create kagent configuration"""
    kagent_config = {
        "version": "1.0",
        "cluster": {
            "name": f"{project_name}-cluster",
            "provider": "doks",  # or "minikube"
            "region": "nyc1"
        },
        "resources": {
            "default_limits": {
                "memory": "512Mi",
                "cpu": "500m"
            },
            "default_requests": {
                "memory": "256Mi",
                "cpu": "250m"
            }
        },
        "monitoring": {
            "enabled": True,
            "service_mesh": "dapr"
        },
        "secrets": {
            "provider": "kubernetes",
            "encryption": True
        }
    }

    with open(base_path / ".kagent" / "config.yaml", "w") as f:
        yaml.dump(kagent_config, f, default_flow_style=False)

def create_dapr_components(base_path):
    """Create Dapr component configurations"""
    # State store component
    state_store = {
        "apiVersion": "dapr.io/v1alpha1",
        "kind": "Component",
        "metadata": {
            "name": "statestore"
        },
        "spec": {
            "type": "state.redis",
            "version": "v1",
            "metadata": [
                {
                    "name": "redisHost",
                    "value": "localhost:6379"
                },
                {
                    "name": "redisPassword",
                    "secretKeyRef": {
                        "name": "redis-password",
                        "key": "password"
                    }
                },
                {
                    "name": "actorStateStore",
                    "value": "true"
                }
            ]
        },
        "scopes": ["myapp"]
    }

    # Pub/Sub component (Kafka)
    pubsub = {
        "apiVersion": "dapr.io/v1alpha1",
        "kind": "Component",
        "metadata": {
            "name": "kafka-pubsub"
        },
        "spec": {
            "type": "pubsub.kafka",
            "version": "v1",
            "metadata": [
                {
                    "name": "brokers",
                    "value": "kafka:9092"
                },
                {
                    "name": "consumerGroup",
                    "value": "myapp-consumer-group"
                },
                {
                    "name": "clientID",
                    "value": "myapp"
                },
                {
                    "name": "authRequired",
                    "value": "false"
                }
            ]
        },
        "scopes": ["myapp"]
    }

    with open(base_path / "dapr-components" / "statestore.yaml", "w") as f:
        yaml.dump(state_store, f, default_flow_style=False)

    with open(base_path / "dapr-components" / "pubsub.yaml", "w") as f:
        yaml.dump(pubsub, f, default_flow_style=False)

def create_helm_chart(base_path):
    """Create basic Helm chart structure"""
    # Chart.yaml
    chart_yaml = {
        "apiVersion": "v2",
        "name": project_name,
        "description": "A Helm chart for my cloud native application",
        "type": "application",
        "version": "0.1.0",
        "appVersion": "1.0.0",
        "maintainers": [
            {
                "name": "Developer",
                "email": "developer@example.com"
            }
        ],
        "keywords": [
            "nodejs",
            "web",
            "application",
            "dapr",
            "cloud-native"
        ]
    }

    # values.yaml
    values_yaml = {
        "replicaCount": 1,
        "image": {
            "repository": "myapp",
            "pullPolicy": "IfNotPresent",
            "tag": ""
        },
        "imagePullSecrets": [],
        "nameOverride": "",
        "fullnameOverride": "",
        "serviceAccount": {
            "create": True,
            "annotations": {},
            "name": ""
        },
        "podAnnotations": {},
        "podSecurityContext": {},
        "securityContext": {},
        "service": {
            "type": "ClusterIP",
            "port": 3000
        },
        "ingress": {
            "enabled": False,
            "className": "",
            "annotations": {},
            "hosts": [
                {
                    "host": "chart-example.local",
                    "paths": [
                        {
                            "path": "/",
                            "pathType": "ImplementationSpecific"
                        }
                    ]
                }
            ],
            "tls": []
        },
        "resources": {},
        "autoscaling": {
            "enabled": False,
            "minReplicas": 1,
            "maxReplicas": 100,
            "targetCPUUtilizationPercentage": 80
        },
        "nodeSelector": {},
        "tolerations": [],
        "affinity": {}
    }

    # Create Chart.yaml
    with open(base_path / "helm-chart" / "Chart.yaml", "w") as f:
        yaml.dump(chart_yaml, f, default_flow_style=False)

    # Create values.yaml
    with open(base_path / "helm-chart" / "values.yaml", "w") as f:
        yaml.dump(values_yaml, f, default_flow_style=False)

    # Create basic deployment template
    deployment_template = '''apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "'''+project_name+'''.fullname" . }}
  labels:
    {{- include "'''+project_name+'''.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "'''+project_name+'''.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{- include "'''+project_name+'''.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "'''+project_name+'''.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
        - name: {{ .Chart.Name }}
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: {{ .Values.service.port }}
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /health
              port: http
          readinessProbe:
            httpGet:
              path: /ready
              port: http
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
'''

    with open(base_path / "helm-chart" / "templates" / "deployment.yaml", "w") as f:
        f.write(deployment_template)

    # Create _helpers.tpl
    helpers_tpl = '''{{/*
Expand the name of the chart.
*/}}
{{- define "'''+project_name+'''.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "'''+project_name+'''.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "'''+project_name+'''.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "'''+project_name+'''.labels" -}}
helm.sh/chart: {{ include "'''+project_name+'''.chart" . }}
{{ include "'''+project_name+'''.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "'''+project_name+'''.selectorLabels" -}}
app.kubernetes.io/name: {{ include "'''+project_name+'''.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "'''+project_name+'''.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "'''+project_name+'''.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
'''

    with open(base_path / "helm-chart" / "templates" / "_helpers.tpl", "w") as f:
        f.write(helpers_tpl)

def create_k8s_manifests(base_path):
    """Create basic Kubernetes manifests"""
    # Namespace manifest
    namespace = {
        "apiVersion": "v1",
        "kind": "Namespace",
        "metadata": {
            "name": f"{project_name}-prod"
        }
    }

    # ConfigMap manifest
    configmap = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {
            "name": f"{project_name}-config",
            "namespace": f"{project_name}-prod"
        },
        "data": {
            "NODE_ENV": "production",
            "LOG_LEVEL": "info"
        }
    }

    with open(base_path / "k8s-manifests" / "namespace.yaml", "w") as f:
        yaml.dump(namespace, f, default_flow_style=False)

    with open(base_path / "k8s-manifests" / "configmap.yaml", "w") as f:
        yaml.dump(configmap, f, default_flow_style=False)

def create_scripts(base_path):
    """Create useful scripts for the project"""
    # Deployment script
    deploy_script = '''#!/bin/bash

set -e

PROJECT_NAME="{{PROJECT_NAME}}"
NAMESPACE="${PROJECT_NAME}-prod"

echo "Deploying $PROJECT_NAME to $NAMESPACE..."

# Create namespace if it doesn't exist
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Deploy using Helm
helm upgrade --install $PROJECT_NAME ./helm-chart \\
  --namespace $NAMESPACE \\
  --values ./helm-chart/values-prod.yaml \\
  --create-namespace

echo "Deployment completed!"
'''

    # Local development script
    dev_script = '''#!/bin/bash

set -e

PROJECT_NAME="{{PROJECT_NAME}}"

echo "Starting local development for $PROJECT_NAME..."

# Start Dapr with the application
dapr run --app-id $PROJECT_NAME \\
  --app-port 3000 \\
  --dapr-http-port 3500 \\
  --components-path ./dapr-components \\
  -- npm run dev

echo "Development stopped!"
'''

    # CI/CD script
    cicd_script = '''#!/bin/bash

set -e

IMAGE_TAG="${1:-latest}"
PROJECT_NAME="{{PROJECT_NAME}}"
REGISTRY="docker.io/username"

echo "Building and deploying $PROJECT_NAME:$IMAGE_TAG..."

# Build and push Docker image
gordon build --tag $IMAGE_TAG --push

# Update Helm values with new image tag
sed -i.bak "s/tag: .*/tag: $IMAGE_TAG/" ./helm-chart/values.yaml

# Deploy to cluster
helm upgrade --install $PROJECT_NAME ./helm-chart \\
  --namespace $PROJECT_NAME-prod \\
  --values ./helm-chart/values-prod.yaml \\
  --atomic

echo "CI/CD pipeline completed!"
'''

    # Make scripts executable and write them
    scripts_dir = base_path / "scripts"

    deploy_path = scripts_dir / "deploy.sh"
    with open(deploy_path, "w") as f:
        f.write(deploy_script.replace("{{PROJECT_NAME}}", project_name))
    os.chmod(deploy_path, 0o755)

    dev_path = scripts_dir / "dev.sh"
    with open(dev_path, "w") as f:
        f.write(dev_script.replace("{{PROJECT_NAME}}", project_name))
    os.chmod(dev_path, 0o755)

    cicd_path = scripts_dir / "cicd.sh"
    with open(cicd_path, "w") as f:
        f.write(cicd_script.replace("{{PROJECT_NAME}}", project_name))
    os.chmod(cicd_path, 0o755)

def create_compose_file(base_path):
    """Create a docker-compose file for local development"""
    compose_content = {
        "version": "3.8",
        "services": {
            "app": {
                "build": ".",
                "ports": [
                    "3000:3000"
                ],
                "environment": [
                    "NODE_ENV=development"
                ],
                "volumes": [
                    ".:/app",
                    "/app/node_modules"
                ],
                "depends_on": [
                    "redis",
                    "postgres",
                    "kafka"
                ]
            },
            "redis": {
                "image": "redis:7-alpine",
                "ports": [
                    "6379:6379"
                ]
            },
            "postgres": {
                "image": "postgres:15-alpine",
                "environment": {
                    "POSTGRES_DB": "myapp",
                    "POSTGRES_USER": "user",
                    "POSTGRES_PASSWORD": "password"
                },
                "ports": [
                    "5432:5432"
                ]
            },
            "kafka": {
                "image": "confluentinc/cp-kafka:7.4.0",
                "environment": {
                    "KAFKA_BROKER_ID": "1",
                    "KAFKA_ZOOKEEPER_CONNECT": "zookeeper:2181",
                    "KAFKA_ADVERTISED_LISTENERS": "PLAINTEXT://kafka:9092",
                    "KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR": "1"
                },
                "ports": [
                    "9092:9092"
                ],
                "depends_on": [
                    "zookeeper"
                ]
            },
            "zookeeper": {
                "image": "confluentinc/cp-zookeeper:7.4.0",
                "environment": {
                    "ZOOKEEPER_CLIENT_PORT": "2181",
                    "ZOOKEEPER_TICK_TIME": "2000"
                }
            }
        }
    }

    with open(base_path / "docker-compose.yaml", "w") as f:
        yaml.dump(compose_content, f, default_flow_style=False)

def create_readme(base_path, project_name):
    """Create README.md"""
    readme_content = f"""# {project_name}

Cloud Native application with Docker, Kubernetes, Helm, and Dapr integration.

## Overview

This project demonstrates cloud-native development patterns using:
- Docker for containerization
- Kubernetes for orchestration
- Helm for package management
- Dapr for distributed application runtime
- Gordon AI Agent for Docker optimization
- kagent for Kubernetes management

## Prerequisites

- Docker and Docker Compose
- Kubernetes cluster (Minikube or DOKS)
- Helm 3
- Dapr CLI
- Gordon AI Agent
- kagent

## Setup

1. Clone the repository:
```bash
git clone {project_name}
cd {project_name}
```

2. Install Dapr:
```bash
dapr init --kubernetes
```

3. Install Gordon AI Agent:
```bash
curl -L https://raw.githubusercontent.com/gordon/gordon-cli/master/install.sh | sh
```

4. Install kagent:
```bash
curl -L https://raw.githubusercontent.com/kagent/kagent-cli/master/install.sh | sh
```

## Local Development

1. Start local services:
```bash
docker-compose up -d
```

2. Run with Dapr:
```bash
dapr run --app-id {project_name} --app-port 3000 -- npm run dev
```

## Kubernetes Deployment

### Local (Minikube)

1. Start Minikube:
```bash
minikube start
```

2. Deploy with Helm:
```bash
helm install {project_name} ./helm-chart --values ./helm-chart/values-dev.yaml
```

### Cloud (DOKS)

1. Connect to your DOKS cluster:
```bash
doctl kubernetes cluster kubeconfig save <cluster-name>
```

2. Deploy with Helm:
```bash
helm install {project_name} ./helm-chart --values ./helm-chart/values-prod.yaml --namespace {project_name}-prod --create-namespace
```

## Dapr Components

Dapr components are defined in the `dapr-components/` directory:
- `statestore.yaml` - Redis state store
- `pubsub.yaml` - Kafka pub/sub

## Helm Chart

The Helm chart is located in the `helm-chart/` directory and includes:
- Deployment with Dapr sidecar
- Service configuration
- ConfigMap for environment variables
- Optional Ingress configuration
- Horizontal Pod Autoscaler

## Scripts

Useful scripts in the `scripts/` directory:
- `deploy.sh` - Deploy to Kubernetes
- `dev.sh` - Start local development
- `cicd.sh` - CI/CD pipeline

## CI/CD Pipeline

The CI/CD pipeline uses:
- Gordon for optimized Docker builds
- kagent for Kubernetes management
- Helm for deployment

## Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Application   │◄──►│    Dapr Sidecar │
│                 │    │                 │
└─────────────────┘    └─────────────────┘
                              │
    ┌─────────────────────────┼─────────────────────────┐
    │                         │                         │
┌───▼──┐                ┌─────▼─────┐            ┌─────▼─────┐
│ Redis│                │   Kafka   │            │PostgreSQL │
│State │                │  Pub/Sub  │            │ Database  │
└──────┘                └───────────┘            └───────────┘
```

## Security

- Non-root user in containers
- Resource limits configured
- Network policies (can be enabled)
- Secrets management with Kubernetes

## Monitoring

- Dapr provides built-in observability
- Configure Prometheus and Grafana for metrics
- Use Jaeger for distributed tracing
"""

    with open(base_path / "README.md", "w") as f:
        f.write(readme_content)

def main():
    if len(sys.argv) != 2:
        print("Usage: python init_cloud_native_project.py <project_name>")
        sys.exit(1)

    global project_name
    project_name = sys.argv[1]

    print(f"Creating new Cloud Native project: {project_name}")

    base_path = create_project_structure(project_name)
    create_dockerfile(base_path)
    create_gordon_config(base_path)
    create_kagent_config(base_path)
    create_dapr_components(base_path)
    create_helm_chart(base_path)
    create_k8s_manifests(base_path)
    create_scripts(base_path)
    create_compose_file(base_path)
    create_readme(base_path, project_name)

    print(f"Project {project_name} created successfully!")
    print(f"Next steps:")
    print(f"1. cd {project_name}")
    print(f"2. Review and customize configuration files")
    print(f"3. Add your application code")
    print(f"4. Run 'docker-compose up' for local development")

if __name__ == "__main__":
    main()