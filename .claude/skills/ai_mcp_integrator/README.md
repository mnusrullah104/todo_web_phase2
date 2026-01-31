# AI MCP Integrator Skill

This skill provides expertise in OpenAI Agents SDK and Model Context Protocol (MCP) for building AI chatbots and MCP servers for task operations.

## Overview

The AI MCP Integrator skill transforms Claude into an expert for AI integration tasks, particularly for implementing:
- MCP (Model Context Protocol) servers using the Official MCP SDK
- OpenAI Agent integrations with conversational logic
- Task operation tools (add_task, list_tasks, complete_task, delete_task)
- Conversational interfaces using OpenAI Chatkit

## Components

### SKILL.md
Main skill definition with capabilities and guidelines

### References
- `mcp_specification.md` - MCP protocol specifications and implementation patterns
- `openai_agents_sdk.md` - OpenAI Agents SDK integration and tool calling
- `chatkit_integration.md` - OpenAI Chatkit frontend integration

### Scripts
- `init_ai_mcp_project.py` - Scaffold a new AI MCP project with OpenAI Agents and Chatkit

### Assets
- `chat_component.jsx` - React chat component for conversational interface

### Tests
- `test_mcp_integration.py` - Validation tests for MCP and OpenAI integration

## Usage

This skill should be invoked when working on:
- MCP server implementations
- OpenAI Agent integrations
- Conversational AI interfaces
- Task management systems with AI
- State management for AI interactions

## Key Guidelines

1. Use the Official MCP SDK to build stateless MCP servers
2. Implement task operation tools: add_task, list_tasks, complete_task, delete_task
3. Integrate OpenAI Agents SDK for conversational logic and tool calling
4. Use OpenAI Chatkit for the frontend conversational interface
5. Follow security best practices for AI integrations