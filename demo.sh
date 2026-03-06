#!/bin/bash
# 演示脚本 - 用于录制演示视频

echo "=========================================="
echo "🔓 Error Log Analyzer - 演示脚本"
echo "=========================================="
echo ""

# 场景 1: 安装
echo "📋 场景 1: 安装"
echo "命令: clawhub install max-gaan/error-log-analyzer"
echo ""

# 场景 2: 分析日志文件
echo "📋 场景 2: 分析日志文件"
echo "命令: python -m src analyze examples/sample-errors.log --no-ai"
echo ""
echo "输出:"
python3 -m src analyze examples/sample-errors.log --no-ai 2>&1 | head -30
echo ""

# 场景 3: Python API 使用
echo "📋 场景 3: Python API 使用"
echo "代码:"
cat << 'EOF'
from src import LogAnalyzer

analyzer = LogAnalyzer()
result = analyzer.analyze_file('error.log')

print(result['summary'])
for error in result['analyses']:
    print(f"{error['severity']}: {error['error_type']}")
EOF
echo ""

# 场景 4: Web UI
echo "📋 场景 4: 启动 Web UI"
echo "命令: cd web && python app.py"
echo "访问: http://localhost:5000"
echo ""

# 场景 5: JSON 输出
echo "📋 场景 5: JSON 格式输出"
echo "命令: python -m src analyze error.log --format json"
echo ""

# 场景 6: 导出报告
echo "📋 场景 6: 导出 Markdown 报告"
echo "命令: python -m src analyze error.log --format markdown --output report.md"
echo ""

echo "=========================================="
echo "✅ 演示准备完成！"
echo "=========================================="
