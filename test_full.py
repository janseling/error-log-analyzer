#!/usr/bin/env python3
"""
Full integration test for Error Log Analyzer
"""
import sys
sys.path.insert(0, '/Users/max/Projects/error-log-analyzer')

from src import LogAnalyzer

def test_basic_analysis():
    """Test basic analysis without AI."""
    print("Testing basic analysis...")
    
    analyzer = LogAnalyzer(api_key=None)  # No AI
    
    # Test Node.js logs
    nodejs_log = '''
{"level":"error","message":"Database connection failed","timestamp":"2026-03-06T10:23:45.123Z","stack":"Error: ECONNREFUSED\\n    at Database.connect (/app/src/db.js:45:12)"}
{"level":"warn","message":"High memory usage","timestamp":"2026-03-06T10:24:12.456Z"}
'''
    
    result = analyzer.analyze(nodejs_log)
    print(f"  ✅ Node.js: {result['total_errors']} errors, {result['unique_errors']} unique")
    assert result['total_errors'] > 0
    
    # Test Python logs
    python_log = '''
2026-03-06 14:23:11,456 - django.request - ERROR - Internal Server Error
Traceback (most recent call last):
  File "/app/views.py", line 45, in get_users
    raise ValueError("Test error")
ValueError: Test error
'''
    
    result = analyzer.analyze(python_log)
    print(f"  ✅ Python: {result['total_errors']} errors, {result['unique_errors']} unique")
    assert result['total_errors'] > 0
    
    # Test Go logs
    go_log = '''
2026/03/06 10:23:45 ERROR: Failed to connect
2026/03/06 10:24:12 WARN: Cache miss
'''
    
    result = analyzer.analyze(go_log)
    print(f"  ✅ Go: {result['total_errors']} errors, {result['unique_errors']} unique")
    assert result['total_errors'] > 0
    
    print("✅ Basic analysis tests passed!\n")


def test_error_clustering():
    """Test error clustering."""
    print("Testing error clustering...")
    
    analyzer = LogAnalyzer(api_key=None)
    
    # Similar errors should be clustered
    log = '''
2026-03-06 10:23:45 ERROR: Connection refused to localhost:5432
2026-03-06 10:23:46 ERROR: Connection refused to localhost:5432
2026-03-06 10:23:47 ERROR: Connection refused to localhost:5432
'''
    
    result = analyzer.analyze(log)
    print(f"  ✅ Clustered {result['total_errors']} errors into {result['unique_errors']} unique")
    assert result['unique_errors'] < result['total_errors']  # Should cluster
    
    print("✅ Error clustering test passed!\n")


def test_file_analysis():
    """Test file analysis."""
    print("Testing file analysis...")
    
    analyzer = LogAnalyzer(api_key=None)
    
    result = analyzer.analyze_file('examples/sample-errors.log')
    print(f"  ✅ File analysis: {result['total_errors']} errors, {result['unique_errors']} unique")
    assert result['total_errors'] > 0
    
    print("✅ File analysis test passed!\n")


def test_report_generation():
    """Test report generation."""
    print("Testing report generation...")
    
    analyzer = LogAnalyzer(api_key=None)
    
    log = '''
2026-03-06 10:23:45 ERROR: Connection timeout
2026-03-06 10:23:46 WARN: Slow response
'''
    
    result = analyzer.analyze(log)
    
    # Test text report
    from src.utils import generate_report
    text_report = generate_report(result['analyses'], format='text')
    assert 'ERROR' in text_report
    
    # Test JSON report
    json_report = generate_report(result, format='json')
    assert '"total_errors"' in json_report
    
    # Test markdown report
    md_report = generate_report(result['analyses'], format='markdown')
    assert '# ' in md_report
    
    print("  ✅ Text report generated")
    print("  ✅ JSON report generated")
    print("  ✅ Markdown report generated")
    
    print("✅ Report generation test passed!\n")


if __name__ == '__main__':
    print("=" * 70)
    print(" 🔧 Error Log Analyzer - Integration Tests")
    print("=" * 70)
    print()
    
    try:
        test_basic_analysis()
        test_error_clustering()
        test_file_analysis()
        test_report_generation()
        
        print("=" * 70)
        print(" ✅ ALL TESTS PASSED!")
        print("=" * 70)
        print()
        print("Ready for production use! 🚀")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
