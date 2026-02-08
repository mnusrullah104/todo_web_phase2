# Docker Containerization Best Practices

## Dockerfile Best Practices

### Multi-stage Builds
```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
USER node
CMD ["npm", "start"]
```

### Base Image Selection
```dockerfile
# Use specific tags instead of 'latest'
FROM node:18.17.0-alpine
# Use minimal base images (alpine, distroless)
FROM golang:1.21-alpine AS builder
```

### Layer Caching Optimization
```dockerfile
# Copy package files first to leverage layer caching
COPY package*.json ./
RUN npm ci

# Copy source code last
COPY . .
```

## Security Best Practices

### Non-root User
```dockerfile
FROM node:18-alpine
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001
USER nextjs
```

### Minimal Permissions
```dockerfile
# Drop all capabilities
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
USER nobody
```

## Resource Management

### Memory and CPU Limits
```dockerfile
# Set resource limits in docker-compose.yml or k8s manifests
# In Dockerfile, optimize for size and startup time
FROM node:18-alpine
RUN npm ci --omit=dev
```

## Health Checks
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
```

## Environment Configuration

### Multi-environment Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
    volumes:
      - ./logs:/app/logs

# docker-compose.override.yml (development)
version: '3.8'
services:
  app:
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    command: npm run dev
```

## Gordon AI Agent Integration

### Gordon Configuration
```json
{
  "gordon": {
    "version": "1.0",
    "build": {
      "strategy": "multi-stage",
      "cache_from": ["myapp:latest"],
      "args": {
        "NODE_ENV": "production"
      }
    },
    "security": {
      "scan": true,
      "allow_failure": false
    },
    "deploy": {
      "target_platforms": ["linux/amd64", "linux/arm64"]
    }
  }
}
```

### Gordon Dockerfile Template
```dockerfile
# This Dockerfile is managed by Gordon AI Agent
FROM node:18-alpine AS base
LABEL maintainer="gordon-ai-agent"

# Install dependencies with security in mind
RUN apk add --no-cache dumb-init curl

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install production dependencies only
RUN npm ci --only=production --audit=false && npm cache clean --force

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copy application code
COPY --chown=nextjs:nodejs . .

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]
CMD ["npm", "start"]

# Add health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js
```

## Optimized Images

### Image Size Reduction
```dockerfile
# Use .dockerignore to exclude unnecessary files
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev --audit=false && npm cache clean --force

FROM node:18-alpine AS production
RUN apk add --no-cache dumb-init
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER node
ENTRYPOINT ["dumb-init", "--"]
CMD ["npm", "start"]
```

### Build Args
```dockerfile
ARG NODE_ENV=production
ARG BUILD_DATE
ARG VERSION

FROM node:18-alpine
LABEL build_date=$BUILD_DATE
LABEL version=$VERSION

ENV NODE_ENV=$NODE_ENV

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=$NODE_ENV
COPY . .
```

## Docker Compose for Development

### Development Services
```yaml
version: '3.8'
services:
  app:
    build:
      context: .
      target: development
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DEBUG=*.*
    depends_on:
      - postgres
      - redis
      - kafka

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  kafka:
    image: confluentinc/cp-kafka:7.4.0
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    ports:
      - "9092:9092"
    depends_on:
      - zookeeper

  zookeeper:
    image: confluentinc/cp-zookeeper:7.4.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

volumes:
  postgres_data:
```

## Docker Build Optimization

### BuildKit Features
```bash
# Use BuildKit for faster builds
DOCKER_BUILDKIT=1 docker build --progress=plain .

# Use cache mounts for npm/yarn
RUN --mount=type=cache,target=/root/.npm npm ci

# Use SSH mount for git
RUN --mount=type=ssh git clone git@github.com:user/repo.git

# Use secret mount for tokens
RUN --mount=type=secret,id=token cat /run/secrets/token
```

### Build Arguments
```dockerfile
# Define build arguments
ARG NODE_VERSION=18-alpine
ARG APP_HOME=/app

FROM node:${NODE_VERSION} AS base
WORKDIR ${APP_HOME}

# Use build args in commands
ARG NODE_ENV=production
RUN npm ci --only=${NODE_ENV}
```

## Docker Security Scanning

### Integration with CI/CD
```bash
# Scan image with Trivy
trivy image myapp:latest

# Scan Dockerfile
trivy config --severity HIGH,CRITICAL .

# Scan for misconfigurations
docker scan myapp:latest
```

## Gordon AI Agent Workflow

### Automated Dockerfile Generation
```bash
# Gordon analyzes your codebase and generates optimized Dockerfile
gordon init --project-type nodejs
gordon build --optimize
gordon scan --security
gordon push --registry docker.io/username/app
```

### Gordon Configuration File
```yaml
# .gordon/config.yaml
version: "1.0"
project:
  name: "myapp"
  type: "nodejs"
  language_version: "18"

build:
  strategy: "multi-stage"
  platforms:
    - "linux/amd64"
    - "linux/arm64"
  cache:
    enabled: true
    from:
      - "myapp:latest"
  args:
    NODE_ENV: "production"

security:
  scan_enabled: true
  severity_threshold: "HIGH"
  allow_failure: false

deployment:
  registry: "docker.io/username"
  tags:
    - "latest"
    - "{{.ShortCommit}}"
    - "{{.Tag}}"
```