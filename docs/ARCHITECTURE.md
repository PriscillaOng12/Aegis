# Aegis Health - Technical Architecture

> **Scalable, real-time chronic disease management platform built for clinical-grade reliability**

## System Overview

Aegis Health implements a microservices architecture designed for healthcare environments requiring sub-200ms response times, 99.9% uptime, and HIPAA compliance. The system processes multi-modal health data streams to provide real-time risk predictions and automated interventions.

### Design Principles
- **Privacy by Design:** Zero-trust security model with end-to-end encryption
- **Real-time Processing:** Sub-180ms P95 latency for critical health decisions  
- **Clinical Reliability:** 99.9% uptime with graceful degradation
- **Horizontal Scalability:** Auto-scaling to handle 10k+ concurrent users
- **Data Integrity:** ACID compliance with audit logging for healthcare regulations

---

## High-Level Architecture

```mermaid
%%{init: {
  'theme': 'dark',
  'themeVariables': {
    'primaryColor': '#4f46e5',
    'primaryTextColor': '#ffffff',
    'primaryBorderColor': '#6366f1',
    'lineColor': '#94a3b8',
    'secondaryColor': '#1e293b',
    'tertiaryColor': '#334155',
    'background': '#0f172a',
    'mainBkg': '#1e293b',
    'secondBkg': '#334155',
    'tertiaryBkg': '#475569'
  }
}}%%

flowchart TD
    %% Users
    patient["👤 Patient<br/>Chronic disease patient<br/>managing health"]
    clinician["👩‍⚕️ Clinician<br/>Healthcare provider<br/>monitoring patients"]
    
    %% Mobile Layer
    subgraph mobile["📱 Mobile Layer"]
        ios_app["Mobile App<br/>React Native + Expo<br/>• Symptom logging<br/>• Risk monitoring<br/>• Health tracking"]
    end
    
    %% Web Layer
    subgraph web["🌐 Web Layer"]
        dashboard["Clinician Dashboard<br/>Next.js + TypeScript<br/>• Analytics interface<br/>• Intervention management<br/>• Patient overview"]
    end
    
    %% API Gateway Layer
    subgraph api_gateway["🚪 API Gateway Layer"]
        fastapi["API Gateway<br/>FastAPI + Uvicorn<br/>• REST APIs<br/>• WebSocket streams<br/>• Request validation"]
        auth["Auth Service<br/>Auth0 + JWT<br/>• Authentication<br/>• Role-based access<br/>• Token management"]
    end
    
    %% Data Processing Layer
    subgraph processing["⚙️ Data Processing Layer"]
        pubsub["Message Queue<br/>Google Pub/Sub<br/>• Event streaming<br/>• Async processing<br/>• Message routing"]
        beam["ETL Pipeline<br/>Apache Beam<br/>• Real-time processing<br/>• Data transformation<br/>• Stream analytics"]
        scheduler["Job Scheduler<br/>Cloud Scheduler<br/>• Batch jobs<br/>• Model training<br/>• Automated tasks"]
    end
    
    %% ML Platform
    subgraph ml_platform["🤖 ML Platform"]
        training["Model Training<br/>XGBoost + PyTorch<br/>• Feature engineering<br/>• Model training<br/>• Performance tuning"]
        serving["Model Serving<br/>TorchServe + GPU<br/>• Real-time inference<br/>• Model versioning<br/>• Prediction API"]
        explainer["AI Explainability<br/>SHAP + LIME<br/>• Feature attribution<br/>• Model transparency<br/>• Decision insights"]
    end
    
    %% Data Storage Layer
    subgraph storage["💾 Data Storage Layer"]
        postgres["Primary Database<br/>Cloud SQL PostgreSQL<br/>• Transactional data<br/>• ACID compliance<br/>• Data integrity"]
        bigquery["Data Warehouse<br/>BigQuery + dbt<br/>• Analytics store<br/>• Feature store<br/>• Historical data"]
        gcs["Object Storage<br/>Cloud Storage<br/>• Model artifacts<br/>• Raw data files<br/>• Backup storage"]
    end
    
    %% Observability Stack
    subgraph monitoring["📊 Observability Stack"]
        prometheus["Metrics Engine<br/>Prometheus<br/>• System metrics<br/>• Health monitoring<br/>• Performance data"]
        grafana["Visualization<br/>Grafana + Alerts<br/>• Dashboards<br/>• Alerting<br/>• Trend analysis"]
        otel["Tracing System<br/>OpenTelemetry<br/>• Distributed tracing<br/>• Error tracking<br/>• Latency monitoring"]
    end
    
    %% External Systems
    healthkit["🏥 Health Platforms<br/>HealthKit / Google Fit<br/>Wearable integrations"]
    notifications["📲 Push Services<br/>Firebase FCM / APNs<br/>Real-time notifications"]
    
    %% Enhanced Relationships
    patient -->|"Interacts<br/>Touch/Voice input"| ios_app
    clinician -->|"Monitors<br/>Web interface"| dashboard
    
    ios_app -->|"API requests<br/>HTTPS/WSS"| fastapi
    dashboard -->|"Data queries<br/>REST API"| fastapi
    fastapi -->|"Token validation<br/>OIDC/OAuth2"| auth
    
    healthkit -->|"Health data<br/>Webhook/API"| pubsub
    fastapi -->|"Event publishing<br/>gRPC/HTTP"| pubsub
    pubsub -->|"Stream processing<br/>Dataflow"| beam
    
    beam -->|"Feature writes<br/>Streaming API"| bigquery
    beam -->|"Data updates<br/>Connection pool"| postgres
    
    scheduler -->|"Training jobs<br/>Cloud Run"| training
    training -->|"Feature queries<br/>SQL/BigQuery API"| bigquery
    training -->|"Model storage<br/>Cloud Storage API"| gcs
    
    fastapi -->|"Predictions<br/>HTTP/gRPC"| serving
    serving -->|"Explanations<br/>Python API"| explainer
    serving -->|"Model loading<br/>Object storage"| gcs
    
    fastapi -->|"CRUD ops<br/>AsyncPG pool"| postgres
    fastapi -->|"Trace data<br/>OTLP/HTTP"| otel
    otel -->|"Metrics export<br/>Prometheus format"| prometheus
    prometheus -->|"Data queries<br/>PromQL"| grafana
    
    fastapi -->|"Push alerts<br/>REST API"| notifications

    %% Styling
    classDef mobileStyle fill:#3b82f6,stroke:#1e40af,stroke-width:2px,color:#ffffff
    classDef webStyle fill:#059669,stroke:#047857,stroke-width:2px,color:#ffffff
    classDef apiStyle fill:#dc2626,stroke:#b91c1c,stroke-width:2px,color:#ffffff
    classDef processingStyle fill:#7c3aed,stroke:#6d28d9,stroke-width:2px,color:#ffffff
    classDef mlStyle fill:#ea580c,stroke:#c2410c,stroke-width:2px,color:#ffffff
    classDef storageStyle fill:#0891b2,stroke:#0e7490,stroke-width:2px,color:#ffffff
    classDef monitoringStyle fill:#be185d,stroke:#9d174d,stroke-width:2px,color:#ffffff
    classDef externalStyle fill:#475569,stroke:#64748b,stroke-width:2px,color:#ffffff,stroke-dasharray: 5 5
    
    class ios_app mobileStyle
    class dashboard webStyle
    class fastapi,auth apiStyle
    class pubsub,beam,scheduler processingStyle
    class training,serving,explainer mlStyle
    class postgres,bigquery,gcs storageStyle
    class prometheus,grafana,otel monitoringStyle
    class healthkit,notifications externalStyle
```


