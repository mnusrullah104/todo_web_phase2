---
id: 4
title: create-cloud-native-devops-skill
stage: general
date_iso: 2026-01-22
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: Specify User
command: cloud_native_devops skill creation
labels:
  - skill
  - docker
  - kubernetes
  - helm
  - dapr
  - cloud-native
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .claude/skills/cloud_native_devops/SKILL.md
  - .claude/skills/cloud_native_devops/references/docker_containerization.md
  - .claude/skills/cloud_native_devops/references/kubernetes_deployment.md
  - .claude/skills/cloud_native_devops/references/helm_charts.md
  - .claude/skills/cloud_native_devops/references/dapr_integration.md
  - .claude/skills/cloud_native_devops/scripts/init_cloud_native_project.py
  - .claude/skills/cloud_native_devops/scripts/package_skill.py
  - .claude/skills/cloud_native_devops/assets/sample_app.js
  - .claude/skills/cloud_native_devops/tests/test_cloud_native_setup.py
  - .claude/skills/cloud_native_devops/README.md
  - cloud_native_devops.skill
tests_yaml:
  - .claude/skills/cloud_native_devops/tests/test_cloud_native_setup.py
prompt_text: |
  name: cloud_native_devops
  description: Expert in Docker, Kubernetes (Minikube/DOKS), Helm, and Dapr. Responsible for containerization, orchestration, and event-driven architecture.
  instructions: |
  -Containerize applications using Docker and Gordon (AI Agent) [cite: 827].
  -Create Helm charts for local and cloud deployment [cite: 827].
  -Manage Kubernetes resources using kubectl-ai and kagent [cite: 827].
  -Implement Dapr for service invocation, state management, and Kafka pub/sub[cite: 497, 505].
response_text: |
  Created a comprehensive Cloud Native DevOps skill with:
  - Main SKILL.md file with capabilities and guidelines
  - Reference materials for Docker, Kubernetes, Helm, and Dapr
  - Scripts for initializing cloud native projects
  - Asset templates for sample applications
  - Test files for validation
  - Successfully packaged as cloud_native_devops.skill file
outcome: Successfully created a complete Cloud Native DevOps skill for Claude, following the specified requirements for Docker containerization, Kubernetes orchestration, Helm chart creation, and Dapr integration. The skill is ready for use and distributed as a packaged .skill file.
evaluation: The skill was created with all required components and successfully packaged for distribution.
---

# Prompt Record: Cloud Native DevOps Skill Creation

## Summary

Created a comprehensive Cloud Native DevOps skill for Claude with expertise in Docker, Kubernetes (Minikube/DOKS), Helm, and Dapr, as requested.

## Changes Made

- Created main SKILL.md with name and description as specified
- Added detailed capability documentation
- Created reference materials covering Docker, Kubernetes, Helm, and Dapr integration
- Developed utility scripts for project initialization and skill packaging
- Added asset templates for sample applications
- Included test files for validation
- Successfully packaged the skill as cloud_native_devops.skill

## Technical Details

The skill follows the architecture specified in the requirements:
- Implements Docker containerization with Gordon AI Agent
- Provides Kubernetes management with kubectl-ai and kagent
- Includes Helm chart creation for local and cloud deployment
- Implements Dapr for service invocation, state management, and Kafka pub/sub
- Adheres to cloud-native best practices for containerization and orchestration

## Outcome

The cloud_native_devops skill is now available for Claude to use when working on cloud-native development tasks, particularly for containerization, orchestration, and event-driven architecture.