# The RAPS Manifesto: Bringing DevOps to the Built Environment

## The Problem: AEC is Stuck in the Stone Age

For decades, the Architecture, Engineering, and Construction (AEC) industry has embraced sophisticated design technology while operating these tools with manual, error-prone processes that belong in the 1990s.

**We're designing buildings with AI and constructing them with spreadsheets.**

While software development solved automation decades ago with CI/CD pipelines, AEC professionals are still:
- Clicking through web interfaces to upload models
- Manually checking translation status every 5 minutes  
- Copy-pasting URNs between applications
- Writing one-off PowerShell scripts that break in production
- Treating APS like a black box instead of a programmable platform

**This stops today.**

## The Vision: Infrastructure as Code for the Built Environment

Imagine a world where:
- Every model upload triggers automated quality checks
- Translation pipelines run in parallel across multiple formats
- Design changes automatically propagate through delivery systems
- Construction workflows integrate seamlessly with design data
- Manufacturing processes are driven by real-time model updates

**This is not a dream. This is RAPS.**

## Core Principles

### 1. **Automation Over Manual Labor**
If you're clicking through a web interface more than once, you're doing it wrong. Every repetitive task should be automated, every workflow should be scriptable, every process should be reproducible.

### 2. **Code Over Configuration**
Configuration files and UI settings are fragile. Code is testable, versionable, and documentable. Infrastructure as Code principles apply to APS workflows: everything should be defined in version-controlled, executable code.

### 3. **Pipelines Over One-Offs**  
Stop writing throw-away scripts. Build reusable pipelines that can be composed, extended, and shared across projects. Your automation should be as robust as your designs.

### 4. **Performance Over Convenience**
Web interfaces are convenient for exploration. Command-line tools are built for performance. When you need to process 100 models, you need a tool designed for scale, not for clicks.

### 5. **Open Source Over Vendor Lock-In**
The AEC industry has suffered too long under proprietary silos. RAPS is open source, MIT licensed, and designed for interoperability. Your automation should belong to you, not your vendor.

## Why Rust? Why Now?

### **Performance Without Compromise**
RAPS starts in milliseconds, handles thousands of files efficiently, and uses minimal memory. When your pipeline processes gigabytes of design data, every CPU cycle matters.

### **Reliability by Design**  
Rust's type system eliminates entire categories of bugs at compile time. No null pointer exceptions, no data races, no silent failures. When your automation runs critical infrastructure, reliability isn't optional.

### **Single Binary Deployment**
No Python virtual environments, no Node.js version conflicts, no Java runtime requirements. One binary, any platform, zero dependencies. Deployment complexity is the enemy of adoption.

### **Cross-Platform from Day One**
Windows, macOS, Linux—RAPS runs everywhere your team works. No platform discrimination, no second-class citizens.

## The MCP Revolution: Teaching AI to Speak APS

Version 3.0 introduces something unprecedented: **natural language APS operations**.

Instead of memorizing CLI commands, you can now simply ask your AI assistant:
- "Show me all my APS buckets"  
- "Translate this Revit model to SVF2 format and wait for completion"
- "Upload these 50 files and start derivative processing in parallel"

The Model Context Protocol (MCP) server bridges the gap between human intent and platform capabilities. This isn't just convenience—it's a fundamental shift in how we interact with design data.

## Beyond Autodesk: A Blueprint for Industry Transformation

RAPS is more than an APS client. It's a proof of concept for what modern AEC tooling should look like:

- **API-First**: Every operation should be programmable
- **CLI-Native**: Command-line interfaces scale better than GUIs  
- **Pipeline-Ready**: Designed for automation from the ground up
- **AI-Integrated**: Natural language operations as a first-class feature
- **Community-Driven**: Open source development with transparent roadmaps

## The Call to Action

**To AEC Developers**: Stop accepting inferior tooling. Demand better. Build better. The technology exists—use it.

**To Engineering Managers**: Your teams deserve tools as sophisticated as the buildings they design. Invest in automation infrastructure, not more manual processes.

**To Technology Leaders**: The future of AEC is programmable. Position your organization for success by adopting infrastructure-as-code practices today.

**To Students and New Professionals**: Learn these tools now. The AEC industry is transforming, and the next generation of leaders will be those who bridge design and technology.

## The RAPS Promise

We commit to:
- **Transparent Development**: Open source, public roadmaps, community input
- **Performance Excellence**: Sub-second startup, efficient resource usage, scalable architecture
- **Documentation Quality**: Every feature documented, every workflow explained, every example tested
- **Community Support**: Responsive maintainership, welcoming contribution process, inclusive development

## Join the Movement

The future of AEC automation starts with your next project. Whether you're uploading a single model or orchestrating enterprise-scale workflows, RAPS provides the foundation for what's possible.

**Download RAPS. Automate your workflows. Transform your industry.**

---

*The Stone Age ended not because we ran out of stones, but because we discovered better tools.*

*The Manual Age of AEC ends today.*

**🌼 RAPS (rapeseed) — Bringing CI/CD to the Built Environment**

---

### About the Author

Dmytro Yemelianov is an Autodesk Expert Elite member with 15+ years in AEC technology. He has spoken at Autodesk University, contributed to the ADN community since 2012, and believes that better tools create better buildings.

### Get Involved

- **GitHub**: https://github.com/dmytro-yemelianov/raps
- **Website**: https://rapscli.xyz
- **Documentation**: https://rapscli.xyz/docs
- **Discussions**: https://github.com/dmytro-yemelianov/raps/discussions

*This manifesto is licensed under Creative Commons Attribution 4.0 and may be freely shared with attribution.*