---

## Data Flow Architecture

### Real-time Event Processing

```mermaid
sequenceDiagram
    participant App as Mobile App
    participant API as FastAPI
    participant Auth as Auth0
    participant DB as PostgreSQL
    participant Queue as Pub/Sub
    participant ETL as Beam Pipeline
    participant ML as ML Service
    participant BQ as BigQuery
    participant Alert as Alert System
    
    Note over App,Alert: Patient logs symptom (Pain: 8/10)
    
    App->>API: POST /v1/symptoms
    API->>Auth: Validate JWT token
    Auth-->>API: Token valid + user claims
    
    API->>DB: INSERT symptom_log
    DB-->>API: Log ID + timestamp
    
    API->>Queue: Publish symptom_event
    Note over Queue: Event: {user_id, pain: 8, timestamp}
    
    par Parallel Processing
        Queue->>ETL: Process symptom event
        ETL->>BQ: Update feature aggregations
        ETL->>ETL: Calculate rolling windows
        
        ETL->>ML: Trigger risk prediction
        Note over ML: Features: [pain_3d_avg, hrv_trend, sleep_efficiency]
        ML->>ML: XGBoost inference + SHAP
        ML-->>ETL: Risk: 0.85 (HIGH)
        
        ETL->>DB: Store risk_score
        ETL->>API: WebSocket risk update
    and
        API->>Alert: Check intervention rules
        Note over Alert: Rule: if risk > 0.8 AND pain > 7
        Alert->>App: Push notification
        Alert->>Queue: Log intervention event
    end
    
    API-->>App: HTTP 201 Created
    Note over App: Real-time risk update via WebSocket
```

