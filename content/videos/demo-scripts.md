# RAPS Video Demo Scripts & Storyboards

## Core Demo Library

### 🎬 **Demo 1: "Zero to Pipeline in 5 Minutes"**
**Target Audience**: First-time users, decision makers  
**Duration**: 5 minutes  
**Goal**: Show complete value proposition from installation to working pipeline

#### Script Outline

**[0:00-0:30] Hook & Problem Setup**
```
"I'm going to show you how to go from manual Revit model uploads 
to a fully automated CI/CD pipeline in under 5 minutes.

No PowerShell scripts that break in production.
No clicking through web interfaces.
No waiting around to check translation status.

Just one command that handles everything."
```

**[0:30-1:00] Installation (Fast-Forward)**
```bash
# Speed through installation options
cargo install raps
# OR
brew install dmytro-yemelianov/tap/raps
# OR  
scoop install raps
```
*Text overlay: "One binary, zero runtime dependencies"*

**[1:00-2:00] Authentication Setup**
```bash
# Show environment variable setup
export APS_CLIENT_ID="your_client_id"
export APS_CLIENT_SECRET="your_client_secret"

# Test the connection
raps auth test
# ✓ 2-legged authentication successful
```

**[2:00-3:30] Your First Automated Workflow**
```bash
# Create a bucket  
raps bucket create my-project-bucket

# Upload a model (show progress bar)
raps object upload my-project-bucket model.rvt
# Uploading model.rvt... ████████████████ 100%
# URN: dXJuOmFkc2sub2...

# Start translation with wait flag
raps translate start $URN --format svf2 --wait
# Translation in progress... ██████████████████████ done (47s)
# ✓ Translation complete

# Get the results as JSON
raps translate manifest $URN -o json
```
*Show actual JSON output, highlight key fields*

**[3:30-4:30] Scale It Up: Batch Processing**
```bash
# Process multiple files at once
raps object upload my-bucket *.rvt --parallel=4

# Start all translations
for urn in $(raps object list my-bucket -o json | jq -r '.[].objectId'); do
  raps translate start $urn --format svf2 &
done

# Monitor progress
raps translate status --all --watch
```

**[4:30-5:00] The Big Picture**
```
"That's it. What used to take hours of manual work 
now runs automatically in your CI/CD pipeline.

✓ No clicking through web interfaces
✓ No waiting around checking status  
✓ No scripts that break when APS APIs change
✓ Full audit trail and error handling

This is how APS automation should work."
```

#### Production Notes
- **Screen Recording**: 4K, clean desktop background
- **Audio**: Professional microphone, noise cancellation
- **Pace**: Slow enough to follow, fast enough to maintain interest
- **Visuals**: Highlight important output, use text overlays for key concepts
- **Files**: Use realistic file names and project structure

---

### 🎬 **Demo 2: "AI Assistant + APS = Magic"**
**Target Audience**: AI/ML practitioners, modern developers  
**Duration**: 3 minutes  
**Goal**: Showcase MCP server natural language capabilities

#### Script Outline

**[0:00-0:20] The Problem**
```
"Memorizing CLI commands is so 2020. 
What if you could just ask your AI assistant 
to manage your APS workflows?"
```

**[0:20-0:40] MCP Setup (Speed Through)**
```bash
# Claude Desktop configuration
# Show config file briefly
{
  "mcpServers": {
    "raps": {
      "command": "raps",
      "args": ["serve"]
    }
  }
}
```

**[0:40-2:00] Natural Language APS Operations**

*Switch to Claude Desktop interface*

**User**: "Show me all my APS buckets"
```
Claude: I'll check your APS buckets for you.

[Uses raps_list_buckets tool]

You currently have 3 buckets:
• my-project-files (transient, 847 objects)
• production-models (persistent, 1,205 objects)  
• staging-bucket (transient, 23 objects)

Would you like me to show details for any specific bucket?
```

**User**: "Upload the Revit file in my current directory to the production bucket"
```
Claude: I'll upload the Revit file to your production-models bucket.

[Uses raps_upload_object tool]

✓ Successfully uploaded "office-building-v2.rvt" 
  URN: dXJuOmFkc2sub2...
  Size: 45.2 MB
  
Would you like me to start translating this model?
```

**User**: "Yes, translate to SVF2 format and let me know when it's done"
```
Claude: Starting SVF2 translation for your model...

[Uses raps_start_translation tool, then raps_check_translation_status]

Translation started successfully! 
Job ID: abc123...

I'll monitor the translation and notify you when complete.

[30 seconds later]
✓ Translation completed successfully in 42 seconds!
  
The SVF2 derivatives are ready for viewing.
Would you like me to generate a viewer URL?
```

**[2:00-2:40] The Power Revealed**
```
"Behind the scenes, Claude is using the same battle-tested 
RAPS CLI that you know and love. But instead of memorizing 
command syntax, you just describe what you want.

This works with any MCP-compatible AI:
• Claude Desktop  
• Cursor IDE
• Continue.dev
• Any tool supporting Model Context Protocol

Same reliable automation, zero cognitive overhead."
```

**[2:40-3:00] Call to Action**
```
"Ready to teach your AI to speak APS? 
Check the description for setup instructions."
```

