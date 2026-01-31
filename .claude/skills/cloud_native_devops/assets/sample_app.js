// sample_app.js - Sample Node.js application for cloud native deployment

const express = require('express');
const axios = require('axios');
const app = express();

// Middleware
app.use(express.json());

// Environment variables
const PORT = process.env.PORT || 3000;
const DAPR_HTTP_ENDPOINT = process.env.DAPR_HTTP_ENDPOINT || 'http://localhost:3500';
const APP_ID = process.env.APP_ID || 'myapp';

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    appId: APP_ID
  });
});

// Ready check endpoint
app.get('/ready', (req, res) => {
  // Add any readiness checks here
  res.status(200).json({ status: 'ready' });
});

// Metrics endpoint
app.get('/metrics', (req, res) => {
  // In a real app, this would return actual metrics
  res.status(200).json({
    appId: APP_ID,
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    timestamp: new Date().toISOString()
  });
});

// Example API endpoint that uses Dapr service invocation
app.post('/process-order', async (req, res) => {
  try {
    const { orderId, customer, items } = req.body;

    console.log(`Processing order ${orderId} for customer ${customer}`);

    // Example: Save order to state store via Dapr
    const orderData = {
      id: orderId,
      customer,
      items,
      status: 'processing',
      createdAt: new Date().toISOString()
    };

    // Save to Dapr state store
    await saveState(`order_${orderId}`, orderData);

    // Example: Publish order event via Dapr pub/sub
    await publishEvent('orders', {
      eventType: 'OrderCreated',
      orderId,
      customer,
      timestamp: new Date().toISOString()
    });

    res.json({
      success: true,
      orderId,
      message: 'Order processed successfully'
    });
  } catch (error) {
    console.error('Error processing order:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Example endpoint that retrieves order from state
app.get('/order/:orderId', async (req, res) => {
  try {
    const { orderId } = req.params;

    // Get from Dapr state store
    const order = await getState(`order_${orderId}`);

    if (!order) {
      return res.status(404).json({ error: 'Order not found' });
    }

    res.json(order);
  } catch (error) {
    console.error('Error retrieving order:', error);
    res.status(500).json({ error: error.message });
  }
});

// Example endpoint that invokes another service via Dapr
app.post('/invoke-payment', async (req, res) => {
  try {
    const { orderId, amount } = req.body;

    // Invoke payment service via Dapr service invocation
    const response = await invokeService('payment-service', 'process-payment', {
      orderId,
      amount,
      currency: 'USD'
    });

    res.json(response);
  } catch (error) {
    console.error('Error invoking payment service:', error);
    res.status(500).json({ error: error.message });
  }
});

// Dapr Helper Functions
async function saveState(key, value) {
  try {
    const stateItem = {
      key,
      value
    };

    await axios.post(`${DAPR_HTTP_ENDPOINT}/v1.0/state/mystatestore`, [stateItem]);
    console.log(`State saved for key: ${key}`);
  } catch (error) {
    console.error(`Failed to save state for key ${key}:`, error.message);
    throw error;
  }
}

async function getState(key) {
  try {
    const response = await axios.get(`${DAPR_HTTP_ENDPOINT}/v1.0/state/mystatestore/${key}`);
    return response.data;
  } catch (error) {
    if (error.response && error.response.status === 404) {
      return null; // Key not found
    }
    console.error(`Failed to get state for key ${key}:`, error.message);
    throw error;
  }
}

async function publishEvent(topic, data, pubsubName = 'kafka-pubsub') {
  try {
    await axios.post(`${DAPR_HTTP_ENDPOINT}/v1.0/publish/${pubsubName}/${topic}`, data);
    console.log(`Event published to topic: ${topic}`);
  } catch (error) {
    console.error(`Failed to publish event to topic ${topic}:`, error.message);
    throw error;
  }
}

async function invokeService(targetAppId, method, data) {
  try {
    const response = await axios.post(
      `${DAPR_HTTP_ENDPOINT}/v1.0/invoke/${targetAppId}/method/${method}`,
      data
    );
    return response.data;
  } catch (error) {
    console.error(`Service invocation failed:`, error.message);
    throw error;
  }
}

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('Received SIGTERM, shutting down gracefully');
  server.close(() => {
    console.log('Process terminated');
  });
});

process.on('SIGINT', () => {
  console.log('Received SIGINT, shutting down gracefully');
  server.close(() => {
    console.log('Process terminated');
  });
});

// Start server
const server = app.listen(PORT, () => {
  console.log(`App listening on port ${PORT}`);
  console.log(`Dapr endpoint: ${DAPR_HTTP_ENDPOINT}`);
  console.log(`App ID: ${APP_ID}`);
});

module.exports = app;