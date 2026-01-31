---
id: 3
title: create-ai-mcp-integrator-skill
stage: general
date_iso: 2026-01-22
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: Specify User
command: ai_mcp_integrator skill creation
labels:
  - skill
  - mcp
  - openai-agents
  - chatkit
  - task-management
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .claude/skills/ai_mcp_integrator/SKILL.md
  - .claude/skills/ai_mcp_integrator/references/mcp_specification.md
  - .claude/skills/ai_mcp_integrator/references/openai_agents_sdk.md
  - .claude/skills/ai_mcp_integrator/references/chatkit_integration.md
  - .claude/skills/ai_mcp_integrator/scripts/init_ai_mcp_project.py
  - .claude/skills/ai_mcp_integrator/scripts/package_skill.py
  - .claude/skills/ai_mcp_integrator/assets/chat_component.jsx
  - .claude/skills/ai_mcp_integrator/tests/test_mcp_integration.py
  - .claude/skills/ai_mcp_integrator/README.md
  - ai_mcp_integrator.skill
tests_yaml:
  - .claude/skills/ai_mcp_integrator/tests/test_mcp_integration.py
prompt_text: |
  name: ai_mcp_integrator
  description: Specialist in OpenAI Agents SDK and Model Context Protocol (MCP). Responsible for building the AI chatbot and MCP server for task operations
  instructions: |
  -Use the Official MCP SDK to build a stateless MCP server [cite: 810].
  -Implement tools for task operations: add_task, list_tasks, complete_task, delete_task [ 815,816,817]
  -Integrate OpenAI Agents SDK for conversational logic and tool calling [cite: {810,812}
  -Use OpenAI Chatkit for the frontend conversational interface [cite: 812].
response_text: |
  Created a comprehensive AI MCP Integrator skill with:
  - Main SKILL.md file with capabilities and guidelines
  - Reference materials for MCP specification, OpenAI Agents SDK, and Chatkit integration
  - Scripts for initializing AI MCP projects
  - Asset templates for chat components
  - Test files for validation
  - Successfully packaged as ai_mcp_integrator.skill file
outcome: Successfully created a complete AI MCP Integrator skill for Claude, following the specified requirements for MCP server implementation, OpenAI Agents SDK integration, and Chatkit frontend. The skill is ready for use and distributed as a packaged .skill file.
evaluation: The skill was created with all required components and successfully packaged for distribution.
---

# Prompt Record: AI MCP Integrator Skill Creation

## Summary

Created a comprehensive AI MCP Integrator skill for Claude with expertise in OpenAI Agents SDK and Model Context Protocol (MCP), as requested.

## Changes Made

- Created main SKILL.md with name and description as specified
- Added detailed capability documentation
- Created reference materials covering MCP specification, OpenAI Agents SDK, and Chatkit integration
- Developed utility scripts for project initialization and skill packaging
- Added asset templates for chat components
- Included test files for validation
- Successfully packaged the skill as ai_mcp_integrator.skill

## Technical Details

The skill follows the architecture specified in the requirements:
- Implements MCP server using the Official MCP SDK
- Provides task operation tools (add_task, list_tasks, complete_task, delete_task)
- Integrates OpenAI Agents SDK for conversational logic and tool calling
- Includes Chatkit integration for frontend conversational interface
- Adheres to statelessness principles for MCP server design

## Outcome

The ai_mcp_integrator skill is now available for Claude to use when working on AI integration tasks, particularly for building AI chatbots and MCP servers for task operations.