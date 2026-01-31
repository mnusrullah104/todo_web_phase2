# Kubernetes Deployment Best Practices

## Cluster Setup

### Minikube Local Development
```bash
# Start Minikube with specific configuration
minikube start --driver=docker --cpus=4 --memory=8192 --disk-size=40g

# Enable addons
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable dashboard

# Access dashboard
minikube dashboard
```

### DOKS (DigitalOcean Kubernetes) Setup
```bash
# Authenticate with DigitalOcean
doctl auth init

# Create DOKS cluster
doctl kubernetes cluster create my-cluster \
  --region nyc1 \
  --node-pool "name=default-node-pool;size=s-2vcpu-2gb;count=3"

# Get cluster credentials
doctl kubernetes cluster kubeconfig save my-cluster

# Verify connection
kubectl cluster-info
```

## Kubernetes Resources

### Deployment Manifest
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
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Service Manifest
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
  type: LoadBalancer  # For external access
```

### Ingress Controller
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

## kubectl-ai and kagent Integration

### kubectl-ai Usage
```bash
# Describe resources in plain English
kubectl-ai "describe the pods in the default namespace"

# Generate Kubernetes manifests
kubectl-ai "create a deployment for a Node.js app with 3 replicas"

# Troubleshoot issues
kubectl-ai "why are my pods crashing?"

# Get resource recommendations
kubectl-ai "suggest resource limits for this application"
```

### kagent Configuration
```yaml
# .kagent/config.yaml
version: "1.0"
cluster:
  name: "my-cluster"
  provider: "doks"  # or "minikube"
  region: "nyc1"

resources:
  default_limits:
    memory: "512Mi"
    cpu: "500m"
  default_requests:
    memory: "256Mi"
    cpu: "250m"

monitoring:
  enabled: true
  service_mesh: "dapr"

secrets:
  provider: "kubernetes"
  encryption: true
```

### kagent Commands
```bash
# Initialize kagent for a project
kagent init --provider doks

# Deploy application with AI-assisted configuration
kagent deploy --app myapp --image myapp:latest

# Scale application based on load
kagent scale --app myapp --replicas 5

# Update application with zero-downtime
kagent update --app myapp --image myapp:v2

# Rollback to previous version
kagent rollback --app myapp
```

## Namespace Management
```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: myapp-prod
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: myapp-prod
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
---
apiVersion: v1
kind: LimitRange
metadata:
  name: mem-limit-range
  namespace: myapp-prod
spec:
  limits:
  - default:
      memory: 512Mi
      cpu: 500m
    defaultRequest:
      memory: 256Mi
      cpu: 250m
    type: Container
```

## ConfigMaps and Secrets
```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  DATABASE_HOST: "postgres-service"
  LOG_LEVEL: "info"
---
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
type: Opaque
data:
  # All values must be base64 encoded
  DATABASE_PASSWORD: cGFzc3dvcmQ=  # "password" in base64
```

### Using ConfigMaps and Secrets in Pods
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  containers:
  - name: myapp
    image: myapp:latest
    envFrom:
    - configMapRef:
        name: myapp-config
    - secretRef:
        name: myapp-secrets
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
  volumes:
  - name: config-volume
    configMap:
      name: myapp-config
```

## Horizontal Pod Autoscaler (HPA)
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## Service Accounts and RBAC
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
subjects:
- kind: ServiceAccount
  name: myapp-sa
  namespace: default
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

## Monitoring and Logging

### Prometheus Metrics
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-metrics
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "3000"
    prometheus.io/path: "/metrics"
spec:
  selector:
    app: myapp
  ports:
  - port: 3000
    targetPort: 3000
```

### Log Collection
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluent-bit
spec:
  selector:
    matchLabels:
      name: fluent-bit
  template:
    metadata:
      labels:
        name: fluent-bit
    spec:
      containers:
      - name: fluent-bit
        image: fluent/fluent-bit:latest
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

## Network Policies
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: myapp-netpol
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 3000
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: TCP
      port: 53
```

## Storage Configuration
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myapp-storage
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-with-storage
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        volumeMounts:
        - name: app-storage
          mountPath: /app/data
        volumes:
        - name: app-storage
          persistentVolumeClaim:
            claimName: myapp-storage
```

## Deployment Strategies

### Rolling Updates
```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
```

### Blue-Green Deployment
```yaml
# blue deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
      - name: myapp
        image: myapp:blue

---
# green deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
spec:
  replicas: 0  # Initially 0, will be scaled up
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
      - name: myapp
        image: myapp:green
```

## kubectl-ai Advanced Usage

### Resource Generation
```bash
# Generate a complete deployment with service and ingress
kubectl-ai "generate a complete deployment for a Node.js app with Redis and PostgreSQL, including service, ingress, and HPA"

# Create monitoring stack
kubectl-ai "create a monitoring stack with Prometheus, Grafana, and alert manager"

# Set up CI/CD pipeline
kubectl-ai "configure ArgoCD for GitOps deployment of myapp from GitHub"
```

### Troubleshooting
```bash
# Debug pod issues
kubectl-ai "analyze why pods in namespace production are restarting frequently"

# Resource optimization
kubectl-ai "recommend resource limits based on actual usage of myapp deployment"

# Network connectivity
kubectl-ai "diagnose why myapp cannot connect to database service"
```