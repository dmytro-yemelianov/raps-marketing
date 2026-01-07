# RAPS Major Announcement Press Release Template

## Template Structure

### **FOR IMMEDIATE RELEASE**

**[HEADLINE - Action-Oriented, News-Worthy]**  
*[Subheadline - Additional context and benefit]*

**[CITY], [DATE]** – [Opening paragraph with who, what, when, where, why]

---

## Sample Press Releases

### 🚀 **Version 4.0 Launch Press Release**

**FOR IMMEDIATE RELEASE**

# RAPS 4.0 Introduces Enterprise-Grade Collaboration Features for Autodesk Platform Services Automation
*New release adds multi-user management, webhook processing, and advanced monitoring capabilities*

**Kyiv, Ukraine – March 15, 2026** – Dmytro Yemelianov, Autodesk Expert Elite and creator of RAPS (Rust Autodesk Platform Services CLI), today announced the release of RAPS 4.0, introducing comprehensive collaboration and team management features designed for enterprise APS deployments. The new version addresses the growing demand for team-based automation workflows in architecture, engineering, construction, and manufacturing organizations.

**Key New Features:**

**Multi-User Profile Management**  
RAPS 4.0 introduces role-based access controls and team-wide configuration profiles, enabling organizations to manage APS credentials and permissions across multiple users while maintaining security compliance. Teams can now share automation workflows while preserving individual accountability and audit trails.

**Webhook Event Processing**  
The new built-in webhook server provides real-time event processing capabilities, allowing teams to create responsive automation workflows that trigger based on APS platform events. This enables immediate processing of uploaded models, automatic quality checks, and integrated notification systems.

**Enterprise Monitoring and Observability**  
RAPS 4.0 includes comprehensive audit logging, OpenTelemetry integration for monitoring, and a web-based team dashboard for tracking APS usage, quotas, and operation history across the organization.

**Industry Impact**

"The AEC industry has been slow to adopt DevOps practices that have transformed software development," said Dmytro Yemelianov, creator of RAPS and Autodesk Expert Elite member. "RAPS 4.0 brings enterprise-grade collaboration features to APS automation, enabling teams to move beyond individual scripts to shared, scalable infrastructure."

Since its launch in 2024, RAPS has been adopted by over 500 organizations for automating Autodesk Platform Services workflows, processing millions of design files and reducing manual operation time by up to 90%.

**Market Reception**

"RAPS has transformed how our team handles model processing workflows," said [Customer Name], [Title] at [Company]. "What used to require dedicated staff monitoring web interfaces now runs automatically in our CI/CD pipeline. Version 4.0's collaboration features will let us scale this across our entire organization."

The AEC technology market is experiencing rapid growth in automation adoption, with Gartner predicting that 60% of construction companies will use automated design processing by 2027.

**Technical Specifications**

RAPS 4.0 maintains the tool's signature single-binary deployment with zero runtime dependencies while adding new capabilities:

- Multi-tenant authentication and authorization
- Real-time webhook event processing with custom handlers
- Comprehensive audit trails with 7-year retention support
- OpenTelemetry metrics and distributed tracing
- Web dashboard for team monitoring and management
- Advanced caching layer with Redis/Memcached support

**Availability and Pricing**

RAPS 4.0 is available immediately as a free, open-source download under the Apache 2.0 license. Enterprise support packages are available through the RAPS website for organizations requiring dedicated assistance, SLA guarantees, and custom development.

**Download Options:**
- Cargo: `cargo install raps`
- Homebrew: `brew install dmytro-yemelianov/tap/raps`
- Scoop: `scoop install raps`
- Docker: `docker pull dmytroyemelianov/raps`
- GitHub Releases: https://github.com/dmytro-yemelianov/raps/releases

**About RAPS**

RAPS (Rust Autodesk Platform Services CLI) is an open-source command-line tool that brings modern DevOps practices to Autodesk Platform Services automation. Built in Rust for performance and reliability, RAPS enables architecture, engineering, construction, and manufacturing teams to automate model processing workflows with enterprise-grade capabilities.

**About Dmytro Yemelianov**

Dmytro Yemelianov is an Autodesk Expert Elite member with over 15 years of experience in AEC technology development. He has been an ADN (Autodesk Developer Network) member since 2012 and is a regular speaker at Autodesk University and industry conferences. He specializes in AI integration, engineering systems, and enterprise platform architecture.

**Media Contact:**  
Dmytro Yemelianov  
Creator and Maintainer, RAPS  
Email: [contact@rapscli.xyz]  
LinkedIn: https://www.linkedin.com/in/dmytro-yemelianov/  
GitHub: https://github.com/dmytro-yemelianov

**Additional Resources:**
- Website: https://rapscli.xyz
- Documentation: https://rapscli.xyz/docs
- Community Discussions: https://github.com/dmytro-yemelianov/raps/discussions
- Technical Blog: https://rapscli.xyz/blog

###

---

### 🤖 **MCP Server Announcement Press Release**

**FOR IMMEDIATE RELEASE**

# RAPS Introduces First AI Assistant Integration for Autodesk Platform Services
*Revolutionary MCP server enables natural language APS operations through Claude, Cursor, and other AI tools*

**Kyiv, Ukraine – September 8, 2025** – RAPS, the leading open-source CLI for Autodesk Platform Services automation, today announced the integration of Model Context Protocol (MCP) server capabilities, making it the first tool to enable natural language operations with APS through AI assistants like Claude and Cursor IDE.

**Revolutionary AI Integration**

