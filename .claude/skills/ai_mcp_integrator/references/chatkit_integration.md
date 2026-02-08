# OpenAI Chatkit Integration

## Overview

OpenAI Chatkit provides a frontend conversational interface for interacting with AI models. It offers a ready-made UI for chat experiences that can be integrated with backend AI services and MCP servers.

## Chatkit Setup

### Basic Configuration
```javascript
// chatkit.js
import { createChat } from '@openai/chatkit';

class ChatInterface {
  constructor(config) {
    this.config = config;
    this.chat = null;
  }

  async initialize() {
    this.chat = await createChat({
      projectId: this.config.projectId,
      instanceLocator: this.config.instanceLocator,
      tokenProvider: this.createTokenProvider(this.config.secretKey)
    });

    return this.chat;
  }

  createTokenProvider(secretKey) {
    return {
      async fetchToken(userId) {
        // In a real app, this would call your backend to generate a token
        const response = await fetch('/api/chatkit/token', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${secretKey}`
          },
          body: JSON.stringify({ userId })
        });

        const data = await response.json();
        return data.token;
      }
    };
  }
}
```

## Frontend Integration

### React Component Implementation
```jsx
// ChatComponent.jsx
import React, { useState, useEffect, useRef } from 'react';

const ChatComponent = ({ apiKey, projectId }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Initialize Chatkit
  useEffect(() => {
    const initializeChat = async () => {
      try {
        const chatkit = new ChatInterface({
          projectId,
          instanceLocator: 'YOUR_INSTANCE_LOCATOR',
          secretKey: apiKey
        });

        const chat = await chatkit.initialize();

        // Subscribe to room messages
        const roomId = await chat.rooms.create({
          name: 'General',
          addUserIds: ['user1']
        });

        chat.messages.subscribe(roomId, {
          onMessage: (message) => {
            setMessages(prev => [...prev, {
              id: message.id,
              text: message.text,
              sender: message.senderId,
              timestamp: message.createdAt
            }]);
          }
        });
      } catch (error) {
        console.error('Error initializing chat:', error);
      }
    };

    initializeChat();
  }, [projectId, apiKey]);

  // Auto-scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to UI immediately
    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'currentUser',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Send message to backend AI service
      const response = await fetch('/api/chat/message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: inputValue,
          userId: 'currentUser'
        })
      });

      const data = await response.json();

      // Add AI response to messages
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        text: data.response,
        sender: 'aiAssistant',
        timestamp: new Date()
      }]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to UI
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'system',
        timestamp: new Date()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages-area">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.sender}`}
          >
            <div className="message-content">{message.text}</div>
            <div className="message-timestamp">
              {new Date(message.timestamp).toLocaleTimeString()}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message aiAssistant">
            <div className="message-content">
              <span className="typing-indicator">AI is thinking...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your message..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatComponent;
```

## Backend API for Chat Integration

### Express.js Backend
```javascript
// server.js
const express = require('express');
const cors = require('cors');
const { createAgent } = require('./task-agent'); // Our OpenAI agent

const app = express();
app.use(cors());
app.use(express.json());

// Initialize the task agent
const agent = createAgent(process.env.OPENAI_API_KEY);

// Endpoint to handle chat messages
app.post('/api/chat/message', async (req, res) => {
  try {
    const { message, userId } = req.body;

    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    // Process the message with the AI agent
    const response = await agent.processMessage(message, userId);

    res.json({
      response: response,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error processing message:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Sorry, something went wrong processing your request.'
    });
  }
});

// Endpoint for Chatkit token generation
app.post('/api/chatkit/token', async (req, res) => {
  try {
    const { userId } = req.body;

    // In a real implementation, validate the user and generate a Chatkit token
    // This is a simplified example
    const token = generateChatkitToken(userId);

    res.json({ token });
  } catch (error) {
    console.error('Error generating token:', error);
    res.status(500).json({ error: 'Token generation failed' });
  }
});

app.listen(3001, () => {
  console.log('Chat server running on port 3001');
});
```

## Integration with Task Operations

### Task-Specific Chat Commands
```javascript
// task-chat-integration.js
class TaskChatIntegration {
  constructor(agent, mcpClient) {
    this.agent = agent;
    this.mcpClient = mcpClient;
  }

  async processMessage(message, userId) {
    // Check if message contains task-related commands
    if (this.isTaskCommand(message)) {
      return await this.handleTaskCommand(message);
    }

    // Otherwise, process with AI agent
    return await this.agent.process(message);
  }

  isTaskCommand(message) {
    const taskCommands = [
      /add.*task/i,
      /create.*task/i,
      /list.*task/i,
      /show.*task/i,
      /complete.*task/i,
      /finish.*task/i,
      /delete.*task/i,
      /remove.*task/i
    ];

    return taskCommands.some(pattern => pattern.test(message));
  }

  async handleTaskCommand(message) {
    // Parse the command and extract relevant information
    const command = this.parseTaskCommand(message);

    switch (command.action) {
      case 'add':
        return await this.handleAddTask(command.params);
      case 'list':
        return await this.handleListTasks();
      case 'complete':
        return await this.handleCompleteTask(command.params);
      case 'delete':
        return await this.handleDeleteTask(command.params);
      default:
        return "I didn't understand that task command. Try phrases like 'add task', 'list tasks', 'complete task', or 'delete task'.";
    }
  }

