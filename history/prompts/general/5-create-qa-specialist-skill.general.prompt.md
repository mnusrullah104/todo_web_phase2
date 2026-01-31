---
id: 5
title: create-qa-specialist-skill
stage: general
date_iso: 2026-01-22
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: Specify User
command: qa_specialist skill creation
labels:
  - skill
  - qa
  - testing
  - verification
  - acceptance-criteria
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .claude/skills/qa_specialist/SKILL.md
  - .claude/skills/qa_specialist/references/acceptance_criteria_verification.md
  - .claude/skills/qa_specialist/references/api_endpoint_testing.md
  - .claude/skills/qa_specialist/references/error_handling_validation.md
  - .claude/skills/qa_specialist/scripts/automated_qa_runner.py
  - .claude/skills/qa_specialist/scripts/package_skill.py
  - .claude/skills/qa_specialist/assets/sample_test_config.yaml
  - .claude/skills/qa_specialist/tests/test_qa_processes.py
  - .claude/skills/qa_specialist/README.md
  - qa_specialist.skill
tests_yaml:
  - .claude/skills/qa_specialist/tests/test_qa_processes.py
prompt_text: |
  name: qa specialist
  description: Responsible for ensuring code quality, running tests, and verifying that implementations meet the acceptance criteria defined in the specs.
  instructions: |
  Verify every implementation against the specific Phase's Acceptance Criteria [cite: 795].
  Ensure all REST endpoints and MCP tools are tested for correctness [cite: 797, 815].
  Check for proper error handling (e.g., 401 Unauthorized for missing JWTs) [cite: 724, 792].
response_text: |
  Created a comprehensive QA Specialist skill with:
  - Main SKILL.md file with capabilities and guidelines
  - Reference materials for acceptance criteria verification, API endpoint testing, and error handling validation
  - Automated QA testing framework script
  - Sample test configuration asset
  - Test files for validation
  - Successfully packaged as qa_specialist.skill file
outcome: Successfully created a complete QA Specialist skill for Claude, following the specified requirements for verifying implementations against acceptance criteria, testing REST endpoints and MCP tools, and validating error handling. The skill is ready for use and distributed as a packaged .skill file.
evaluation: The skill was created with all required components and successfully packaged for distribution.
---

# Prompt Record: QA Specialist Skill Creation

## Summary

Created a comprehensive QA Specialist skill for Claude with expertise in ensuring code quality, running tests, and verifying implementations against acceptance criteria.

## Changes Made

- Created main SKILL.md with name and description as specified
- Added detailed capability documentation
- Created reference materials covering acceptance criteria verification, API endpoint testing, and error handling validation
- Developed automated testing framework for API validation
- Added sample test configuration
- Included test files for validation
- Successfully packaged the skill as qa_specialist.skill

## Technical Details

The skill follows the architecture specified in the requirements:
- Implements verification against acceptance criteria
- Provides testing for REST endpoints and MCP tools
- Validates proper error handling including 401 Unauthorized for missing JWTs
- Includes automated testing framework
- Adheres to quality assurance best practices

## Outcome

The qa_specialist skill is now available for Claude to use when performing quality assurance tasks, particularly for ensuring code quality, running tests, and verifying that implementations meet the acceptance criteria defined in the specs.