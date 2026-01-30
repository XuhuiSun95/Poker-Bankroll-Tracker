# 🔒 Security & Compliance

## Authentication & Authorization

The platform implements a zero-trust security model using **Keycloak** for identity management, **Istio** service mesh for secure service-to-service communication, and **OPA (Open Policy Agent)** for fine-grained authorization policies.

### **OIDC with PKCE**
- **Modern Authentication Flow**: OpenID Connect (OIDC) authorization code flow with PKCE (Proof Key for Code Exchange)
- **JWT Tokens**: Stateless session management with refresh tokens
- **Role-Based Access Control (RBAC)**: Granular permissions for different user types
- **API Rate Limiting**: Redis-based rate limiting to prevent abuse
- **GraphQL Security**: Query depth limiting and complexity analysis

> **Note**: OIDC (OpenID Connect) is built on top of OAuth 2.0/2.1 and adds identity layer. PKCE is a security extension that makes the authorization code flow more secure, especially for public clients.

### **Implementation Details**
```yaml
# OIDC Configuration
oidc:
  provider: "Keycloak" # Self-hosted identity provider
  flow: "authorization_code"
  pkce: true
  scopes: ["openid", "profile", "email", "session:read", "session:write"]
  redirect_uri: "https://app.pokerbankroll.com/callback"

# JWT Configuration
jwt:
  algorithm: "RS256"
  issuer: "https://keycloak.example.com/realms/poker-bankroll"
  audience: "poker-bankroll-users"
  expiration: "15m"
  refresh_expiration: "7d"
```

### Authentication Flow (Keycloak + Istio)

```
User → Frontend → Istio Gateway → Keycloak
                              ↓
                    JWT Token (validated)
                              ↓
                    Service Mesh (mTLS)
                              ↓
                    Backend Services
```

1. **User Authentication**:
   - User authenticates via Keycloak using OIDC authorization code flow with PKCE
   - Frontend generates a code verifier and code challenge (PKCE)
   - User is redirected to Keycloak for authentication
   - Keycloak validates credentials and issues authorization code
   - Frontend exchanges authorization code + code verifier for tokens
   - Keycloak issues JWT access tokens and refresh tokens
   - Tokens include user identity (`sub`), scopes, and custom claims

2. **Edge Authentication (Istio)**:
   - Istio Gateway validates JWT tokens at the ingress using `RequestAuthentication` policy
   - Token validation checks signature against Keycloak's JWKS endpoint
   - Validates token issuer, audience, and expiration
   - Valid tokens are forwarded to backend services with claims injected into headers (e.g., `x-jwt-payload`)
   - Invalid or missing tokens result in 401 Unauthorized responses

3. **Service-to-Service Communication**:
   - Istio service mesh enforces mutual TLS (mTLS) between all services
   - Services communicate securely without additional authentication overhead
   - Service identity is verified via Istio's SPIFFE-based identity system
   - All inter-service traffic is encrypted and authenticated

### Authorization Flow (OPA)

```
Request → Istio AuthorizationPolicy → OPA Envoy Plugin
                                    ↓
                            Policy Evaluation
                                    ↓
                            Allow / Deny
```

1. **Policy-Based Authorization**:
   - OPA (Open Policy Agent) evaluates authorization policies for each request
   - Policies are written in Rego and stored in OPA's policy store
   - Istio `AuthorizationPolicy` resources delegate authorization decisions to OPA via Envoy's External Authorization filter
   - Policies are evaluated based on JWT claims, request path, method, and other context

2. **Authorization Checks**:
   - **Resource-Level**: Policies check if the user has access to specific resources (e.g., sessions)
   - **Scope-Based**: Validates OAuth scopes (e.g., `session:read`, `session:write`)
   - **Role-Based**: Evaluates user roles and permissions from Keycloak
   - **Context-Aware**: Considers request path, method, and user attributes

3. **Policy Examples**:
   - Users can only access their own session data (resource ownership validation)
   - Admin users have elevated permissions for analytics
   - Rate limiting based on user tier or subscription level
   - GraphQL query complexity limits based on user role

### Security Components Integration

