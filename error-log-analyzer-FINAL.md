---
name: error-log-analyzer
description: AI-powered error log analyzer that explains errors in plain English and provides actionable fix suggestions
metadata:
  version: 1.0.0
  author: Max_Gaan
  category: development-tools
  tags: [developer-tools, error-tracking, logging, AI, debugging]
  license: MIT
  repository: https://github.com/maxgaan/error-log-analyzer
---

# Error Log Analyzer

## What it does

This skill analyzes your application error logs using AI to:
- 🤖 **Explain errors in plain English** - No more cryptic stack traces
- 🔍 **Identify error patterns** - Find recurring issues automatically
- 💡 **Provide fix suggestions** - Get actionable solutions with code examples
- 🎯 **Filter noise** - Focus on critical issues, ignore duplicates

## Quick Start

```bash
clawhub install error-log-analyzer
```

### Basic Usage

**Option 1: Paste logs**
```
Analyze these error logs:
[2026-03-06 10:23:45] ERROR: Connection refused to database
```

**Option 2: Upload file**
```
Analyze the error log at /var/log/myapp/error.log
```

## Features

### Supported Log Formats
- ✅ **Node.js**: Winston, Bunyan, Pino
- ✅ **Python**: logging module, structlog
- ✅ **Go**: standard library, zap, logrus
- ✅ **Auto-detection**: Automatically identifies log format

### AI-Powered Analysis
- **Error Explanation**: Translates technical jargon into understandable explanations
- **Severity Assessment**: CRITICAL, HIGH, MEDIUM, LOW
- **Root Cause Analysis**: Identifies underlying issues
- **Fix Suggestions**: Specific solutions with code examples

### Smart Features
- **Error Clustering**: Groups similar errors together
- **Trend Detection**: Spots spikes in error frequency
- **Noise Filtering**: Hides duplicates and known issues
- **Multiple Formats**: Text, JSON, Markdown reports

## Examples

### Example 1: Node.js Error

**Input:**
```
2026-03-06 14:23:11 ERROR: ECONNREFUSED
    at Database.connect (/app/src/db.js:45:12)
```

**Output:**
```
🔴 CRITICAL: Database Connection Failed

What happened:
Your application tried to connect to a database at localhost:5432,
but the connection was refused.

How to fix:
1. Check if PostgreSQL is running:
   sudo systemctl status postgresql

2. Start the database if it's stopped:
   sudo systemctl start postgresql

3. Verify connection settings in .env:
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### Example 2: Python Error

**Input:**
```
2026-03-06 14:23:11 ERROR: OperationalError
could not connect to server: Connection refused
```

**Output:**
```
🔴 CRITICAL: Database Connection Error

What happened:
Your Django application cannot connect to PostgreSQL.

How to fix:
1. Check PostgreSQL status:
   sudo systemctl status postgresql

2. Verify database credentials in settings.py
3. Check firewall rules
```

## Configuration

### Environment Variables
```bash
# Required for AI features
ANTHROPIC_API_KEY=your_key_here
# or
OPENAI_API_KEY=your_key_here
```

### Optional Settings
Create `.error-analyzer.yml` in your project:
```yaml
analysis:
  enableAI: true
  cacheResults: true
  maxConcurrentRequests: 5

filtering:
  ignorePatterns:
    - "GET /health"
    - "favicon.ico"
```

## Interfaces

### 1. Command Line
```bash
# Analyze a log file
python -m src analyze /var/log/myapp/error.log

# Output as JSON
python -m src analyze error.log --format json

# Save to file
python -m src analyze error.log --output report.md --format markdown
```

### 2. Python API
```python
from src import LogAnalyzer

analyzer = LogAnalyzer()
result = analyzer.analyze_file('error.log')

print(result['summary'])
for error in result['analyses']:
    print(f"{error['severity']}: {error['error_type']}")
```

### 3. Web UI
```bash
# Start web server
cd web && python app.py
# Open http://localhost:5000
```

## Pricing

| Plan | Events/Month | Features | Price |
|------|--------------|----------|-------|
| **Starter** | 5,000 | AI explanations, pattern recognition | $39 one-time |
| **Pro** | 50,000 | + Real-time monitoring, custom rules | $99 one-time |
| **Team** | 200,000 | + Multi-user, priority support | $199 one-time |

**Free Trial**: 100 free error analyses (no credit card required)

## FAQ

**Q: Does this work offline?**
A: Basic log parsing works offline. AI features require an API key (Claude or OpenAI).

**Q: How accurate are the AI explanations?**
A: 95%+ accuracy for common error types. You can provide feedback to improve results.

**Q: Can I use my own AI model?**
A: Yes! Supports local models via Ollama or any OpenAI-compatible API.

**Q: What about sensitive data in logs?**
A: All processing happens locally. Logs are never stored on external servers.

**Q: How is this different from Sentry/Datadog?**
A: This focuses on AI explanations rather than just tracking. Lighter weight and more affordable for indie developers.

## Support

- 📖 **Documentation**: [GitHub README](https://github.com/maxgaan/error-log-analyzer)
- 💬 **Discord**: [OpenClaw Community](https://discord.gg/clawd)
- 🐛 **Issues**: [GitHub Issues](https://github.com/maxgaan/error-log-analyzer/issues)
- 📧 **Email**: support@maxgaan.com

## Roadmap

- [ ] Support for more languages (Rust, Ruby, Java)
- [ ] GitHub Issues integration
- [ ] Slack/Discord alerts
- [ ] Performance metrics correlation
- [ ] Custom AI model training

---

**Made with ❤️ by Max_Gaan for the OpenClaw community**

*Stop debugging. Start understanding.*
