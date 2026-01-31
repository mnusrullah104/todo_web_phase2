---
id: 1
title: create-python-specialist-skill
stage: general
date_iso: 2026-01-22
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: Specify User
command: python_specialist skill creation
labels:
  - skill
  - python
  - fastapi
  - sqlmodel
  - uv
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .claude/skills/python_specialist/SKILL.md
  - .claude/skills/python_specialist/references/python_best_practices.md
  - .claude/skills/python_specialist/references/fastapi_patterns.md
  - .claude/skills/python_specialist/references/sqlmodel_patterns.md
  - .claude/skills/python_specialist/scripts/init_fastapi_project.py
  - .claude/skills/python_specialist/scripts/package_skill.py
  - .claude/skills/python_specialist/assets/task_routes_template.py
  - .claude/skills/python_specialist/tests/test_python_patterns.py
  - .claude/skills/python_specialist/README.md
  - python_specialist.skill
tests_yaml:
  - .claude/skills/python_specialist/tests/test_python_patterns.py
prompt_text: |
  name: python_specialist I
  description: Expert in Python 3.13+, FastAPI, SOLModel, and UV. Responsible for implementing back-end logic, RESTful APIs, and database integrations for the Todo application.
  instructions: I
  Use Python 3.13+ and UV for package management [cite: 658, 657].
  Implement RESTful APIs using FastAPI [cite: 692, 697].
  Use SQLModel for ORM and database interactions with Neon PostgreSQL [cite: 697, 792].
  Adhere to clean code principles and proper project structure defined in the constitution[cite: 655].
response_text: |
  Created a comprehensive Python Specialist skill with:
  - Main SKILL.md file with capabilities and guidelines
  - Reference materials for Python 3.13+, FastAPI, and SQLModel patterns
  - Scripts for initializing FastAPI projects and packaging skills
  - Asset templates for common API patterns
  - Test files for validation
  - Successfully packaged as python_specialist.skill file
outcome: Successfully created a complete Python Specialist skill for Claude, following the specified requirements for Python 3.13+, FastAPI, SQLModel, and UV usage. The skill is ready for use and distributed as a packaged .skill file.
evaluation: The skill was created with all required components and successfully packaged for distribution.
---

# Prompt Record: Python Specialist Skill Creation

## Summary

Created a comprehensive Python Specialist skill for Claude with expertise in Python 3.13+, FastAPI, SQLModel, and UV, as requested.

## Changes Made

- Created main SKILL.md with name and description as specified
- Added detailed capability documentation
- Created reference materials covering Python best practices, FastAPI patterns, and SQLModel patterns
- Developed utility scripts for project initialization and skill packaging
- Added asset templates for common API development tasks
- Included test files for validation
- Successfully packaged the skill as python_specialist.skill

## Technical Details

The skill follows the architecture specified in the requirements:
- Uses Python 3.13+ with modern features
- Implements FastAPI for RESTful API development
- Integrates SQLModel for ORM and database interactions
- Leverages UV for package management
- Adheres to clean code principles and proper project structure

## Outcome

The python_specialist skill is now available for Claude to use when working on Python backend development tasks, particularly for implementing back-end logic, RESTful APIs, and database integrations for the Todo application.