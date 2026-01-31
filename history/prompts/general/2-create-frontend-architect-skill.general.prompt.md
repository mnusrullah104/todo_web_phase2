---
id: 2
title: create-frontend-architect-skill
stage: general
date_iso: 2026-01-22
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: Specify User
command: frontend_architect skill creation
labels:
  - skill
  - nextjs
  - typescript
  - tailwind
  - better-auth
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .claude/skills/frontend_architect/SKILL.md
  - .claude/skills/frontend_architect/references/nextjs_patterns.md
  - .claude/skills/frontend_architect/references/tailwind_patterns.md
  - .claude/skills/frontend_architect/references/api_integration.md
  - .claude/skills/frontend_architect/scripts/init_nextjs_project.js
  - .claude/skills/frontend_architect/scripts/package_skill.py
  - .claude/skills/frontend_architect/assets/ui_components.tsx
  - .claude/skills/frontend_architect/assets/utils.ts
  - .claude/skills/frontend_architect/tests/test_components.js
  - .claude/skills/frontend_architect/README.md
  - frontend_architect.skill
tests_yaml:
  - .claude/skills/frontend_architect/tests/test_components.js
prompt_text: |
  name: frontend_architect
  description: Expert in Next.js 14+ (App Router), TypeScript, and Tailwind CSS. Responsible for building responsive user interfaces and integrating with the FastAPI backend.
  instructions: |
  Use Next.js 14+ with App Router and TypeScript [cite: 697, 790].
  Build responsive UI using Tailwind CSS [cite: 790, 791].
  Integrate with the backend via a central API client (e.g., /lib/api.ts) [cite: 790, 791].
  Use Better Auth for user authentication and manage JWT tokens in headers [cite: 695, 711].
response_text: |
  Created a comprehensive Frontend Architect skill with:
  - Main SKILL.md file with capabilities and guidelines
  - Reference materials for Next.js 14+, Tailwind CSS, and API integration
  - Scripts for initializing Next.js projects
  - Asset templates for UI components and utilities
  - Test files for validation
  - Successfully packaged as frontend_architect.skill file
outcome: Successfully created a complete Frontend Architect skill for Claude, following the specified requirements for Next.js 14+, TypeScript, Tailwind CSS, and Better Auth integration. The skill is ready for use and distributed as a packaged .skill file.
evaluation: The skill was created with all required components and successfully packaged for distribution.
---

# Prompt Record: Frontend Architect Skill Creation

## Summary

Created a comprehensive Frontend Architect skill for Claude with expertise in Next.js 14+ (App Router), TypeScript, and Tailwind CSS, as requested.

## Changes Made

- Created main SKILL.md with name and description as specified
- Added detailed capability documentation
- Created reference materials covering Next.js patterns, Tailwind CSS, and API integration
- Developed utility scripts for project initialization and skill packaging
- Added asset templates for UI components and utilities
- Included test files for validation
- Successfully packaged the skill as frontend_architect.skill

## Technical Details

The skill follows the architecture specified in the requirements:
- Uses Next.js 14+ with App Router
- Implements TypeScript for type safety
- Integrates Tailwind CSS for responsive UI
- Provides API client for backend integration
- Includes Better Auth for authentication
- Adheres to clean code and proper project structure

## Outcome

The frontend_architect skill is now available for Claude to use when working on frontend development tasks, particularly for building responsive user interfaces and integrating with the FastAPI backend.