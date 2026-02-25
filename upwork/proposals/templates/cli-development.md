# Proposal Template: CLI Development

## Template Information
**Use For**: Jobs requesting command-line tools, terminal applications, automation scripts

---

## Proposal Template

```
Hi [Client Name],

Your need for a [describe their CLI need] caught my attention - this is exactly the type of tool I specialize in building.

**WHY I'M THE RIGHT FIT**

I'm the creator of RAPS, a production-grade CLI written in Rust with 50+ commands, used by developers worldwide. This gives me deep expertise in:

• Command structure and argument parsing
• Multiple output formats (JSON, YAML, CSV, table)
• Shell completions (bash, zsh, fish, PowerShell)
• Cross-platform support (Windows, macOS, Linux)
• Configuration management and profiles
• Progress indicators and user experience
• Error handling and exit codes for scripting

**UNDERSTANDING YOUR NEEDS**

From your description, you're looking for:
[Summarize their requirements - show you understand]

**WHAT I'LL DELIVER**

1. **Production-Ready CLI**
   • Clean command structure following CLI best practices
   • Helpful error messages and usage documentation
   • [Specific features they mentioned]

2. **Documentation**
   • README with installation and usage
   • Man page or detailed --help output
   • Example scripts and use cases

3. **Distribution**
   • Pre-built binaries for target platforms
   • Optional: npm/pip package for easy installation
   • Optional: Homebrew/Scoop formula

4. **Quality Assurance**
   • Unit and integration tests
   • Cross-platform testing
   • Performance benchmarks

**TECHNOLOGY CHOICE**

For CLI development, I recommend:

**Rust** (my specialty)
✅ Single binary, no runtime dependencies
✅ Excellent performance
✅ Cross-platform compilation
✅ Strong type system catches bugs early

**Python** (if you prefer)
✅ Faster initial development
✅ Easy to modify and extend
✅ Rich library ecosystem
⚠️ Requires Python runtime

**Node.js** (if JavaScript ecosystem)
✅ npm distribution is simple
✅ Good for JavaScript teams
⚠️ Requires Node.js runtime

I'll recommend based on your team's needs - happy to discuss.

**TIMELINE & INVESTMENT**

Based on the complexity described:
• Estimated duration: [X] weeks
• Investment: $[X,XXX]

This includes two rounds of revision and 30 days of bug-fix support.

**PROCESS**

1. **Kickoff Call**: Align on requirements and priorities
2. **Design Doc**: Command structure, I/O formats for your approval
3. **MVP**: Core functionality demo in [X] days
4. **Polish**: Error handling, edge cases, documentation
5. **Delivery**: Final binaries + source + docs

**READY TO START?**

Let's schedule a quick call to discuss your use case in detail. I'm available [suggest times].

Best regards,
[Your Name]

GitHub: github.com/dmytro-yemelianov/raps (see my CLI work in action)
```

---

## Customization Variations

### For Automation/Scripting Focus
```
I specialize in building automation tools that integrate with CI/CD pipelines. 
Key considerations I'll address:
• Standardized exit codes for error handling
• JSON output for parsing by other tools
• Non-interactive mode for unattended execution
• Environment variable configuration
```

### For API Client CLIs
```
Your API client CLI will include:
• Secure credential storage
• Token caching and refresh
• Rate limiting and retry logic
• Response caching for performance
• Multiple authentication methods
```

### For Data Processing CLIs
```
For data-heavy operations, I'll ensure:
• Streaming processing (handles large files)
• Progress indicators with ETA
• Resumable operations for long tasks
• Parallel processing where beneficial
```

---

## Technical Discussion Points

### If Client Asks About Rust
"Rust compiles to native binaries with no dependencies - your users just download and run. The performance is comparable to C/C++, and the type system eliminates entire classes of bugs. The main trade-off is development takes slightly longer than Python, but the result is more robust."

### If Client Wants Python
"Python is great for CLIs - I use Click or Typer for the interface, which gives excellent auto-generated help and shell completions. We can distribute via pip for easy installation. Main consideration is users need Python installed."

### If Client Needs Windows Focus
"Windows is fully supported. I'll include PowerShell completions, proper path handling, and test on Windows throughout development. We can also package as a Scoop formula for easy installation."