| Component | Role | Configuration |
|-----------|------|---------------|
| **Keycloak** | Identity Provider | OIDC / OAuth 2.1, JWT signing, user management, role assignment |
| **Istio Gateway** | Edge Security | JWT validation, TLS termination, request routing |
| **Istio Service Mesh** | Service Security | mTLS, service identity, traffic policies |
| **OPA** | Authorization Engine | Policy evaluation, fine-grained access control |
| **Backend Services** | Application Logic | Trust JWT claims from Istio headers, enforce business rules |

### Token Flow Details

- **Access Tokens**: Short-lived (15 minutes), contain user identity and scopes
- **Refresh Tokens**: Long-lived (7 days), used to obtain new access tokens
- **Token Claims**: Include `sub` (user ID), `scope` (permissions), `realm_access` (roles), `email`, `preferred_username`
- **Header Injection**: Istio injects validated JWT payload into `x-jwt-payload` header for backend services
- **Token Refresh**: Frontend uses refresh token to obtain new access tokens before expiration

### Benefits

- **Zero Trust**: Every request is authenticated and authorized, no implicit trust
- **Centralized Identity**: Single source of truth for user identity and roles
- **Fine-Grained Control**: OPA policies enable complex authorization logic
- **Service Isolation**: mTLS ensures secure inter-service communication
- **Audit Trail**: All authentication and authorization decisions are logged
- **PKCE Security**: Prevents authorization code interception attacks
- **Stateless Authentication**: JWT tokens enable horizontal scaling without session storage

## Data Security

### **Encryption at Rest**
- **Database Encryption**: ClickHouse and Redis data encrypted at rest
- **File System Encryption**: All persistent storage encrypted
- **Backup Encryption**: Automated encrypted backups with key rotation

### **Encryption in Transit**
- **TLS 1.3**: All communications encrypted with latest TLS
- **Certificate Management**: Automated certificate rotation and validation
- **API Security**: GraphQL and REST endpoints secured with HTTPS

### **Data Privacy**
- **GDPR Compliance**: Right to be forgotten and data portability
- **Data Minimization**: Only collect necessary session data
- **Anonymization**: Optional data anonymization for analytics
- **Audit Logging**: Comprehensive access and modification logs

## Infrastructure Security

### **Container Security**
- **Image Scanning**: Automated vulnerability scanning for all container images
- **Runtime Security**: Container runtime security monitoring
- **Network Policies**: Kubernetes network policies for service isolation
- **Secrets Management**: Kubernetes secrets with encryption

### **Network Security**
- **Zero Trust**: Network segmentation and micro-perimeters
- **API Gateway**: Centralized security controls
- **DDoS Protection**: Rate limiting and traffic filtering
- **VPN Access**: Secure remote access for administration

## Application Security

### **Input Validation**
- **GraphQL Validation**: Comprehensive input validation and sanitization
- **SQL Injection Prevention**: Parameterized queries and ORM usage
- **XSS Protection**: Content Security Policy and input sanitization
- **CSRF Protection**: Token-based CSRF protection

### **API Security**
- **Rate Limiting**: Per-user and per-endpoint rate limiting
- **GraphQL Depth Limiting**: Prevent complex query attacks
- **Authentication**: JWT-based stateless authentication
- **Authorization**: Role-based access control for all endpoints

## Monitoring & Incident Response

### **Security Monitoring**
- **SIEM Integration**: Centralized security event monitoring
- **Anomaly Detection**: AI-powered security anomaly detection
- **Threat Intelligence**: Integration with threat intelligence feeds
- **Vulnerability Scanning**: Regular automated security scans

### **Incident Response**
- **Automated Alerts**: Real-time security incident notifications
- **Forensic Capabilities**: Comprehensive audit trail preservation
- **Recovery Procedures**: Documented incident response procedures
- **Communication Plan**: Stakeholder notification procedures

## Compliance & Governance

### **Regulatory Compliance**
- **GDPR**: European data protection compliance
- **CCPA**: California privacy regulation compliance
- **SOC 2**: Security and availability certification
- **PCI DSS**: Payment card industry standards (if applicable)

### **Data Governance**
- **Data Classification**: Sensitive data identification and handling
- **Access Controls**: Principle of least privilege
- **Data Retention**: Automated data lifecycle management
- **Audit Trails**: Comprehensive activity logging and monitoring
