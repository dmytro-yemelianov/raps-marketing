# FAQ Responses for Upwork

## Common Client Questions & Responses

---

## About Experience

### "Have you worked with Autodesk Forge/APS before?"

> Yes, extensively. I'm the creator of RAPS, the most comprehensive open-source CLI for Autodesk Platform Services. It covers all major APS APIs including Authentication, OSS, Model Derivative, Data Management, Design Automation, Webhooks, and the Construction Cloud APIs (Issues, RFIs, Assets, Submittals, Checklists).
>
> The tool is validated against Autodesk's official OpenAPI specifications and is used in production environments. You can see the project at https://github.com/dmytro-yemelianov/raps

### "Do you have experience with BIM 360 / ACC?"

> Yes, I have deep experience with both BIM 360 and Autodesk Construction Cloud (ACC). I've implemented:
> - Hub and project discovery
> - Document management (upload, versioning, folder operations)
> - Issues management with comments and attachments
> - RFI workflows
> - Assets, Submittals, and Checklists
> 
> I understand the nuances of 3-legged OAuth requirements, project ID formats, and the differences between BIM 360 and ACC APIs.

### "Have you worked with Design Automation?"

> Yes, I've built production workflows for AutoCAD, Revit, Inventor, and 3ds Max using Design Automation. This includes:
> - Creating and managing app bundles with custom automation code
> - Defining activities with proper input/output configurations
> - Executing work items at scale with monitoring
> - Handling the complexities of engine versions and cloud credits
>
> I can help with parametric model generation, batch processing, data extraction, and format conversion.

---

## About Technology

### "Why do you use Rust?"

> Rust offers significant advantages for CLI tools and automation:
> - **Single binary**: No runtime dependencies - users just download and run
> - **Performance**: Comparable to C/C++, great for file operations
> - **Reliability**: The type system catches entire classes of bugs at compile time
> - **Cross-platform**: Easy compilation for Windows, macOS, and Linux
>
> That said, I'm also proficient in Python and TypeScript if your project requires those for team compatibility.

### "Can you work with our existing stack (Node.js / Python / .NET)?"

> Absolutely. While I specialize in Rust, I'm comfortable integrating with any technology stack:
> - For Node.js: I can build npm packages or integrate via HTTP/CLI
> - For Python: I can create pip packages or Python bindings
> - For .NET: I can provide REST APIs or native interop
>
> What matters most is fitting into your team's workflow.

### "What's MCP / Model Context Protocol?"

> MCP (Model Context Protocol) is an open standard that allows AI assistants like Claude and Cursor to interact with external tools. I've built an MCP server for RAPS that exposes 14 APS operations as tools that AI can call directly.
>
> This means you can interact with APS using natural language: "List my buckets," "Start translating this file," etc. It's particularly useful for developers who want to explore APS capabilities quickly.

---

## About Process

### "What's your development process?"

> I follow a structured process:
> 1. **Discovery**: Understand your requirements thoroughly
> 2. **Design**: Architecture document for your approval before coding
> 3. **Implementation**: Iterative development with regular demos
> 4. **Testing**: Comprehensive testing including edge cases
> 5. **Documentation**: Clear docs for maintenance
> 6. **Handover**: Knowledge transfer and support period
>
> I prefer to start with a small milestone to build trust before larger commitments.

### "How do you handle communication?"

> I believe in transparent, proactive communication:
> - Daily async updates on progress/blockers
> - Weekly video calls if desired
> - Responsive on Upwork messages (usually within a few hours)
> - Clear documentation of decisions and trade-offs
>
> I'll never disappear - if there's an issue, you'll hear about it immediately, not at the deadline.

### "Can you work with our team?"

> Absolutely. I'm experienced in both solo delivery and collaborative work:
> - Code reviews and pair programming
> - Git workflow (feature branches, PRs, etc.)
> - Integration with your existing CI/CD
> - Knowledge transfer to your team
>
> I can adapt to your team's processes rather than imposing my own.

---

## About Pricing

### "Why are your rates higher than other developers?"

> A few reasons:
> 1. **Specialization**: APS expertise is rare - there are fewer than 500 active Forge/APS developers globally
> 2. **Quality**: My code is production-tested and validated against official specs
> 3. **Efficiency**: I solve problems faster because I've seen them before
> 4. **Reliability**: You're paying for on-time delivery, not just code
>
> Clients typically find that my higher rate results in lower total cost because of fewer revisions and production issues.

### "Can you do this for a fixed price?"

> Yes, I prefer fixed-price for well-defined projects. I'll provide a detailed estimate after understanding the full scope. For the estimate to be accurate, I need:
> - Clear requirements (doesn't have to be exhaustive, but clear)
> - Access to any existing systems I'll integrate with
> - Identified stakeholders for decisions
>
> I include reasonable revision rounds in my fixed quotes.

### "Do you offer discounts for startups?"

> I evaluate startup projects on a case-by-case basis. I consider:
> - Stage (pre-seed startups have different needs than Series A)
> - Scope (MVP vs. production system)
> - Relationship potential (long-term engagement value)
>
> I'm also open to equity/hybrid arrangements for the right opportunity. Let's discuss your situation.

---

## About Availability

### "When can you start?"

> I typically have availability within 1-2 weeks. For urgent projects, I may be able to start sooner depending on current commitments. Let's discuss your timeline and I'll give you an honest assessment.

### "What's your timezone / availability?"

> I'm based in [timezone] but have flexibility in my schedule. I typically work [hours] but can accommodate calls in other timezones as needed. Most of my work is async-compatible.

### "Can you commit to a longer engagement?"

> Yes, I'm open to retainer arrangements or multi-month projects. For ongoing work, I offer discounted rates and priority scheduling. Retainer clients get:
> - 15-25% rate reduction
> - Guaranteed availability
> - Priority response times
> - Monthly strategy calls

---

## About Specific Scenarios

### "We need to migrate from Forge to APS"

> This is a common need, and the good news is that most Forge code translates directly to APS. The main changes are:
> - Endpoint URLs (forge.autodesk.com → developer.api.autodesk.com)
> - Some OAuth scope names
> - A few response format changes
>
> I can audit your current implementation, create a migration plan, and support the transition with minimal disruption.

### "Our current integration isn't working well"

> Happy to help diagnose and fix. Common issues I see include:
> - Missing retry logic for transient failures
> - Inefficient token management
> - No rate limiting compliance
> - Missing error handling
>
> A technical audit would identify root causes, and I can then provide a prioritized fix plan.

### "We need this done very quickly"

> I understand urgency. For rush projects, I can:
> - Start immediately (if available)
> - Work extended hours
> - Prioritize MVP features
> - Deploy incrementally
>
> Rush projects typically carry a 25-50% premium to account for schedule disruption. Let's discuss what "quick" means for your specific case.