### Data Pipeline Layers

```mermaid
graph TD
    subgraph "1. Ingestion Layer"
        A1[Mobile Symptoms]
        A2[Wearable Data]
        A3[Clinical Notes]
        A4[Medication Events]
    end
    
    subgraph "2. Streaming Layer"
        B1[Pub/Sub Topics]
        B2[Dead Letter Queues]
        B3[Stream Processing]
    end
    
    subgraph "3. Processing Layer"
        C1[Data Validation]
        C2[Feature Engineering]
        C3[Aggregation Windows]
        C4[Real-time Scoring]
    end
    
    subgraph "4. Storage Layer"
        D1[Transactional DB]
        D2[Analytics Warehouse]
        D3[Cold Storage]
        D4[Feature Cache]
    end
    
    subgraph "5. Serving Layer"
        E1[REST APIs]
        E2[WebSocket Streams]
        E3[ML Inference]
        E4[Analytics Queries]
    end
    
    A1 --> B1
    A2 --> B1
    A3 --> B1
    A4 --> B1
    
    B1 --> B3
    B2 --> B3
    
    B3 --> C1
    C1 --> C2
    C2 --> C3
    C3 --> C4
    
    C2 --> D1
    C3 --> D2
    C4 --> D4
    B1 --> D3
    
    D1 --> E1
    D2 --> E4
    D4 --> E3
    E3 --> E2
    
    classDef ingestion fill:#E8F4FD,stroke:#1565C0,stroke-width:2px,color:#000000
    classDef streaming fill:#E8F5E8,stroke:#2E7D32,stroke-width:2px,color:#000000
    classDef processing fill:#FFF8E1,stroke:#EF6C00,stroke-width:2px,color:#000000
    classDef storage fill:#F3E5F5,stroke:#6A1B9A,stroke-width:2px,color:#000000
    classDef serving fill:#FFEBEE,stroke:#C62828,stroke-width:2px,color:#000000
    
    class A1,A2,A3,A4 ingestion
    class B1,B2,B3 streaming
    class C1,C2,C3,C4 processing
    class D1,D2,D3,D4 storage
    class E1,E2,E3,E4 serving
```

---

## Machine Learning Pipeline

### Training Pipeline

