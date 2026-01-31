# Dapr Integration Best Practices

## Overview

Dapr (Distributed Application Runtime) is a portable, event-driven runtime that simplifies building resilient, microservice applications. It provides building blocks for common distributed systems patterns.

## Dapr Installation

### Install Dapr CLI
```bash
# Linux/macOS
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash

# Windows (PowerShell)
powershell -Command "Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1'))"
```

### Initialize Dapr on Kubernetes
```bash
# Initialize Dapr on your Kubernetes cluster
dapr init --kubernetes

# Verify installation
dapr status -k

# Check Dapr control plane components
kubectl get pods -n dapr-system
```

## Dapr Building Blocks

### Service Invocation
```yaml
# dapr-components/http.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: my-http-component
spec:
  type: secretstores.kubernetes
  version: v1
  metadata: []
```

### Example Service Code (Node.js)
```javascript
// app.js
const express = require('express');
const app = express();

app.use(express.json());

// Dapr service invocation endpoint
app.post('/invoke/:method', async (req, res) => {
  const { method } = req.params;
  const { data } = req.body;

  console.log(`Invoking method: ${method} with data:`, data);

  // Your business logic here
  const result = await processMethod(method, data);

  res.json({ result });
});

// Dapr input binding endpoint
app.post('/bind/:binding', async (req, res) => {
  const { binding } = req.params;
  const { data } = req.body;

  console.log(`Received data from binding ${binding}:`, data);

  // Process the bound data
  await processData(binding, data);

  res.sendStatus(200);
});

// Dapr pub/sub subscriber
app.post('/orders', async (req, res) => {
  const data = req.body;

  console.log('Order received:', data);

  // Process order
  await processOrder(data);

  res.sendStatus(200);
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`App listening on port ${port}`);
});

async function processMethod(method, data) {
  // Implementation of method processing
  return `Processed ${method} with ${JSON.stringify(data)}`;
}

async function processData(binding, data) {
  // Implementation of data processing
  console.log(`Processing data from ${binding}`);
}

async function processOrder(order) {
  // Implementation of order processing
  console.log(`Processing order: ${order.id}`);
}
```

## Dapr Components

### State Store Configuration
```yaml
# dapr-components/statestore.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: mystatestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    secretKeyRef:
      name: redis-password
      key: password
  - name: actorStateStore
    value: "true"
scopes:
  - myapp
```

### Pub/Sub Configuration (Kafka)
```yaml
# dapr-components/pubsub.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka:9092"
  - name: consumerGroup
    value: "myapp-consumer-group"
  - name: clientID
    value: "myapp"
  - name: authRequired
    value: "false"
scopes:
  - myapp
```

### Secret Store Configuration
```yaml
# dapr-components/secrets.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: my-secret-store
spec:
  type: secretstores.kubernetes
  version: v1
  metadata: []
scopes:
  - myapp
```

### Binding Configuration
```yaml
# dapr-components/input-binding.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: my-input-binding
spec:
  type: bindings.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka:9092"
  - name: topics
    value: "myapp-input-topic"
  - name: consumerGroup
    value: "myapp-binding-consumer"
  - name: authRequired
    value: "false"
scopes:
  - myapp
```

## Dapr Sidecar Configuration

### Deployment with Dapr Annotation
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "myapp"
        dapr.io/app-port: "3000"
        dapr.io/config: "appconfig"
        dapr.io/log-level: "info"
        dapr.io/app-max-concurrency: "10"
        dapr.io/enable-api-logging: "true"
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: "production"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

## Dapr Configuration

### App Configuration
```yaml
# dapr-components/appconfig.yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: appconfig
spec:
  tracing:
    samplingRate: "1"
    zipkin:
      endpointAddress: "http://zipkin.default.svc.cluster.local:9411/api/v2/spans"
  metric:
    enabled: true
  httpPipeline:
    handlers:
    - name: validator
      type: middleware.http.validator
  features:
  - name: AppHealthCheck
    enabled: true
  - name: InputBindingsConcurrency
    enabled: true
```

## Dapr Service Invocation

