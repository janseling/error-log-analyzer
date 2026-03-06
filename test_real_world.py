#!/usr/bin/env python3
"""
Test real-world error scenarios
"""
import sys
sys.path.insert(0, '/Users/max/Projects/error-log-analyzer')

from src import LogAnalyzer


def test_scenario_1():
    """Node.js Production App Crash"""
    print("\n" + "="*70)
    print("Scenario 1: Node.js Production App Crash")
    print("="*70)

    log = '''{"level":"error","message":"UnhandledPromiseRejectionWarning: Error: Connection lost: The server closed the connection.","timestamp":"2026-03-06T14:23:11.456Z","stack":"Error: Connection lost: The server closed the connection.\\n    at Protocol._enqueue (/app/node_modules/mysql/lib/protocol/Protocol.js:144:48)"}
{"level":"error","message":"Failed to connect to database after 5 retries","timestamp":"2026-03-06T14:23:12.123Z"}
{"level":"fatal","message":"Application shutting down due to database connection failure","timestamp":"2026-03-06T14:23:12.789Z"}'''

    analyzer = LogAnalyzer(api_key=None)
    result = analyzer.analyze(log)

    print(f"✅ Detected {result['total_errors']} errors, {result['unique_errors']} unique")
    print(f"✅ Summary: {result['summary']}")

    assert result['total_errors'] == 3, f"Expected 3 errors, got {result['total_errors']}"
    return True


def test_scenario_2():
    """Python Django Application Error"""
    print("\n" + "="*70)
    print("Scenario 2: Python Django Application Error")
    print("="*70)

    log = '''2026-03-06 09:15:33,456 - django.request - ERROR - Internal Server Error: /api/v1/users/
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/core/handlers/base.py", line 197, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File "/app/api/views.py", line 234, in get_users
    users = User.objects.filter(is_active=True).select_related('profile')
OperationalError: could not connect to server: Connection refused
	Is the server running on host "db" (172.18.0.2) and accepting
	TCP/IP connections on port 5432?'''

    analyzer = LogAnalyzer(api_key=None)
    result = analyzer.analyze(log)

    print(f"✅ Detected {result['total_errors']} errors, {result['unique_errors']} unique")
    print(f"✅ Summary: {result['summary']}")

    assert result['total_errors'] == 1, f"Expected 1 error, got {result['total_errors']}"
    return True


def test_scenario_3():
    """Go Microservices Communication Error"""
    print("\n" + "="*70)
    print("Scenario 3: Go Microservices Communication Error")
    print("="*70)

    log = '''2026/03/06 15:45:22 ERROR: Failed to call user-service: Post "http://user-service:8080/api/users": dial tcp 172.18.0.5:8080: connect: connection refused
2026/03/06 15:45:23 ERROR: Retry 1/3: user-service unavailable
2026/03/06 15:45:24 ERROR: Retry 2/3: user-service unavailable
2026/03/06 15:45:25 ERROR: Retry 3/3: user-service unavailable
2026/03/06 15:45:26 FATAL: Circuit breaker opened for user-service'''

    analyzer = LogAnalyzer(api_key=None)
    result = analyzer.analyze(log)

    print(f"✅ Detected {result['total_errors']} errors, {result['unique_errors']} unique")
    print(f"✅ Summary: {result['summary']}")

    assert result['total_errors'] == 5, f"Expected 5 errors, got {result['total_errors']}"
    return True


def test_scenario_4():
    """Memory Leak in Node.js"""
    print("\n" + "="*70)
    print("Scenario 4: Memory Leak in Node.js")
    print("="*70)

    log = '''{"level":"warn","message":"JavaScript heap out of memory","timestamp":"2026-03-06T16:00:00.000Z"}
{"level":"error","message":"FATAL ERROR: CALL_AND_RETRY_LAST Allocation failed - JavaScript heap out of memory","timestamp":"2026-03-06T16:00:01.000Z"}'''

    analyzer = LogAnalyzer(api_key=None)
    result = analyzer.analyze(log)

    print(f"✅ Detected {result['total_errors']} errors, {result['unique_errors']} unique")
    print(f"✅ Summary: {result['summary']}")

    assert result['total_errors'] == 2, f"Expected 2 errors, got {result['total_errors']}"
    return True