```mermaid
flowchart TD
    subgraph "1. Data Preparation"
        A1[BigQuery Source] --> A2[Feature Selection]
        A2 --> A3[Data Validation]
        A3 --> A4[Train/Val Split]
    end
    
    subgraph "2. Feature Engineering"
        B1[Rolling Aggregations<br/>3d, 7d, 14d windows]
        B2[Trend Features<br/>Slope, momentum]
        B3[Categorical Encoding<br/>Target encoding]
        B4[Interaction Features<br/>Pain × Sleep efficiency]
    end
    
    subgraph "3. Model Training"
        C1[XGBoost Training]
        C2[Hyperparameter Tuning<br/>Optuna optimization]
        C3[Cross-validation<br/>Time series split]
        C4[Calibration<br/>Platt scaling]
    end
    
    subgraph "4. Model Evaluation"
        D1[Performance Metrics<br/>AUROC, AUPRC, ECE]
        D2[Clinical Validation<br/>Physician review]
        D3[Fairness Testing<br/>Demographic parity]
        D4[Feature Importance<br/>SHAP analysis]
    end
    
    subgraph "5. Model Deployment"
        E1[Model Packaging<br/>TorchServe MAR]
        E2[Shadow Testing<br/>3-week validation]
        E3[Gradual Rollout<br/>10% → 50% → 100%]
        E4[Monitoring<br/>Drift detection]
    end
    
    A4 --> B1
    A4 --> B2
    A4 --> B3
    A4 --> B4
    
    B1 --> C1
    B2 --> C1
    B3 --> C1
    B4 --> C1
    
    C1 --> C2
    C2 --> C3
    C3 --> C4
    
    C4 --> D1
    D1 --> D2
    D2 --> D3
    D3 --> D4
    
    D4 --> E1
    E1 --> E2
    E2 --> E3
    E3 --> E4
    
    classDef data fill:#E8F4FD,stroke:#1565C0,stroke-width:2px,color:#000000
    classDef feature fill:#E8F5E8,stroke:#2E7D32,stroke-width:2px,color:#000000
    classDef training fill:#FFF8E1,stroke:#EF6C00,stroke-width:2px,color:#000000
    classDef evaluation fill:#F3E5F5,stroke:#6A1B9A,stroke-width:2px,color:#000000
    classDef deployment fill:#FFEBEE,stroke:#C62828,stroke-width:2px,color:#000000
    
    class A1,A2,A3,A4 data
    class B1,B2,B3,B4 feature
    class C1,C2,C3,C4 training
    class D1,D2,D3,D4 evaluation
    class E1,E2,E3,E4 deployment
```

### Feature Engineering Pipeline

| Feature Category | Examples | Window | Update Frequency |
|------------------|----------|--------|------------------|
| **Symptom Trends** | Pain slope (7d), Fatigue volatility | 3d, 7d, 14d | Real-time |
| **Wearable Vitals** | HRV RMSSD, HR variability, Sleep efficiency | 1d, 3d, 7d | Every 15min |
| **Behavioral Patterns** | Step count trends, Sleep regularity | 7d, 30d | Daily |
| **Temporal Features** | Day of week, Hour of day, Season | - | Static |
| **Interaction Features** | Pain × Sleep, HRV × Stress score | 3d | Real-time |

---

## Security Architecture

### Zero-Trust Security Model

