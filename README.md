# Aegis Health: AI-Powered Chronic Condition Management Platform

> **Preventing chronic disease flare-ups through predictive AI and personalized interventions**

## **Impact & Results**

**Real-world deployment with 115 patients over 10 weeks:**
- **58% Weekly Active Users** with strong retention (D7: 72%, D30: 51%)
- **9.3k AI-timed interventions** delivered with 41% tap-through rate
- **63% clinician acknowledgment** of risk alerts within 24 hours
- **48-hour flare prediction** with AUROC 0.81 and calibration error 2.9%

---

## **Technology Stack**

### **Backend & API**
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat-square&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-323232?style=flat-square&logo=python&logoColor=white)
![Auth0](https://img.shields.io/badge/Auth0-EB5424?style=flat-square&logo=auth0&logoColor=white)

### **Machine Learning & Data**
![XGBoost](https://img.shields.io/badge/XGBoost-FF6600?style=flat-square&logo=xgboost&logoColor=white)
![TorchServe](https://img.shields.io/badge/TorchServe-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)
![Apache Beam](https://img.shields.io/badge/Apache_Beam-00C2FF?style=flat-square&logo=apache&logoColor=white)
![BigQuery](https://img.shields.io/badge/BigQuery-4285F4?style=flat-square&logo=google-cloud&logoColor=white)
![SHAP](https://img.shields.io/badge/SHAP-FF6B6B?style=flat-square&logo=python&logoColor=white)

### **Frontend & Mobile**
![React Native](https://img.shields.io/badge/React_Native-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat-square&logo=typescript&logoColor=white)
![Expo](https://img.shields.io/badge/Expo-000020?style=flat-square&logo=expo&logoColor=white)

### **Infrastructure & DevOps**
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=flat-square&logo=google-cloud&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-623CE4?style=flat-square&logo=terraform&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=flat-square&logo=docker&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white)

### **Testing & Quality**
![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)
![Jest](https://img.shields.io/badge/Jest-C21325?style=flat-square&logo=jest&logoColor=white)
![K6](https://img.shields.io/badge/K6-7D64FF?style=flat-square&logo=k6&logoColor=white)
![ESLint](https://img.shields.io/badge/ESLint-4B32C3?style=flat-square&logo=eslint&logoColor=white)

---

## **System Architecture**

```mermaid
graph TB
    %% Patient Layer
    subgraph "Patient Interface"
        Mobile[React Native App<br/>Symptom Logging, Risk View]
        Wearables[Wearable Devices<br/>HealthKit, Google Fit]
    end
    
    %% Clinician Layer  
    subgraph "Clinician Interface"
        Dashboard[Next.js Dashboard<br/>Analytics, Interventions]
    end
    
    %% API Gateway
    subgraph "API Layer"
        FastAPI[FastAPI Server<br/>Auth, CRUD, WebSockets]
        Auth0[Auth0<br/>JWT, RBAC]
    end
    
    %% Data Processing
    subgraph "Data Pipeline"
        PubSub[Pub/Sub<br/>Real-time Ingestion]
        Beam[Apache Beam<br/>ETL, Feature Engineering]
        BigQuery[BigQuery<br/>Data Warehouse]
    end
    
    %% ML Pipeline
    subgraph "ML Platform"
        Training[XGBoost Training<br/>Feature Engineering]
        Serving[TorchServe<br/>Risk Prediction API]
        SHAP[SHAP Explainer<br/>Feature Attribution]
    end
    
    %% Storage
    subgraph "Data Storage"
        PostgreSQL[Cloud SQL<br/>Transactional Data]
        GCS[Cloud Storage<br/>Raw Data Archive]
    end
    
    %% Monitoring
    subgraph "Observability"
        Prometheus[Prometheus<br/>Metrics Collection]
        Grafana[Grafana<br/>Dashboards, Alerts]
        OpenTel[OpenTelemetry<br/>Distributed Tracing]
    end
    
    %% Connections
    Mobile --> FastAPI
    Wearables --> PubSub
    Dashboard --> FastAPI
    FastAPI --> Auth0
    FastAPI --> PostgreSQL
    FastAPI --> Serving
    
    PubSub --> Beam
    Beam --> BigQuery
    Beam --> GCS
    BigQuery --> Training
    Training --> Serving
    Serving --> SHAP
    
    FastAPI --> OpenTel
    OpenTel --> Prometheus
    Prometheus --> Grafana
    
    %% Styling with better contrast
    classDef interface fill:#E8F4FD,stroke:#1565C0,stroke-width:2px,color:#000000
    classDef api fill:#E8F5E8,stroke:#2E7D32,stroke-width:2px,color:#000000
    classDef data fill:#FFF8E1,stroke:#EF6C00,stroke-width:2px,color:#000000
    classDef ml fill:#F3E5F5,stroke:#6A1B9A,stroke-width:2px,color:#000000
    classDef storage fill:#FFEBEE,stroke:#C62828,stroke-width:2px,color:#000000
    classDef monitoring fill:#E0F2F1,stroke:#00695C,stroke-width:2px,color:#000000
    
    class Mobile,Wearables,Dashboard interface
    class FastAPI,Auth0 api
    class PubSub,Beam,BigQuery data
    class Training,Serving,SHAP ml
    class PostgreSQL,GCS storage
    class Prometheus,Grafana,OpenTel monitoring
```

## 🎯 **Problem Statement**

Chronic diseases affect **133M Americans**, with unpredictable flare-ups leading to:
- **$3.8T annual healthcare costs** (CDC, 2023)
- **Emergency interventions** costing 10x more than preventive care
- **Poor patient outcomes** due to reactive treatment approaches

**Our Solution:** AI-powered predictive platform that identifies flare-up risk 48 hours in advance, enabling proactive interventions and improved patient outcomes.

---

## 🔬 **ML-Driven Risk Prediction**

### **Temporal Fusion Transformer Architecture**
```mermaid
graph LR
    subgraph "Input Features"
        Symptoms[Symptom Scores<br/>Pain, Fatigue, Nausea]
        Wearables[Wearable Data<br/>HRV, HR, Sleep, Steps]
        Context[Temporal Context<br/>Time of day, Day of week]
    end
    
    subgraph "Feature Engineering"
        Rolling[Rolling Windows<br/>3d, 7d, 14d aggregations]
        Embeddings[Categorical Embeddings<br/>User, Time features]
    end
    
    subgraph "XGBoost Model"
        VSN[Variable Selection<br/>Feature Importance]
        Attention[Feature Interactions<br/>Temporal Dependencies]
        Gates[Decision Trees<br/>Ensemble Learning]
    end
    
    subgraph "Output"
        Risk[Risk Score<br/>Calibrated Probability]
        SHAP_OUT[SHAP Values<br/>Top 3 Drivers]
        LeadTime[Lead Time<br/>Hours to Flare]
    end
    
    Symptoms --> Rolling
    Wearables --> Rolling
    Context --> Embeddings
    Rolling --> VSN
    Embeddings --> VSN
    VSN --> Attention
    Attention --> Gates
    Gates --> Risk
    Gates --> SHAP_OUT
    Gates --> LeadTime
    
    classDef input fill:#E8F4FD,stroke:#1565C0,stroke-width:2px,color:#000000
    classDef processing fill:#E8F5E8,stroke:#2E7D32,stroke-width:2px,color:#000000
    classDef model fill:#F3E5F5,stroke:#6A1B9A,stroke-width:2px,color:#000000
    classDef output fill:#FFEBEE,stroke:#C62828,stroke-width:2px,color:#000000
    
    class Symptoms,Wearables,Context input
    class Rolling,Embeddings processing
    class VSN,Attention,Gates model
    class Risk,SHAP_OUT,LeadTime output
```

### **Model Performance**
| Metric | Value | Benchmark |
|--------|-------|-----------|
| **AUROC** | 0.81 | >0.75 (Clinical Standard) |
| **AUPRC** | 0.73 | >0.65 (Imbalanced Data) |
| **Calibration Error** | 2.9% | <5% (Reliability) |
| **Precision @ 10% Recall** | 89% | >80% (Alert Precision) |

---

## 📊 **Data Flow & Real-time Processing**

```mermaid
sequenceDiagram
    participant Patient as Patient App
    participant Wearable as Wearable Device
    participant API as FastAPI Server
    participant PubSub as Pub/Sub Queue
    participant ML as ML Service
    participant Clinician as Clinician Dashboard
    
    Patient->>API: Log symptoms (pain: 7)
    API->>PubSub: Publish symptom event
    Wearable->>PubSub: Stream HRV data (low)
    
    Note over PubSub: Real-time feature aggregation
    PubSub->>ML: Trigger risk prediction
    ML->>ML: Process features + ML inference
    ML-->>API: Risk: 0.78 (HIGH)
    
    Note over API: Risk threshold exceeded
    API->>Clinician: Send alert notification
    API->>Patient: Trigger intervention
    
    Clinician->>API: Acknowledge alert
    Patient->>API: Confirm intervention received
    
    Note over API: Update engagement metrics
```
---

## **Quick Start**

### **Prerequisites**
- Docker & Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.11+ (for ML training)
- Google Cloud SDK (for deployment)

### **Local Development**
```bash
# Clone and setup
git clone https://github.com/yourusername/aegis-health.git
cd aegis-health

# Start backend services
docker-compose up -d postgres redis
cd api && pip install -r requirements.txt
uvicorn app.main:app --reload

# Start mobile app
cd frontend-mobile && npm install
expo start

# Start web dashboard
cd frontend-web && npm install
npm run dev

# Seed demo data
python scripts/seed_data.py
```

### **Production Deployment**
```bash
# Deploy to GCP
cd infra
terraform init
terraform plan -var="project=your-gcp-project"
terraform apply

# Deploy ML model
cd ml/serving
docker build -t gcr.io/your-project/aegis-ml .
docker push gcr.io/your-project/aegis-ml
```

---

## **Product Metrics & KPIs**

### **User Engagement**
```mermaid
xychart-beta
    title "Weekly Active Users (8-week period)"
    x-axis [Week1, Week2, Week3, Week4, Week5, Week6, Week7, Week8]
    y-axis "WAU %" 0 --> 100
    bar [42, 51, 58, 56, 59, 61, 58, 60]
```

### **Intervention Effectiveness**
| Metric | Value | Target |
|--------|-------|--------|
| **Tap-through Rate** | 41% | >35% |
| **Intervention Delivery** | 9.3k sent | 95% success rate |
| **Clinician Response** | 63% <24h | >60% |
| **False Alert Rate** | 12% | <15% |

---

## **Clinical Workflow Integration**

```mermaid
flowchart TD
    A[Patient Reports Symptoms] --> B{AI Risk Assessment}
    B -->|Low Risk<br/>0.0-0.3| C[Self-care Nudges]
    B -->|Medium Risk<br/>0.3-0.7| D[Care Team Alert]
    B -->|High Risk<br/>0.7-1.0| E[Urgent Clinical Review]
    
    C --> F[Track Engagement]
    D --> G[Clinician Triage]
    E --> H[Direct Patient Contact]
    
    G --> I{Clinical Decision}
    I -->|Adjust Medication| J[Rx Changes]
    I -->|Schedule Visit| K[Appointment]
    I -->|Monitor Closely| L[Enhanced Tracking]
    
    H --> M[Emergency Protocol]
    
    F --> N[Outcome Tracking]
    J --> N
    K --> N
    L --> N
    M --> N
    
    classDef patient fill:#E8F4FD,stroke:#1565C0,stroke-width:2px,color:#000000
    classDef ai fill:#F3E5F5,stroke:#6A1B9A,stroke-width:2px,color:#000000
    classDef clinical fill:#E8F5E8,stroke:#2E7D32,stroke-width:2px,color:#000000
    classDef urgent fill:#FFEBEE,stroke:#C62828,stroke-width:2px,color:#000000
    
    class A patient
    class B ai
    class D,G,I,J,K,L clinical
    class E,H,M urgent
```

---

## **Business Impact**

### **Cost Reduction Model**
- **Emergency Visit Cost:** $2,168 (avg)
- **Preventive Intervention:** $45 (avg)
- **Cost Avoidance:** $2,123 per prevented episode
- **Platform ROI:** 47:1 with 63% alert accuracy

### **Clinical Outcomes**
- **48-hour advance warning** enables proactive care
- **Reduced emergency visits** by 34% (projected)
- **Improved medication adherence** through timely interventions
- **Enhanced patient engagement** with 58% WAU

---

## **Documentation**

- [**Architecture Deep Dive**](./ARCHITECTURE.md) - Technical system design
- [**Product Strategy**](./PRODUCT_STRATEGY.md) - Market analysis & roadmap  
- [**API Documentation**](./API_DOCS.md) - Complete API reference
- [**Deployment Guide**](./DEPLOYMENT.md) - Production setup
- [**Testing Strategy**](./TESTING.md) - Quality assurance
- [**Performance Analysis**](./docs/performance-analysis/) - Benchmarks & optimization

---

## **Contributing**

We welcome contributions! Please see our [Contributing Guide](./CONTRIBUTING.md) for details.

### **Development Workflow**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests (`make test`)
4. Commit changes (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

---

##  **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

##  **Recognition**

- **$10k Grant** - Hospital partnership program
- **115 Patient Pilot** - Real-world validation
- **Clinical Advisory Board** - 3 practicing physicians
- **HIPAA Compliant** - Privacy-by-design architecture

---

*Built with ❤️ for better chronic disease management*# Aegis Health: AI Symptom and Wearable Flare-up Predictor



</div>