def test_scenario_5():
    """Python Celery Task Failure"""
    print("\n" + "="*70)
    print("Scenario 5: Python Celery Task Failure")
    print("="*70)

    log = '''2026-03-06 18:30:45,123 - celery.worker - ERROR - TaskHandlerError
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/celery/app/trace.py", line 450, in trace_task
    R = retval = fun(*args, **kwargs)
  File "/app/tasks/email_tasks.py", line 45, in send_welcome_email
    send_mail()
SMTPServerDisconnected: Connection unexpectedly closed'''

    analyzer = LogAnalyzer(api_key=None)
    result = analyzer.analyze(log)

    print(f"✅ Detected {result['total_errors']} errors, {result['unique_errors']} unique")
    print(f"✅ Summary: {result['summary']}")

    assert result['total_errors'] == 1, f"Expected 1 error, got {result['total_errors']}"
    return True


def test_scenario_6():
    """Database Migration Failure"""
    print("\n" + "="*70)
    print("Scenario 6: Database Migration Failure")
    print("="*70)

    log = '''2026-03-06 20:15:33,789 - django.db.migrations - ERROR - Error applying migration users.0012_alter_user_email
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/migrations/executor.py", line 116, in apply_migration
    migration.apply(project_state, schema_editor)
django.db.utils.ProgrammingError: column "email" of relation "auth_user" contains null values'''

    analyzer = LogAnalyzer(api_key=None)
    result = analyzer.analyze(log)

    print(f"✅ Detected {result['total_errors']} errors, {result['unique_errors']} unique")
    print(f"✅ Summary: {result['summary']}")

    assert result['total_errors'] == 1, f"Expected 1 error, got {result['total_errors']}"
    return True


def test_scenario_7():
    """Kubernetes Pod CrashLoopBackOff"""
    print("\n" + "="*70)
    print("Scenario 7: Kubernetes Pod CrashLoopBackOff")
    print("="*70)

    log = '''2026/03/06 22:00:00 ERROR: Liveness probe failed: HTTP probe failed with statuscode: 500
2026/03/06 22:00:05 ERROR: Readiness probe failed: HTTP probe failed with statuscode: 500
2026/03/06 22:00:10 FATAL: Application crashed: panic: runtime error: invalid memory address or nil pointer dereference'''

    analyzer = LogAnalyzer(api_key=None)
    result = analyzer.analyze(log)

    print(f"✅ Detected {result['total_errors']} errors, {result['unique_errors']} unique")
    print(f"✅ Summary: {result['summary']}")

    assert result['total_errors'] == 3, f"Expected 3 errors, got {result['total_errors']}"
    return True


if __name__ == '__main__':
    print("\n" + "="*70)
    print(" 🔧 Error Log Analyzer - Real-World Scenario Tests")
    print("="*70)

    tests = [
        ("Node.js Production App Crash", test_scenario_1),
        ("Python Django Application Error", test_scenario_2),
        ("Go Microservices Communication Error", test_scenario_3),
        ("Memory Leak in Node.js", test_scenario_4),
        ("Python Celery Task Failure", test_scenario_5),
        ("Database Migration Failure", test_scenario_6),
        ("Kubernetes Pod CrashLoopBackOff", test_scenario_7),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("\n" + "="*70)
    print(f" Results: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("="*70)

    if failed == 0:
        print("\n✅ All real-world scenarios tested successfully! 🎉\n")
    else:
        print(f"\n❌ {failed} test(s) failed\n")
        sys.exit(1)
