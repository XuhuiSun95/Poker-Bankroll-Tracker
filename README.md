# 🃏 Poker Bankroll Tracker

A CNCF-flavored, self-hosted poker bankroll analytics platform built by a developer, infra operator, ML/SecOps tinkerer — and poker player. Track every chip, spot your tilt, and outplay variance with data. ♠️📈

---

## 🎯 Core Features

- **Track Sessions**: From start to finish, with real-time updates and metrics
- **Live Analytics**: Visualize stack movements and session health in real time
- **AI Insights**: Detect tilt and suggest breaks based on behavior patterns
- **Comprehensive History**: Analyze trends, performance, and patterns over time
- **Offline Resilience**: Continue session tracking with auto-sync on reconnection

---

## 🏗️ Architecture Overview

```
Frontend (SvelteKit)
    ↓
Session Management API (FastAPI + GraphQL)
    ↓
Redis (live session state) ↔ Kafka (session events)
    ↓
Real-Time Analytics (SSE + RedisTimeSeries)
    ↓
ETL (Flink jobs)
    ↓
ClickHouse (aggregated metrics)
    ↓
Embedded Superset Dashboards
```

### Technology Stack

| Component        | Technology         | Purpose                                       |
|------------------|--------------------|-----------------------------------------------|
| **Frontend**     | SvelteKit          | Modern reactive UI with real-time updates     |
| **Backend**      | FastAPI + GraphQL  | Type-safe APIs for session management         |
| **Session Store**| Redis + TimeSeries | Store real-time data with TTL                 |
| **Messaging**    | Apache Kafka       | Real-time event streaming                     |
| **ETL**          | Apache Flink       | Process and aggregate session data            |
| **Analytics DB** | ClickHouse         | High-performance historical analytics         |
| **AI/ML**        | Ray                | Tilt detection and behavioral recommendations |
| **Dashboards**   | Superset           | Embedded user-facing analytics                |
| **Identity**     | Keycloak           | OIDC identity provider with PKCE              |
| **Service Mesh** | Istio              | mTLS, JWT validation, traffic management      |
| **Authorization**| OPA                | Policy-based access control                   |

---

## 🔐 Authentication & Authorization

The platform implements a zero-trust security model using **Keycloak** (OIDC with PKCE), **Istio** service mesh (mTLS + JWT validation), and **OPA** (policy-based authorization).

**Key Components**:
- **Keycloak**: Identity provider using OIDC authorization code flow with PKCE
- **Istio Gateway**: Validates JWT tokens at the edge and injects claims into headers
- **Istio Service Mesh**: Enforces mTLS for secure service-to-service communication
- **OPA**: Fine-grained authorization policies evaluated per request

> For detailed authentication and authorization flow diagrams and configuration, see [docs/SECURITY.md](docs/SECURITY.md)

---

## 🔄 Data Flow

### Real-Time Session Tracking
1. User creates session → FastAPI stores in Redis with TTL
2. Session events published to Kafka
3. Frontend receives live updates via SSE
4. AI models monitor behavior for tilt detection
5. Visualizations update live with stack movement

### Historical Analytics
1. ETL jobs process session events via Flink
2. Aggregated metrics are stored in ClickHouse
3. Superset dashboards render embedded in the frontend

---

## 📊 Analytics Strategy

### Live Analytics (Frontend)
- Stack visualization and current metrics
- Behavioral alerts and tilt detection
- Session break suggestions in real time

### Historical Analytics (Superset)
- Bankroll trend analysis over time
- Breakdown by stake, location, or session type
- Frequency and pattern analysis
- Fully customizable dashboards with SQL support

---

## ⚡ Quickstart

```bash
# Clone the repo
git clone https://github.com/your-username/poker-bankroll-tracker.git
cd poker-bankroll-tracker

# Install dependencies and start development
# (Implementation details to be added as project structure is built)
```

> See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for full deployment and Docker/Kubernetes setup.

---

## 🐳 Deployment

This platform is designed for modern containerized environments.

- Ready for Kubernetes, Docker Compose, or local development
- Includes infrastructure manifests in `/infrastructure`
- Monitoring, observability, and logging support (coming soon)
- Superset configuration for analytics dashboards is included

---

## 📁 Project Structure

```
.
├── docs/                    # Documentation
│   ├── ARCHITECTURE.md     # Technical architecture and design
│   ├── SECURITY.md         # Security and compliance strategy
│   └── FUTURE_ENHANCEMENTS.md # Roadmap and future features
├── infrastructure/          # Kubernetes manifests and Helm charts (planned)
├── session-management/      # FastAPI + GraphQL service (planned)
├── frontend/               # SvelteKit application (planned)
├── etl/                    # Data processing (Flink jobs) (planned)
└── dashboards/             # Superset dashboards (planned)
```

---

## ✅ Key Benefits

- Track real-time performance with instant updates
- Analyze session history with embedded dashboards
- Detect tilt and suggest breaks with AI-powered models
- Embrace CNCF-native, scalable microservices design
- Retain full control with a fully self-hosted system

---

## 📚 Additional Documentation

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Tech stack and service layout
- **[SECURITY.md](docs/SECURITY.md)** - Auth and compliance strategy
- **[FUTURE_ENHANCEMENTS.md](docs/FUTURE_ENHANCEMENTS.md)** - Roadmap and future vision

---

Originally built as a homelab project by a poker player and hands-on engineer — blending developer mindset, ML/SecOps experimentation, and CNCF-native architecture into a data-driven way to outplay variance, both at the table and in the stack. ♠️📊💡