```mermaid
graph TB
    subgraph "Client Layer"
        A1[Mobile App<br/>Certificate Pinning]
        A2[Web Dashboard<br/>CSP Headers]
    end
    
    subgraph "API Gateway"
        B1[WAF<br/>DDoS Protection]
        B2[Auth0<br/>JWT + RBAC]
        B3[Rate Limiting<br/>100 req/min per user]
    end
    
    subgraph "Application Layer"
        C1[FastAPI<br/>Input validation]
        C2[Encryption<br/>AES-256-GCM]
        C3[Audit Logging<br/>All data access]
    end
    
    subgraph "Data Layer"
        D1[PostgreSQL<br/>Encryption at rest]
        D2[Secret Manager<br/>Key rotation]
        D3[BigQuery<br/>Column-level security]
    end
    
    subgraph "Network Layer"
        E1[VPC<br/>Private networking]
        E2[Firewall Rules<br/>Principle of least privilege]
        E3[TLS 1.3<br/>All communications]
    end
    
    A1 --> B1
    A2 --> B1
    B1 --> B2
    B2 --> B3
    B3 --> C1
    C1 --> C2
    C2 --> C3
    C3 --> D1
    C3 --> D2
    C3 --> D3
    
    D1 -.-> E1
    D2 -.-> E1
    D3 -.-> E1
    E1 --> E2
    E2 --> E3
    
    classDef client fill:#E8F4FD,stroke:#1565C0,stroke-width:2px,color:#000000
    classDef gateway fill:#E8F5E8,stroke:#2E7D32,stroke-width:2px,color:#000000
    classDef app fill:#FFF8E1,stroke:#EF6C00,stroke-width:2px,color:#000000
    classDef data fill:#F3E5F5,stroke:#6A1B9A,stroke-width:2px,color:#000000
    classDef network fill:#FFEBEE,stroke:#C62828,stroke-width:2px,color:#000000
    
    class A1,A2 client
    class B1,B2,B3 gateway
    class C1,C2,C3 app
    class D1,D2,D3 data
    class E1,E2,E3 network
```

### HIPAA Compliance Controls

| Control | Implementation | Audit Frequency |
|---------|----------------|-----------------|
| **Access Control** | RBAC with Auth0, MFA required | Quarterly |
| **Audit Logs** | All data access logged to BigQuery | Real-time |
| **Encryption** | AES-256 at rest, TLS 1.3 in transit | Annual review |
| **Data Minimization** | Only collect necessary PHI | Monthly review |
| **Breach Detection** | Anomaly detection, automated alerts | Continuous |
| **Business Associate** | Auth0, GCP BAAs in place | Annual renewal |

---

## Performance & Scaling

### Load Testing Results

```mermaid
xychart-beta
    title "API Performance Under Load"
    x-axis [10, 25, 50, 100, 200, 500]
    y-axis "Response Time (ms)" 0 --> 500
    line [45, 62, 89, 142, 178, 234]
```

| Metric | Current | Target | Peak Load |
|--------|---------|--------|-----------|
| **P95 Latency** | 178ms | <200ms | 234ms @ 500 RPS |
| **Throughput** | 25 RPS | 100 RPS | 500 RPS sustained |
| **Error Rate** | 0.02% | <0.1% | 0.05% @ peak |
| **Availability** | 99.94% | 99.9% | 4h downtime/month |

### Auto-scaling Configuration

```yaml
# Cloud Run Auto-scaling
api_service:
  min_instances: 2
  max_instances: 100
  cpu_threshold: 70%
  memory_threshold: 80%
  request_timeout: 300s
  
ml_service:
  min_instances: 1
  max_instances: 20
  cpu_threshold: 80%
  concurrent_requests: 10
  
postgres:
  connection_pool: 20
  max_overflow: 30
  pool_timeout: 30s
```

---

## Database Schema Design

### Core Entity Relationships

```mermaid
erDiagram
    User ||--o{ SymptomLog : logs
    User ||--o{ WearableSnapshot : generates
    User ||--o{ RiskScore : has
    User ||--o{ Intervention : receives
    User ||--|| AuthIdentity : authenticated_by
    
    User {
        string id PK
        string tenant_id
        timestamp created_at
    }
    
    SymptomLog {
        string id PK
        string user_id FK
        integer pain
        integer fatigue
        integer nausea
        string notes
        timestamp timestamp
        timestamp created_at
        boolean consent
    }
    
    WearableSnapshot {
        string id PK
        string user_id FK
        string source
        timestamp timestamp
        float hr
        float hrv
        float steps
        float sleep
        timestamp created_at
        boolean consent
    }
    
    RiskScore {
        string id PK
        string user_id FK
        float risk_percentage
        string top_drivers
        float lead_time_hours
        timestamp created_at
    }
    
    Intervention {
        string id PK
        string user_id FK
        string template_id
        timestamp scheduled_for
        timestamp sent_at
        timestamp created_at
    }
    
    AuthIdentity {
        string id PK
        string user_id FK
        string provider
        string subject
    }
```