  parseTaskCommand(message) {
    // Simple parsing logic - in production, use NLP
    const lowerMsg = message.toLowerCase();

    if (lowerMsg.includes('add') || lowerMsg.includes('create')) {
      // Extract task name and description
      const match = message.match(/(?:add|create)\s+(?:a\s+)?task\s+(.+)/i);
      if (match) {
        return {
          action: 'add',
          params: {
            name: match[1].trim()
          }
        };
      }
    } else if (lowerMsg.includes('list') || lowerMsg.includes('show')) {
      return { action: 'list' };
    } else if (lowerMsg.includes('complete') || lowerMsg.includes('finish')) {
      // Extract task ID or name
      const match = message.match(/(?:complete|finish)\s+(?:task\s+)?(.+)/i);
      if (match) {
        return {
          action: 'complete',
          params: {
            task_id: match[1].trim()
          }
        };
      }
    } else if (lowerMsg.includes('delete') || lowerMsg.includes('remove')) {
      // Extract task ID or name
      const match = message.match(/(?:delete|remove)\s+(?:task\s+)?(.+)/i);
      if (match) {
        return {
          action: 'delete',
          params: {
            task_id: match[1].trim()
          }
        };
      }
    }

    return { action: 'unknown' };
  }

  async handleAddTask(params) {
    try {
      // Call MCP server to add task
      const result = await this.mcpClient.callTool("task_server", "prompts/add_task", {
        name: params.name,
        description: params.description || ""
      });

      return `Task "${result.result.name}" has been added successfully with ID: ${result.result.id}`;
    } catch (error) {
      return `Error adding task: ${error.message}`;
    }
  }

  async handleListTasks() {
    try {
      // Call MCP server to list tasks
      const result = await this.mcpClient.callTool("task_server", "prompts/list_tasks", {});

      if (result.result.length === 0) {
        return "No tasks found.";
      }

      const taskList = result.result.map(task =>
        `- ${task.completed ? '✓' : '○'} ${task.name} (ID: ${task.id})`
      ).join('\n');

      return `Here are your tasks:\n${taskList}`;
    } catch (error) {
      return `Error listing tasks: ${error.message}`;
    }
  }

  async handleCompleteTask(params) {
    try {
      // Call MCP server to complete task
      const result = await this.mcpClient.callTool("task_server", "prompts/complete_task", {
        task_id: params.task_id
      });

      return result.result ?
        `Task "${params.task_id}" has been marked as completed.` :
        `Could not find task with ID: ${params.task_id}`;
    } catch (error) {
      return `Error completing task: ${error.message}`;
    }
  }

  async handleDeleteTask(params) {
    try {
      // Call MCP server to delete task
      const result = await this.mcpClient.callTool("task_server", "prompts/delete_task", {
        task_id: params.task_id
      });

      return result.result ?
        `Task "${params.task_id}" has been deleted.` :
        `Could not find task with ID: ${params.task_id}`;
    } catch (error) {
      return `Error deleting task: ${error.message}`;
    }
  }
}
```

## Styling and UI Components

### CSS for Chat Interface
```css
/* chat-styles.css */
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 800px;
  margin: 0 auto;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}

.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background-color: #f9f9f9;
}

.message {
  margin-bottom: 12px;
  padding: 8px 12px;
  border-radius: 18px;
  max-width: 70%;
  word-wrap: break-word;
}

.message.currentUser {
  background-color: #007AFF;
  color: white;
  margin-left: auto;
  text-align: right;
}

.message.aiAssistant {
  background-color: #E5E5EA;
  color: black;
  margin-right: auto;
}

.message.system {
  background-color: #FFD700;
  color: black;
  margin: 0 auto;
  text-align: center;
  font-style: italic;
}

.message-timestamp {
  font-size: 0.7em;
  opacity: 0.7;
  margin-top: 4px;
}

.input-form {
  display: flex;
  padding: 16px;
  background-color: white;
  border-top: 1px solid #eee;
}

.input-form input {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 24px;
  margin-right: 8px;
  outline: none;
}

.input-form input:focus {
  border-color: #007AFF;
}

.input-form button {
  padding: 12px 20px;
  background-color: #007AFF;
  color: white;
  border: none;
  border-radius: 24px;
  cursor: pointer;
}

.input-form button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.typing-indicator {
  display: inline-block;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
```

## Security Considerations

### Authentication and Authorization
```javascript
// auth-middleware.js
const jwt = require('jsonwebtoken');

const authenticateUser = (req, res, next) => {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing or invalid authorization header' });
  }

  const token = authHeader.substring(7);

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.userId = decoded.userId;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
};

module.exports = { authenticateUser };
```

### Input Validation and Sanitization
```javascript
const sanitizeInput = (input) => {
  // Remove potentially dangerous characters
  return input.replace(/[<>]/g, '');
};

const validateMessage = (message) => {
  if (!message || typeof message !== 'string') {
    throw new Error('Message must be a non-empty string');
  }

  if (message.length > 1000) {
    throw new Error('Message exceeds maximum length of 1000 characters');
  }

  return sanitizeInput(message);
};
```