### Making Service Calls
```javascript
// client.js
const axios = require('axios');

const DAPR_HTTP_ENDPOINT = process.env.DAPR_HTTP_ENDPOINT || 'http://localhost:3500';

async function invokeService(appId, method, data) {
  try {
    const response = await axios.post(
      `${DAPR_HTTP_ENDPOINT}/v1.0/invoke/${appId}/method/${method}`,
      data
    );

    return response.data;
  } catch (error) {
    console.error('Service invocation failed:', error.message);
    throw error;
  }
}

// Example usage
async function example() {
  const result = await invokeService('order-processor', 'processOrder', {
    orderId: '123',
    customer: 'John Doe'
  });

  console.log('Service result:', result);
}
```

## Dapr State Management

### State Operations
```javascript
// state.js
const axios = require('axios');

const DAPR_HTTP_ENDPOINT = process.env.DAPR_HTTP_ENDPOINT || 'http://localhost:3500';

class DaprStateManager {
  constructor(storeName = 'mystatestore') {
    this.storeName = storeName;
    this.endpoint = DAPR_HTTP_ENDPOINT;
  }

  async saveState(key, value, options = {}) {
    try {
      const stateItem = {
        key,
        value,
        ...options
      };

      await axios.post(`${this.endpoint}/v1.0/state/${this.storeName}`, [stateItem]);
      console.log(`State saved for key: ${key}`);
    } catch (error) {
      console.error(`Failed to save state for key ${key}:`, error.message);
      throw error;
    }
  }

  async getState(key) {
    try {
      const response = await axios.get(`${this.endpoint}/v1.0/state/${this.storeName}/${key}`);
      return response.data;
    } catch (error) {
      if (error.response && error.response.status === 404) {
        return null; // Key not found
      }
      console.error(`Failed to get state for key ${key}:`, error.message);
      throw error;
    }
  }

  async deleteState(key, options = {}) {
    try {
      const queryString = new URLSearchParams(options).toString();
      await axios.delete(`${this.endpoint}/v1.0/state/${this.storeName}/${key}?${queryString}`);
      console.log(`State deleted for key: ${key}`);
    } catch (error) {
      console.error(`Failed to delete state for key ${key}:`, error.message);
      throw error;
    }
  }

  async bulkGet(keys) {
    try {
      const response = await axios.post(`${this.endpoint}/v1.0/state/${this.storeName}/bulk`, {
        keys
      });
      return response.data;
    } catch (error) {
      console.error('Bulk get failed:', error.message);
      throw error;
    }
  }
}

// Example usage
async function example() {
  const stateManager = new DaprStateManager();

  // Save state
  await stateManager.saveState('orderId-123', {
    id: '123',
    customer: 'John Doe',
    status: 'processing'
  });

  // Get state
  const order = await stateManager.getState('orderId-123');
  console.log('Retrieved order:', order);

  // Delete state
  await stateManager.deleteState('orderId-123');
}
```

## Dapr Publish/Subscribe

### Publishing Messages
```javascript
// publisher.js
const axios = require('axios');

const DAPR_HTTP_ENDPOINT = process.env.DAPR_HTTP_ENDPOINT || 'http://localhost:3500';

async function publishMessage(topic, data, pubsubName = 'kafka-pubsub') {
  try {
    await axios.post(`${DAPR_HTTP_ENDPOINT}/v1.0/publish/${pubsubName}/${topic}`, data);
    console.log(`Message published to topic: ${topic}`);
  } catch (error) {
    console.error(`Failed to publish message to topic ${topic}:`, error.message);
    throw error;
  }
}

// Example usage
async function example() {
  await publishMessage('orders', {
    id: '123',
    customer: 'John Doe',
    items: ['item1', 'item2']
  });
}
```

### Subscription Handler
```javascript
// subscriber.js
const express = require('express');
const app = express();

app.use(express.json());

// Dapr subscription endpoint
app.post('/orders', async (req, res) => {
  const order = req.body;

  console.log('Order received:', order);

  try {
    // Process the order
    await processOrder(order);

    res.sendStatus(200);
  } catch (error) {
    console.error('Error processing order:', error);
    res.status(500).send('Error processing order');
  }
});

// Dapr subscription routes
app.get('/dapr/subscribe', (req, res) => {
  res.json([
    {
      pubsubname: 'kafka-pubsub',
      topic: 'orders',
      route: '/orders'
    }
  ]);
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Subscriber app listening on port ${port}`);
});

async function processOrder(order) {
  // Process the order
  console.log(`Processing order: ${order.id}`);
  // Add your business logic here
}
```

## Dapr with Kafka

### Kafka Setup for Dapr
```yaml
# kafka-dapr.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kafka-dapr-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kafka-dapr-app
  template:
    metadata:
      labels:
        app: kafka-dapr-app
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "kafka-dapr-app"
        dapr.io/app-port: "3000"
        dapr.io/config: "appconfig"
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 3000
---
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka-service:9092"
  - name: consumerGroup
    value: "kafka-dapr-app-group"
  - name: authRequired
    value: "false"
