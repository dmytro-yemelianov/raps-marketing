# RAPS Enterprise Admin Cheat Sheet

## Enterprise Deployment

### 1. Prerequisites
```bash
# System Requirements
- Windows Server 2019+ / RHEL 8+ / Ubuntu 20.04+
- 4GB RAM minimum, 8GB recommended
- 10GB disk space for logs and cache
- Network: HTTPS (443), SSH (22), Custom ports configurable

# Required Access
- Autodesk Platform Services credentials with admin scope
- Enterprise identity provider (Azure AD, Okta, LDAP)
- Network access to APS endpoints (*.autodesk.com)
```

### 2. Enterprise Installation
```bash
# Download enterprise installer
curl -L https://rapscli.xyz/enterprise/installer.sh | bash

# Or manual installation
wget https://rapscli.xyz/enterprise/raps-enterprise-4.0.tar.gz
tar -xzf raps-enterprise-4.0.tar.gz
./install-enterprise.sh

# Verify installation
raps enterprise status
```

### 3. License Configuration
```bash
# Apply enterprise license
raps license apply --file enterprise-license.key

# Configure license server (for air-gapped environments)
raps license configure --server license.company.com:8443

# Check license status
raps license status --verbose
```

---

## Identity & Access Management

### SSO Integration
```bash
# Azure AD Setup
raps sso configure azure \
  --tenant-id YOUR_TENANT_ID \
  --client-id YOUR_APP_ID \
  --client-secret YOUR_SECRET

# Okta Setup  
raps sso configure okta \
  --domain company.okta.com \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_SECRET

# LDAP Setup
raps sso configure ldap \
  --server ldap://ldap.company.com:389 \
  --base-dn "dc=company,dc=com" \
  --bind-dn "cn=admin,dc=company,dc=com"
```

### Role-Based Access Control
```bash
# Create role templates
raps rbac create-role "APS_ADMIN" \
  --permissions "oss:*,dm:*,derivative:*"

raps rbac create-role "PROJECT_MANAGER" \
  --permissions "dm:read,dm:create,derivative:read"

raps rbac create-role "VIEWER" \
  --permissions "dm:read,derivative:read"

# Assign roles to users/groups
raps rbac assign-role user@company.com "APS_ADMIN"
raps rbac assign-role "Engineering Team" "PROJECT_MANAGER"
```

### User Management
```bash
# Bulk user import from CSV
raps users import users.csv --sso-mapping

# Provision user accounts
raps users create --email user@company.com \
  --role PROJECT_MANAGER \
  --projects project1,project2

# Deactivate users
raps users deactivate user@company.com --transfer-ownership admin@company.com
```

---

## Multi-Tenant Configuration

### Tenant Setup
```bash
# Create tenant hierarchy
raps tenant create "Company HQ" --type root
raps tenant create "North America" --parent "Company HQ"
raps tenant create "Engineering Dept" --parent "North America"

# Configure tenant isolation
raps tenant configure "Engineering Dept" \
  --isolation strict \
  --resource-quota 100GB \
  --api-rate-limit 1000/hour
```

### Resource Management
```bash
# Set resource quotas per tenant
raps quota set --tenant "Engineering Dept" \
  --storage 500GB \
  --api-calls 10000/day \
  --concurrent-jobs 50

# Monitor resource usage
raps quota status --tenant "Engineering Dept"
raps quota alerts --threshold 80% --notify admin@company.com
```

### Cost Allocation
```bash
# Configure cost tracking
raps billing configure --provider azure \
  --cost-center-mapping tenant-based

# Generate cost reports
raps billing report --tenant all --period monthly
raps billing export --format csv --file costs-2026-01.csv
```

---

## Security & Compliance

### Security Configuration
```bash
# Enable enterprise security features
raps security enable --audit-logging \
  --encryption-at-rest \
  --network-isolation

# Configure security policies
raps security policy create "data-classification" \
  --require-encryption \
  --restrict-external-sharing

# Setup certificate management
raps security cert install --file company-ca.crt
raps security cert auto-rotate --schedule monthly
```

### Compliance Settings
```bash
# GDPR compliance
raps compliance enable gdpr \
  --data-retention 7years \
  --right-to-be-forgotten \
  --consent-management

# SOC 2 compliance
raps compliance enable soc2 \
  --audit-trail detailed \
  --access-reviews quarterly \
  --change-management

# Industry-specific compliance (HIPAA, etc.)
raps compliance enable --framework hipaa
```

### Audit & Monitoring
```bash
# Configure comprehensive auditing
raps audit configure \
  --log-level detailed \
  --storage elasticsearch \
  --retention 5years

# Setup real-time monitoring
raps monitor configure \
  --metrics-endpoint prometheus:9090 \
  --alerts-webhook https://alerts.company.com \
  --dashboard grafana
```

---

## Performance & Scaling

### High Availability Setup
```bash
# Configure load balancers
raps ha configure \
  --nodes node1.company.com,node2.company.com \
  --health-check /health \
  --failover-timeout 30s

# Setup database clustering
raps db cluster init \
  --primary db1.company.com \
  --replicas db2.company.com,db3.company.com

# Configure shared storage
raps storage configure \
  --type nfs \
  --mount /shared/raps \
  --backup-schedule daily
```

