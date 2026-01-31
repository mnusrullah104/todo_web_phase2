import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const ChatComponent = ({ apiUrl = 'http://localhost:8000' }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm your AI task assistant. How can I help you with your tasks today?",
      sender: 'ai',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to UI immediately
    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Send message to backend AI service
      const response = await axios.post(`${apiUrl}/api/v1/chat/message`, {
        message: inputValue,
        user_id: 'current-user' // In a real app, this would be the authenticated user
      });

      // Add AI response to messages
      const aiMessage = {
        id: Date.now() + 1,
        text: response.data.response,
        sender: 'ai',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to UI
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'system',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>AI Task Assistant</h2>
        <p>Manage your tasks with natural language</p>
      </div>

      <div className="messages-area">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.sender}-message`}
          >
            <div className="message-content">
              {message.text}
            </div>
            <div className="message-timestamp">
              {formatTime(message.timestamp)}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="message ai-message">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
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
          placeholder="Ask me to add, list, complete, or delete tasks..."
          disabled={isLoading}
          className="message-input"
        />
        <button type="submit" disabled={isLoading} className="send-button">
          Send
        </button>
      </form>

      <style jsx>{`
        .chat-container {
          display: flex;
          flex-direction: column;
          height: 100vh;
          max-width: 800px;
          margin: 0 auto;
          border: 1px solid #ddd;
          border-radius: 8px;
          overflow: hidden;
          background: white;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .chat-header {
          background: #007AFF;
          color: white;
          padding: 16px;
          text-align: center;
        }

        .chat-header h2 {
          margin: 0 0 4px 0;
          font-size: 1.2rem;
        }

        .chat-header p {
          margin: 0;
          opacity: 0.9;
          font-size: 0.9rem;
        }

        .messages-area {
          flex: 1;
          overflow-y: auto;
          padding: 16px;
          background-color: #f9f9f9;
          display: flex;
          flex-direction: column;
        }

        .message {
          margin-bottom: 12px;
          padding: 12px 16px;
          border-radius: 18px;
          max-width: 70%;
          word-wrap: break-word;
          position: relative;
        }

        .user-message {
          background-color: #007AFF;
          color: white;
          margin-left: auto;
          align-self: flex-end;
        }

        .ai-message {
          background-color: #E5E5EA;
          color: black;
          margin-right: auto;
          align-self: flex-start;
        }

        .system-message {
          background-color: #FFD700;
          color: black;
          margin: 0 auto;
          text-align: center;
          font-style: italic;
          align-self: center;
        }

        .message-timestamp {
          font-size: 0.7em;
          opacity: 0.7;
          margin-top: 4px;
          text-align: right;
        }

        .input-form {
          display: flex;
          padding: 16px;
          background-color: white;
          border-top: 1px solid #eee;
        }

        .message-input {
          flex: 1;
          padding: 12px 16px;
          border: 1px solid #ddd;
          border-radius: 24px;
          margin-right: 8px;
          outline: none;
          font-size: 1rem;
        }

        .message-input:focus {
          border-color: #007AFF;
        }

        .send-button {
          padding: 12px 24px;
          background-color: #007AFF;
          color: white;
          border: none;
          border-radius: 24px;
          cursor: pointer;
          font-size: 1rem;
        }

        .send-button:disabled {
          background-color: #ccc;
          cursor: not-allowed;
        }

        .typing-indicator {
          display: flex;
          align-items: center;
        }

        .typing-indicator span {
          height: 8px;
          width: 8px;
          background-color: #666;
          border-radius: 50%;
          display: inline-block;
          margin: 0 2px;
          animation: typing 1s infinite;
        }

        .typing-indicator span:nth-child(2) {
          animation-delay: 0.2s;
        }

        .typing-indicator span:nth-child(3) {
          animation-delay: 0.4s;
        }

        @keyframes typing {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-5px); }
        }
      `}</style>
    </div>
  );
};

export default ChatComponent;