### BigQuery Feature Store Schema

```sql
-- Feature table optimized for ML training
CREATE TABLE `aegis.features` (
  user_id STRING NOT NULL,
  day DATE NOT NULL,
  
  -- Symptom features
  pain INTEGER,
  fatigue INTEGER, 
  nausea INTEGER,
  
  -- Wearable features (rolling windows)
  hr_mean_1d FLOAT64,
  hr_std_3d FLOAT64,
  hrv_rmssd_mean_3d FLOAT64,
  hrv_trend_7d FLOAT64,
  sleep_efficiency_mean_7d FLOAT64,
  steps_sum_1d FLOAT64,
  steps_trend_7d FLOAT64,
  
  -- Derived features
  pain_fatigue_interaction FLOAT64,
  stress_composite_score FLOAT64,
  circadian_misalignment FLOAT64,
  
  -- Target variable (next 48h flare)
  label INTEGER,
  
  -- Metadata
  feature_version STRING,
  computed_at TIMESTAMP
)
PARTITION BY day
CLUSTER BY user_id;
```

---

## Event-Driven Architecture

### Message Schema & Topics

```json
{
  "symptom_logged": {
    "schema": {
      "user_id": "string",
      "symptom_log_id": "string", 
      "pain": "integer",
      "fatigue": "integer",
      "nausea": "integer",
      "timestamp": "ISO8601",
      "metadata": {
        "app_version": "string",
        "device_type": "string"
      }
    },
    "topic": "aegis-symptoms",
    "retention": "7 days"
  },
  
  "wearable_synced": {
    "schema": {
      "user_id": "string",
      "source": "string",
      "snapshots": [
        {
          "timestamp": "ISO8601",
          "hr": "float",
          "hrv": "float", 
          "steps": "float",
          "sleep": "float"
        }
      ]
    },
    "topic": "aegis-wearables",
    "retention": "30 days"
  },
  
  "risk_scored": {
    "schema": {
      "user_id": "string",
      "risk_score_id": "string",
      "risk_percentage": "float",
      "top_drivers": [
        {
          "feature": "string",
          "impact": "float"
        }
      ],
      "model_version": "string",
      "computed_at": "ISO8601"
    },
    "topic": "aegis-risk-scores",
    "retention": "90 days"
  }
}
```

### Event Processing Pipeline

```mermaid
graph LR
    subgraph "Event Sources"
        A1[Mobile App]
        A2[Wearables]
        A3[Clinical Systems]
    end
    
    subgraph "Event Streaming"
        B1[Pub/Sub<br/>aegis-symptoms]
        B2[Pub/Sub<br/>aegis-wearables]
        B3[Pub/Sub<br/>aegis-clinical]
    end
    
    subgraph "Stream Processing"
        C1[Real-time ETL<br/>Apache Beam]
        C2[Feature Computation<br/>Rolling aggregations]
        C3[ML Inference<br/>Risk scoring]
    end
    
    subgraph "Event Sinks"
        D1[PostgreSQL<br/>Transactional]
        D2[BigQuery<br/>Analytics]
        D3[Monitoring<br/>Metrics]
        D4[Alerting<br/>Notifications]
    end
    
    A1 --> B1
    A2 --> B2
    A3 --> B3
    
    B1 --> C1
    B2 --> C1
    B3 --> C1
    
    C1 --> C2
    C2 --> C3
    
    C1 --> D1
    C2 --> D2
    C3 --> D3
    C3 --> D4
    
    classDef source fill:#E8F4FD,stroke:#1565C0,stroke-width:2px,color:#000000
    classDef streaming fill:#E8F5E8,stroke:#2E7D32,stroke-width:2px,color:#000000
    classDef processing fill:#FFF8E1,stroke:#EF6C00,stroke-width:2px,color:#000000
    classDef sink fill:#F3E5F5,stroke:#6A1B9A,stroke-width:2px,color:#000000
    
    class A1,A2,A3 source
    class B1,B2,B3 streaming
    class C1,C2,C3 processing
    class D1,D2,D3,D4 sink
```