---
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-binding
spec:
  type: bindings.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka-service:9092"
  - name: topics
    value: "input-topic,output-topic"
  - name: consumerGroup
    value: "kafka-binding-group"
  - name: authRequired
    value: "false"
```

## Dapr Observability

### Distributed Tracing
```yaml
# dapr-components/tracing.yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: appconfig
spec:
  tracing:
    samplingRate: "0.1"
    zipkin:
      endpointAddress: "http://jaeger-collector:9411/api/v2/spans"
```

### Metrics Configuration
```yaml
# dapr-components/metrics.yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: appconfig
spec:
  metric:
    enabled: true
    rules:
    - name: custom_rule
      description: "Custom metric rule"
```

## Dapr Security

### Authentication and Authorization
```yaml
# dapr-components/secure-statestore.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: secure-statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: "redis:6379"
  - name: redisPassword
    secretKeyRef:
      name: "redis-secret"
      key: "password"
  - name: enableTLS
    value: "true"
scopes:
  - myapp
```

### Dapr Sidecar Security
```yaml
# dapr-components/sentry.yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: dapr-config
spec:
  mtls:
    enabled: true
    workloadCertTTL: "24h"
    allowedClockSkew: "15m"
```

## Dapr in Helm Charts

### Dapr Integration in Chart
```yaml
# templates/dapr-components.yaml
{{- if .Values.dapr.enabled }}
{{- range .Values.dapr.components }}
---
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: {{ .name }}
spec:
  type: {{ .type }}
  version: {{ .version }}
  metadata:
  {{- range .metadata }}
  - name: {{ .name }}
    {{- if .value }}
    value: {{ .value | quote }}
    {{- else if .secretKeyRef }}
    secretKeyRef:
      name: {{ .secretKeyRef.name }}
      key: {{ .secretKeyRef.key }}
    {{- end }}
  {{- end }}
{{- if .scopes }}
scopes:
{{- range .scopes }}
  - {{ . }}
{{- end }}
{{- end }}
{{- end }}
{{- end }}
```

### Dapr Configuration in Values
```yaml
# values.yaml with Dapr
dapr:
  enabled: true
  appId: "myapp"
  appPort: 3000
  config: "appconfig"
  components:
    - name: "statestore"
      type: "state.redis"
      version: "v1"
      metadata:
        - name: "redisHost"
          value: "redis:6379"
        - name: "redisPassword"
          secretKeyRef:
            name: "redis-secret"
            key: "password"
      scopes:
        - "myapp"
    - name: "pubsub"
      type: "pubsub.kafka"
      version: "v1"
      metadata:
        - name: "brokers"
          value: "kafka:9092"
        - name: "consumerGroup"
          value: "myapp-group"
      scopes:
        - "myapp"
```

## Dapr Development Workflow

### Local Development
```bash
# Run with Dapr locally
dapr run --app-id myapp --app-port 3000 --dapr-http-port 3500 node app.js

# Run with specific components
dapr run --app-id myapp --app-port 3000 --components-path ./dapr-components node app.js

# Run with debug logging
dapr run --app-id myapp --app-port 3000 --log-level debug node app.js
```

### Debugging Dapr Applications
```bash
# Check Dapr sidecar logs
kubectl logs -l app=myapp -c daprd

# Get Dapr sidecar status
dapr status --kubernetes

# Get configuration
dapr configurations -k

# Get components
dapr components -k
```

## Dapr Best Practices

### Performance Optimization
- Use bulk operations for state management
- Configure appropriate concurrency settings
- Use proper partitioning for pub/sub
- Monitor and tune Dapr sidecar resource usage

### Resilience Patterns
- Implement circuit breaker patterns
- Use retries with exponential backoff
- Configure timeouts appropriately
- Use health checks for service discovery

### Security Considerations
- Enable mTLS for service-to-service communication
- Use secrets management for sensitive data
- Configure proper scopes for components
- Regularly rotate certificates and secrets

### Monitoring and Observability
- Enable distributed tracing
- Collect metrics for performance monitoring
- Set up alerts for Dapr system health
- Monitor application-specific metrics through Dapr