### Performance Tuning
```bash
# Optimize for high throughput
raps performance tune \
  --worker-threads 32 \
  --memory-limit 8GB \
  --cache-size 2GB

# Configure connection pooling
raps connection-pool configure \
  --aps-connections 100 \
  --db-connections 50 \
  --timeout 30s

# Setup caching
raps cache configure redis \
  --servers cache1:6379,cache2:6379 \
  --ttl 3600
```

---

## Enterprise Operations

### Backup & Disaster Recovery
```bash
# Configure automated backups
raps backup configure \
  --schedule "0 2 * * *" \
  --retention 90days \
  --storage s3://company-backups

# Test disaster recovery
raps dr test --scenario full-outage
raps dr restore --backup 2026-01-01-full --verify

# Setup geo-redundancy
raps geo-redundancy enable \
  --primary us-east \
  --secondary eu-west \
  --sync-mode async
```

### Maintenance & Updates
```bash
# Schedule maintenance windows
raps maintenance schedule \
  --window "Saturday 02:00-06:00 UTC" \
  --notification-lead 48h

# Update management
raps update configure \
  --channel stable \
  --auto-update security \
  --manual-approval features

# Health monitoring
raps health monitor \
  --interval 60s \
  --alert-threshold 90% \
  --notify ops@company.com
```

---

## Monitoring & Analytics

### Key Performance Indicators
```bash
# System performance metrics
raps metrics system --dashboard

# Business KPIs
raps analytics generate \
  --report monthly-usage \
  --dimensions tenant,user,project
```

### Dashboard Configuration
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| API Success Rate | % of successful API calls | < 99% |
| Response Time | Average API response time | > 5 seconds |
| Error Rate | % of failed operations | > 1% |
| Storage Usage | Total storage consumed | > 80% quota |
| Active Users | Current concurrent users | Monitor trends |
| Cost per Transaction | Average cost per operation | Monitor variance |

### Alerting Rules
```bash
# Critical system alerts
raps alert create "api-failure-rate" \
  --condition "error_rate > 5%" \
  --severity critical \
  --notify "pagerduty:ops-team"

# Business process alerts
raps alert create "unusual-activity" \
  --condition "api_calls > baseline * 2" \
  --severity warning \
  --notify "email:admin@company.com"
```

---

## Troubleshooting

### Common Enterprise Issues

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| SSO Authentication Failed | Check IdP configuration | `raps sso test azure --verbose` |
| High Memory Usage | Monitor resource consumption | `raps performance analyze --memory` |
| Slow API Responses | Check network and caching | `raps debug network --trace` |
| License Violations | Verify usage vs. limits | `raps license audit --details` |
| Audit Log Gaps | Check logging configuration | `raps audit verify --range 24h` |

### Debug Commands
```bash
# System diagnostics
raps debug system --full-report

# Network connectivity tests
raps debug network --test-all-endpoints

# Performance profiling
raps debug performance --profile cpu,memory,network

# Configuration validation
raps debug config --validate-all
```

---

## Compliance Reports

### Automated Reporting
```bash
# Generate compliance reports
raps compliance report soc2 \
  --period Q1-2026 \
  --format pdf \
  --output compliance-reports/

# Security assessment
raps security assessment \
  --framework nist \
  --export security-report-2026.pdf

# Cost optimization report
raps cost-optimization analyze \
  --recommendations \
  --savings-potential
```

---

## Emergency Procedures

### Incident Response
```bash
# Emergency shutdown
raps emergency shutdown --reason "security-incident"

# Isolate tenant
raps emergency isolate --tenant "compromised-dept"

# Enable debug mode
raps emergency debug --level maximum --duration 1h

# Contact emergency support
raps support emergency --priority critical --issue "description"
```

### Recovery Procedures
```bash
# Service recovery
raps recovery start --from-backup latest
raps recovery verify --check-integrity

# Data recovery
raps data recover --tenant "affected-tenant" --point-in-time "2026-01-01T10:00:00Z"
```

---

## Support & Resources

### Enterprise Support Channels
- **Emergency**: +1-800-RAPS-911 (24/7)
- **Technical**: enterprise-support@rapscli.xyz
- **Account Management**: success@rapscli.xyz
- **Security**: security@rapscli.xyz

### Documentation & Training
- **Enterprise Portal**: [enterprise.rapscli.xyz](https://enterprise.rapscli.xyz)
- **Admin Training**: [rapscli.xyz/enterprise/training](https://rapscli.xyz/enterprise/training)
- **Best Practices**: [rapscli.xyz/enterprise/best-practices](https://rapscli.xyz/enterprise/best-practices)
- **Community**: [community.rapscli.xyz](https://community.rapscli.xyz)

---

## Quick Command Reference

### Daily Operations
```bash
raps status --all                    # System overview
raps users active                    # Active user count
raps quota status --all-tenants     # Resource usage
raps health check --comprehensive   # Full health check
```

### Weekly Reviews
```bash
raps analytics weekly               # Usage analytics
raps security scan                 # Security assessment
raps performance report            # Performance summary
raps costs summary --week         # Cost analysis
```

### Monthly Tasks
```bash
raps users review --inactive       # User cleanup
raps license reconcile             # License compliance
raps backup verify --all          # Backup integrity
raps update check --security      # Security updates
```

---
*RAPS Enterprise Admin Guide v4.0 | Updated: 2026 | Classification: Internal Use*