#### Production Notes
- **Split Screen**: Terminal/CLI on one side, AI chat on other
- **Transitions**: Smooth switches between interfaces  
- **Timing**: Let AI responses play in real-time (don't speed up)
- **Authenticity**: Show real APS operations, real file uploads

---

### 🎬 **Demo 3: "Enterprise Pipeline Deep Dive"**
**Target Audience**: DevOps engineers, enterprise architects  
**Duration**: 8 minutes  
**Goal**: Show production-ready CI/CD integration

#### Script Outline

**[0:00-0:30] The Enterprise Challenge**
```
"Moving from prototype to production APS workflows means 
solving problems that demos don't show you:

• How do you handle authentication in CI environments?
• What about error handling and retry logic?
• How do you monitor and debug pipeline failures?
• Can you audit who processed what models when?

Let's build a production-ready pipeline from scratch."
```

**[0:30-1:30] GitHub Actions Integration**
```yaml
# .github/workflows/model-processing.yml
name: Model Processing Pipeline

on:
  push:
    paths: ['models/*.rvt']

jobs:
  process:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup RAPS
        uses: dmytro-yemelianov/raps-action@v1
        with:
          client-id: ${{ secrets.APS_CLIENT_ID }}
          client-secret: ${{ secrets.APS_CLIENT_SECRET }}
      
      - name: Process Changed Models
        run: |
          # Detect changed files
          git diff --name-only HEAD~1 HEAD | grep '\.rvt$' | while read file; do
            # Upload and translate each changed model
            raps object upload production-bucket "$file"
            raps translate start $URN --format svf2 --wait
          done
```

**[1:30-3:00] Error Handling & Monitoring**
```bash
# Show RAPS with comprehensive error handling
raps object upload production-bucket model.rvt \
  --retry-attempts 3 \
  --retry-backoff exponential \
  --timeout 300s \
  --progress-format json \
  --audit-log /var/log/raps/uploads.log

# Translation with monitoring hooks
raps translate start $URN \
  --format svf2 \
  --webhook-url https://api.company.com/webhooks/translation \
  --failure-notification slack://devops-alerts \
  --success-notification email://project-team@company.com
```

**[3:00-4:30] Multi-Environment Configuration**
```bash
# Development environment
raps config profile create development
raps config set --profile development endpoint "https://developer-api.autodesk.com"
raps config set --profile development bucket_prefix "dev-"

# Staging environment  
raps config profile create staging
raps config set --profile staging bucket_prefix "staging-"
raps config set --profile staging audit_level "verbose"

# Production environment
raps config profile create production  
raps config set --profile production bucket_prefix "prod-"
raps config set --profile production audit_level "full"
raps config set --profile production encryption_required true
```

**[4:30-6:00] Monitoring & Observability**
```bash
# RAPS exports OpenTelemetry metrics by default
export OTEL_EXPORTER_OTLP_ENDPOINT="https://monitoring.company.com/v1/traces"

# Run pipeline with full observability
raps pipeline run model-processing.yaml \
  --telemetry-enabled \
  --metrics-interval 5s \
  --distributed-tracing \
  --log-level debug

# Query metrics in Grafana/DataDog
# - aps_requests_total
# - aps_request_duration_seconds  
# - aps_translation_success_rate
# - aps_bucket_storage_bytes
```

**[6:00-7:00] Security & Compliance**
```bash
# Enterprise security configuration
raps config set secret_management "vault://secrets/aps"
raps config set network_policy "company-vpn-only"  
raps config set audit_retention "7_years"
raps config set encryption_at_rest true

# Run security scan
raps security scan --check-permissions --check-encryption --check-audit-trail
# ✓ All security checks passed
# ✓ Compliance requirements satisfied  
# ✓ Ready for production deployment
```

**[7:00-8:00] The Result**
```
"This is what enterprise APS automation looks like:

✓ Zero-downtime deployments  
✓ Full audit trails for compliance
✓ Automatic error recovery and retry logic
✓ Real-time monitoring and alerting
✓ Multi-environment isolation
✓ Enterprise security and encryption

Your design team pushes a commit.
Your infrastructure handles the rest.

That's the power of treating APS like the programmable platform it was always meant to be."
```

#### Production Notes
- **Multiple Screens**: Show CI/CD dashboard, monitoring tools, GitHub
- **Real Data**: Use actual enterprise-scale file sizes and processing times
- **Professional Quality**: Higher production value than quick demos
- **Technical Depth**: Don't dumb down for this audience

---

## Video Production Guidelines

### 📹 **Technical Specifications**
- **Resolution**: 1920x1080 minimum, 4K preferred
- **Frame Rate**: 60fps for screen recordings
- **Audio**: 48kHz, -16dB levels, professional microphone
- **Format**: MP4 with H.264 encoding

### 🎨 **Visual Standards**
- **Font**: JetBrains Mono for terminal, system UI font for overlays
- **Colors**: Match RAPS brand colors (rapeseed yellow, slate dark)
- **Terminal Theme**: Dark theme with high contrast
- **Cursor**: Highlight cursor for visibility
- **Zoom**: 150% browser zoom for readability

### 📊 **Content Guidelines**
- **Pace**: Allow 2-3 seconds to read command output
- **Authenticity**: Use real APS operations, not mocked data
- **Error Handling**: Show at least one failure/recovery scenario
- **Files**: Use realistic project names and file structures
- **Context**: Always explain WHY before showing HOW

### 🎯 **Distribution Strategy**

**Primary Channels:**
- YouTube (RAPS official channel)
- LinkedIn (native video posts)
- GitHub (embedded in documentation)
- Company website (landing page features)

**Supporting Channels:**  
- Twitter (short clips with links to full videos)
- Reddit (r/AutoCAD, r/Revit community engagement)
- Autodesk Forums (embedded in helpful responses)
- Conference presentations (live demo backup)

### 📈 **Success Metrics**
- **View Count**: >1000 views per demo within 30 days
- **Engagement**: >5% like rate, >2% comment rate
- **Conversion**: Track website visits from video descriptions
- **Share Rate**: Track social shares and embeds
- **Lead Generation**: Track demo requests from video CTAs

---

*These demo scripts should be treated as living documents, updated based on feature releases and community feedback.*