---

## Deployment Architecture

### Google Cloud Platform Setup

```mermaid
graph TB
    subgraph "Production Environment"
        subgraph "Compute"
            A1[Cloud Run<br/>API Service]
            A2[Cloud Run<br/>ML Service]
            A3[Cloud Functions<br/>ETL Triggers]
        end
        
        subgraph "Data Services"
            B1[Cloud SQL<br/>PostgreSQL 14]
            B2[BigQuery<br/>Data Warehouse]
            B3[Cloud Storage<br/>Model Artifacts]
        end
        
        subgraph "Messaging"
            C1[Pub/Sub<br/>Event Streaming]
            C2[Dataflow<br/>Stream Processing]
            C3[Cloud Scheduler<br/>Batch Jobs]
        end
        
        subgraph "Security"
            D1[IAM<br/>Service Accounts]
            D2[Secret Manager<br/>API Keys]
            D3[VPC<br/>Private Network]
        end
        
        subgraph "Monitoring"
            E1[Cloud Monitoring<br/>Metrics & Alerts]
            E2[Cloud Logging<br/>Centralized Logs]
            E3[Cloud Trace<br/>Distributed Tracing]
        end
    end
    
    subgraph "External Services"
        F1[Auth0<br/>Authentication]
        F2[Firebase<br/>Push Notifications]
        F3[SendGrid<br/>Email Service]
    end
    
    A1 --> B1
    A2 --> B3
    A3 --> C2
    
    C1 --> C2
    C2 --> B2
    C3 --> A3
    
    A1 --> D1
    A2 --> D2
    A1 --> D3
    
    A1 --> E1
    A2 --> E2
    C2 --> E3
    
    A1 --> F1
    A1 --> F2
    A3 --> F3
    
    classDef compute fill:#4285F4,color:#ffffff,stroke:#1976D2,stroke-width:2px
    classDef data fill:#34A853,color:#ffffff,stroke:#2E7D32,stroke-width:2px
    classDef messaging fill:#FBBC04,color:#000000,stroke:#F57C00,stroke-width:2px
    classDef security fill:#EA4335,color:#ffffff,stroke:#C62828,stroke-width:2px
    classDef monitoring fill:#9C27B0,color:#ffffff,stroke:#6A1B9A,stroke-width:2px
    classDef external fill:#607D8B,color:#ffffff,stroke:#37474F,stroke-width:2px
    
    class A1,A2,A3 compute
    class B1,B2,B3 data
    class C1,C2,C3 messaging
    class D1,D2,D3 security
    class E1,E2,E3 monitoring
    class F1,F2,F3 external
```

### CI/CD Pipeline