The new MCP server integration allows users to interact with Autodesk Platform Services using natural language commands instead of memorizing CLI syntax. Users can now simply ask their AI assistant to "upload this Revit model and translate it to SVF2 format" or "show me all my APS buckets with usage statistics."

"This represents a fundamental shift in how we interact with design data," said Dmytro Yemelianov, creator of RAPS and Autodesk Expert Elite member. "Instead of learning command syntax, teams can focus on their design intent and let AI handle the technical implementation."

**Supported AI Platforms**

The MCP server works with any AI assistant that supports the Model Context Protocol, including:
- Claude Desktop (Anthropic)
- Cursor IDE (natural language coding)
- Continue.dev (VS Code AI assistant)
- Any custom MCP-compatible implementation

**Technical Innovation**

The MCP integration reuses RAPS's battle-tested API clients and authentication systems, ensuring the same reliability and performance that command-line users expect. The AI assistant acts as a natural language interface while RAPS handles the complex APS operations in the background.

**Example interactions include:**
- "Translate all Revit files in this folder to SVF2 and IFC formats"
- "Check the translation status of my recent uploads"
- "Create a new bucket for the downtown project with persistent retention"
- "Generate a usage report for the last month's APS operations"

**Industry Impact**

The integration addresses a major barrier to APS automation adoption: the learning curve for command-line tools. By enabling natural language interaction, RAPS makes advanced APS automation accessible to designers and project managers who may not have deep technical backgrounds.

"This democratizes access to powerful automation capabilities," noted [Industry Expert Name], [Title] at [Research Firm]. "When project managers can ask an AI to process models instead of learning CLI commands, adoption accelerates dramatically."

**Immediate Availability**

The MCP server integration is available in RAPS v3.0, released today. Setup requires adding RAPS to the AI assistant's MCP configuration and takes less than 5 minutes to complete.

**Configuration example for Claude Desktop:**
```json
{
  "mcpServers": {
    "raps": {
      "command": "raps",
      "args": ["serve"]
    }
  }
}
```

**Market Context**

The announcement comes as the AEC industry increasingly adopts AI tools for design and project management workflows. Integration with existing design platforms like APS positions AI assistants as practical productivity tools rather than experimental technologies.

Recent surveys indicate that 78% of AEC professionals are interested in AI-powered workflow automation, but 65% cite technical complexity as a primary barrier to adoption.

**Future Development**

RAPS v3.5, planned for Q1 2026, will expand MCP capabilities to include streaming responses for long-running operations, enhanced conversation context, and integration with additional AI platforms including GitHub Copilot.

**About Model Context Protocol (MCP)**

Model Context Protocol is an open standard that enables AI assistants to access external data and tools safely and consistently. Developed by Anthropic and adopted by leading AI platforms, MCP provides a standardized way for AI assistants to interact with enterprise systems and developer tools.

**Availability**

RAPS v3.0 with MCP integration is available immediately as a free download:
- Installation: `cargo install raps` 
- Documentation: https://rapscli.xyz/docs/mcp-server
- GitHub: https://github.com/dmytro-yemelianov/raps

**Media Contact:**  
Dmytro Yemelianov  
Creator, RAPS  
LinkedIn: https://www.linkedin.com/in/dmytro-yemelianov/

###

---

## Distribution Strategy

### **Primary Outlets**
- **AEC Trade Publications**: ENR, Architect Magazine, Construction Executive
- **Technology Publications**: InfoWorld, SD Times, The New Stack  
- **Industry Analysts**: Gartner, Forrester, AEC industry research firms
- **Business Wire/PR Newswire**: Broad distribution to tech journalists

### **Secondary Outlets**
- **Autodesk Community**: Official blog submission, newsletter inclusion
- **Developer Publications**: DevOps.com, DZone, Stack Overflow Blog
- **LinkedIn Publisher**: Direct publication to professional network
- **Industry Conferences**: Press release coordination with speaking events

### **Supporting Materials**

Each press release should include:
- **High-resolution screenshots** of new features
- **Technical fact sheet** with specifications and requirements  
- **Customer quote library** with permission for use
- **Executive bio and headshot** 
- **Company backgrounder** and key statistics
- **Video demo links** for visual media outlets

### **Timing Strategy**

**Optimal Release Times:**
- **Tuesday-Thursday**: 10:00 AM EST for maximum journalist attention
- **Avoid Mondays**: Journalists catching up on weekend news
- **Avoid Fridays**: News gets buried over the weekend
- **Conference Coordination**: Release 2-3 days before major speaking events

### **Follow-Up Protocol**

**Day 0-1 (Release Day):**
- Direct outreach to key journalists and industry contacts
- Social media amplification across all channels
- Community forum posting with press release content
- Update website with news section feature

**Day 2-7:**
- Follow up with journalists who opened but didn't respond
- Pitch exclusive interviews or additional angles
- Monitor coverage and respond to any questions
- Track metrics and coverage reach

**Week 2-4:**  
- Leverage coverage for speaking opportunities
- Use quotes and coverage in future marketing materials
- Reach out to industry analysts for additional commentary
- Plan follow-up content based on journalist interest

### **Success Metrics**

**Coverage Metrics:**
- Number of publications that pick up the story
- Total estimated reach/circulation of coverage
- Quality tier of publications (major vs. niche)
- Sentiment analysis of coverage tone

**Engagement Metrics:**
- Website traffic increases following release
- Social media shares and engagement
- GitHub stars/downloads spike
- Speaking opportunity invitations

**Business Impact:**
- Enterprise inquiry increases
- Partnership discussion initiations  
- Community growth acceleration
- Brand mention increase in industry discussions

---

*These press release templates should be customized for each major announcement, with specific details, quotes, and supporting materials prepared in advance.*