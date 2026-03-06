# Error Log Analyzer

**AI-powered error log analysis for developers**

[![ClawHub](https://img.shields.io/badge/ClawHub-Install%20Now-blue)](https://clawhub.ai/skills/max-gaan/error-log-analyzer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

## 🎯 What is this?

Error Log Analyzer is an OpenClaw skill that uses AI to explain your application errors in plain English and provide actionable fix suggestions.

**Key Features:**
- 🤖 AI explains errors like a senior developer would
- 🔍 Automatically identifies error patterns and root causes
- 💡 Get specific fix suggestions with code examples
- ⚡ Works with Node.js, Python, and Go logs
- 🎯 Filters noise so you focus on what matters

## 📦 Installation

### Quick Install (Recommended)
```bash
clawhub install max-gaan/error-log-analyzer
```

### Manual Install
```bash
git clone https://github.com/maxgaan/error-log-analyzer.git
cd error-log-analyzer
pip install -r requirements.txt
```

### Requirements
- Python 3.11 or higher
- OpenClaw installed
- API key for Claude or OpenAI (for AI features)

## 🚀 Quick Start

### 1. Set up API Key
```bash
export ANTHROPIC_API_KEY="your-key-here"
# or
export OPENAI_API_KEY="your-key-here"
```

### 2. Analyze Your First Log

**Command Line:**
```bash
python -m error_analyzer analyze /var/log/myapp/error.log
```

**Python API:**
```python
from error_analyzer import LogAnalyzer

analyzer = LogAnalyzer()
result = analyzer.analyze_file("/var/log/myapp/error.log")

for error in result.critical_errors:
    print(f"{error.severity}: {error.message}")
    print(f"Fix: {error.suggestion}")
```

**OpenClaw Chat:**
```
Analyze this error log:
[2026-03-06 10:23:45] ERROR: Connection refused to database
```

## 📊 Example Output

### Input Log
```
2026-03-06 14:23:11 ERROR: ECONNREFUSED
    at Database.connect (/app/src/db.js:45:12)
    at async initApp (/app/src/index.js:23:5)
```

### Output
```
🔴 CRITICAL: Database Connection Failed

What happened:
Your application tried to connect to a database at localhost:5432, 
but the connection was refused.

How to fix it:
1. Check if PostgreSQL is running:
   sudo systemctl status postgresql

2. Start the database:
   sudo systemctl start postgresql

3. Verify connection settings in .env:
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

## 🛠️ Features

### Supported Log Formats
- **Node.js**: Winston, Bunyan, Pino
- **Python**: logging module, structlog, loguru
- **Go**: standard library, zap, logrus

### AI Capabilities
- Explains technical errors in plain English
- Identifies root causes
- Provides severity assessment (Critical, High, Medium, Low)
- Suggests fixes with code examples

### Pattern Recognition
- Groups similar errors
- Detects error trends
- Filters duplicates
- Identifies correlations

## 📖 Documentation

- [Full Documentation](docs/)
- [API Reference](docs/api.md)
- [Configuration Guide](docs/configuration.md)
- [Examples](examples/)
- [FAQ](docs/faq.md)

## 💰 Pricing

| Plan | Events/Month | Price |
|------|--------------|-------|
| Starter | 5,000 | $39 one-time |
| Pro | 50,000 | $99 one-time |
| Team | 200,000 | $199 one-time |

**Free trial**: 100 free error analyses

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📝 License

MIT License - see [LICENSE](LICENSE)

## 🆘 Support

- 💬 Discord: [OpenClaw Community](https://discord.gg/clawd)
- 🐛 Issues: [GitHub Issues](https://github.com/maxgaan/error-log-analyzer/issues)
- 📧 Email: support@maxgaan.com

---

**Made by [Max_Gaan](https://github.com/maxgaan) for the OpenClaw community**