```mermaid
flowchart LR
    subgraph "Development"
        A1[Developer Push]
        A2[GitHub PR]
        A3[Code Review]
    end
    
    subgraph "CI Pipeline"
        B1[Unit Tests<br/>pytest, Jest]
        B2[Lint & Format<br/>ESLint, Black]
        B3[Security Scan<br/>Bandit, Semgrep]
        B4[Build Images<br/>Docker Build]
    end
    
    subgraph "CD Pipeline"
        C1[Deploy Staging<br/>Cloud Run]
        C2[Integration Tests<br/>API Testing]
        C3[Performance Tests<br/>K6 Load Testing]
        C4[Manual QA<br/>Smoke Tests]
    end
    
    subgraph "Production"
        D1[Blue-Green Deploy<br/>Zero Downtime]
        D2[Health Checks<br/>Readiness Probes]
        D3[Rollback Ready<br/>Previous Version]
    end
    
    A1 --> A2
    A2 --> A3
    A3 --> B1
    
    B1 --> B2
    B2 --> B3
    B3 --> B4
    
    B4 --> C1
    C1 --> C2
    C2 --> C3
    C3 --> C4
    
    C4 --> D1
    D1 --> D2
    D2 --> D3
    
    classDef dev fill:#E8F4FD,stroke:#1565C0,stroke-width:2px,color:#000000
    classDef ci fill:#E8F5E8,stroke:#2E7D32,stroke-width:2px,color:#000000
    classDef cd fill:#FFF8E1,stroke:#EF6C00,stroke-width:2px,color:#000000
    classDef prod fill:#FFEBEE,stroke:#C62828,stroke-width:2px,color:#000000
    
    class A1,A2,A3 dev
    class B1,B2,B3,B4 ci
    class C1,C2,C3,C4 cd
    class D1,D2,D3 prod
```

---

## Technical Metrics & SLAs

### Service Level Objectives

| Service | Availability | Latency (P95) | Error Rate | Recovery Time |
|---------|-------------|---------------|------------|---------------|
| **API Gateway** | 99.9% | <200ms | <0.1% | <5min |
| **ML Inference** | 99.5% | <500ms | <0.5% | <10min |
| **Data Pipeline** | 99.0% | <30s (batch) | <1.0% | <30min |
| **Mobile App** | 99.9% | <3s (startup) | <0.1% | Client-side |

### Resource Utilization

```mermaid
xychart-beta
    title "Resource Utilization (Average)"
    x-axis [API, ML, Database, ETL]
    y-axis "Utilization %" 0 --> 100
    bar [45, 62, 35, 78]
```

### Cost Optimization

| Component | Monthly Cost | Optimization Strategy |
|-----------|-------------|----------------------|
| **Cloud Run (API)** | $245 | Auto-scaling, request-based billing |
| **Cloud SQL** | $156 | Connection pooling, read replicas |
| **BigQuery** | $89 | Partitioning, clustering, slot management |
| **Pub/Sub** | $67 | Message batching, retention policies |
| **Cloud Storage** | $23 | Lifecycle policies, compression |
| **Total** | **$580** | 67% reduction from initial architecture |

---

## Future Architecture Considerations

### Scalability Roadmap

1. **Horizontal Scaling (Q1 2025)**
   - Multi-region deployment (US East/West)
   - Database sharding by tenant_id
   - CDN for static assets

2. **Advanced ML Pipeline (Q2 2025)**
   - Real-time feature stores (Feast)
   - A/B testing framework for models
   - Federated learning for privacy

3. **Edge Computing (Q3 2025)**
   - On-device inference for critical predictions
   - Edge data preprocessing
   - Offline-first mobile architecture

4. **Microservices Evolution (Q4 2025)**
   - Service mesh (Istio) implementation
   - Event sourcing pattern
   - CQRS for read/write separation

### Technology Migrations

| Current | Future | Timeline | Reason |
|---------|--------|----------|--------|
| XGBoost | Temporal Fusion Transformer | Q2 2025 | Better temporal modeling |
| PostgreSQL | CockroachDB | Q3 2025 | Global distribution |
| Pub/Sub | Apache Kafka | Q4 2025 | Streaming analytics |
| Cloud Run | GKE Autopilot | Q1 2026 | Advanced orchestration |

---

This architecture has been battle-tested with **115 real patients** over **10 weeks**, achieving **sub-180ms P95 latency** at **25 RPS** with **99.94% uptime**. The design prioritizes clinical reliability, patient privacy, and horizontal scalability to support the next phase of growth.
