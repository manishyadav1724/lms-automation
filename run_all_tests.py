#!/usr/bin/env python3
"""
run_all_tests.py

Run pytest programmatically (sequential), collect results, write a plain-text report,
and then automatically email the report (unless --no-email). No per-test sleep here —
per-test delays (if any) should be handled inside conftest.py teardown.

Usage:
    python run_all_tests.py
    python run_all_tests.py --no-email
    python run_all_tests.py --to "a@x.com,b@x.com" --subject "Nightly Report"
    python run_all_tests.py tests/some_test.py --pytest-args "-k smoke -s"
"""

import sys
import time
import argparse
from datetime import datetime
import pytest
import os
import subprocess
import importlib

# -------------------- Pytest result collector --------------------
class PytestResultCollector:
    """
    Collects per-test call-phase reports for report generation.
    """
    def __init__(self):
        self.test_reports = []
        self.session_start = None
        self.session_end = None

    def pytest_sessionstart(self, session):
        self.session_start = time.time()

    def pytest_runtest_logreport(self, report):
        # Only collect the "call" phase (actual test function execution)
        if report.when == "call":
            outcome = getattr(report, "outcome", None)
            if outcome is None:
                if getattr(report, "passed", False):
                    outcome = "passed"
                elif getattr(report, "failed", False):
                    outcome = "failed"
                elif getattr(report, "skipped", False):
                    outcome = "skipped"
                else:
                    outcome = "unknown"
            try:
                duration = float(report.duration)
            except Exception:
                duration = None
            longrepr = None
            try:
                longrepr = report.longreprtext if hasattr(report, "longreprtext") else str(report.longrepr)
            except Exception:
                longrepr = None
            self.test_reports.append({
                "nodeid": getattr(report, "nodeid", "<unknown>"),
                "outcome": outcome,
                "duration": duration,
                "longrepr": longrepr,
            })

    def pytest_sessionfinish(self, session, exitstatus):
        self.session_end = time.time()


# -------------------- report generation --------------------
def generate_report(collector: PytestResultCollector, out_path: str):
    reports = collector.test_reports
    total = len(reports)
    passed = sum(1 for r in reports if r["outcome"] == "passed")
    failed = sum(1 for r in reports if r["outcome"] == "failed")
    skipped = sum(1 for r in reports if r["outcome"] == "skipped")
    unknown = total - (passed + failed + skipped)
    start_ts = collector.session_start or 0
    end_ts = collector.session_end or time.time()
    start_dt = datetime.fromtimestamp(start_ts).strftime("%Y-%m-%d %H:%M:%S") if start_ts else "N/A"
    end_dt = datetime.fromtimestamp(end_ts).strftime("%Y-%m-%d %H:%M:%S")
    total_time = end_ts - start_ts if start_ts else 0.0

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("Test Run Report\n")
        fh.write("================\n")
        fh.write(f"Start Time : {start_dt}\n")
        fh.write(f"End Time   : {end_dt}\n")
        fh.write(f"Total Time : {total_time:.3f} seconds\n\n")

        fh.write("Summary\n")
        fh.write("-------\n")
        fh.write(f"Total tests run : {total}\n")
        fh.write(f"Passed          : {passed}\n")
        fh.write(f"Failed          : {failed}\n")
        fh.write(f"Skipped         : {skipped}\n")
        fh.write(f"Unknown         : {unknown}\n\n")

        fh.write("Details (test, outcome, duration seconds)\n")
        fh.write("-----------------------------------------------------\n")
        for r in reports:
            dur = f"{r['duration']:.3f}" if r["duration"] is not None else "N/A"
            fh.write(f"{r['nodeid']}  |  {r['outcome']:6}  |  {dur}\n")
            if r.get("longrepr"):
                fh.write("  Failure / Info:\n")
                excerpt = r["longrepr"]
                if len(excerpt) > 1000:
                    excerpt = excerpt[:1000] + "\n... (truncated)\n"
                fh.write(excerpt + "\n")
        fh.write("\nEnd of report\n")

    print(f"\nSaved report to: {out_path}")
    print("\n=== Summary ===")
    print(f"Total: {total}  Passed: {passed}  Failed: {failed}  Skipped: {skipped}")
    print(f"Total Time: {total_time:.3f} seconds\n")


# -------------------- email sending helpers --------------------
def send_report_via_module(report_path, to_addrs=None, subject=None):
    """
    Try to import send_test_report_email and call its send_email(report_path, recipients, subject=...).
    Returns True on success, False on failure.
    """
    try:
        module_name = "send_test_report_email"
        send_mod = importlib.import_module(module_name)
        # prefer 'send_email' function (updated script exposes send_email)
        send_fn = getattr(send_mod, "send_email", None)
        if send_fn is None:
            print("[send] module imported but 'send_email' not found; falling back to subprocess")
            return False

        if isinstance(to_addrs, str):
            to_list = [a.strip() for a in to_addrs.split(",") if a.strip()]
        else:
            to_list = to_addrs

        print(f"[send] calling send_email from module for {report_path} -> {to_list}")
        # call and accept both (report_path, recipients, subject=...) or (report_path, recipients, subject)
        try:
            send_fn(report_path, to_list, subject=subject)
        except TypeError:
            send_fn(report_path, to_list, subject)
        return True
    except Exception as e:
        print(f"[send] import/send via module failed: {e}")
        return False


def send_report_via_subprocess(report_path, to_addrs=None, subject=None):
    """
    Fallback: run send_test_report_email.py as a subprocess.
    """
    cmd = [sys.executable, "send_test_report_email.py", "--report", report_path]
    if to_addrs:
        if isinstance(to_addrs, (list, tuple)):
            to_arg = ",".join(to_addrs)
        else:
            to_arg = to_addrs
        cmd += ["--to", to_arg]
    if subject:
        cmd += ["--subject", subject]
    print(f"[send] running subprocess: {' '.join(cmd)}")
    try:
        res = subprocess.run(cmd, check=False)
        return res.returncode == 0
    except Exception as e:
        print("[send] subprocess invocation failed:", e)
        return False


# -------------------- main --------------------
def main():
    parser = argparse.ArgumentParser(description="Run pytest and generate a sequential test report (and optionally email it).")
    parser.add_argument("path", nargs="?", default="tests", help="Path to tests (file or directory). Default: ./tests")
    parser.add_argument("--report", "-r", default=None, help="Report output path (default: ./test_report_<ts>.txt)")
    parser.add_argument("--no-email", action="store_true", help="Generate report but do not send email.")
    parser.add_argument("--to", default=None, help="Comma-separated recipients to override config or script defaults.")
    parser.add_argument("--subject", default=None, help="Email subject override.")
    parser.add_argument("--pytest-args", "-p", default="", help="Additional pytest args (quoted). Example: -k 'smoke' -q")
    args = parser.parse_args()

    tests_path = args.path
    extra_args = args.pytest_args.split() if args.pytest_args else []

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_report = f"test_report_{ts}.txt"
    report_path = args.report or default_report

    collector = PytestResultCollector()

    # Build pytest arguments
    pytest_args = [tests_path] + ["-q"] + extra_args

    print("Running pytest with args:", " ".join(pytest_args))
    start_all = time.time()
    exit_code = pytest.main(pytest_args, plugins=[collector])
    end_all = time.time()

    # Ensure timestamps on collector
    if collector.session_end is None:
        collector.session_end = end_all
    if collector.session_start is None:
        collector.session_start = start_all

    generate_report(collector, report_path)

    # Email logic
    if args.no_email:
        print("[send] --no-email set; skipping email send.")
        sys.exit(exit_code if isinstance(exit_code, int) else 1)

    # Resolve recipients and subject
    to_addrs = None
    if args.to:
        to_addrs = [a.strip() for a in args.to.split(",") if a.strip()]

    subject = args.subject or f"Automated Test Report ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"

    # Try import-based send first, then subprocess fallback
    sent = send_report_via_module(report_path, to_addrs=to_addrs, subject=subject)
    if not sent:
        print("[send] falling back to subprocess runner")
        sent = send_report_via_subprocess(report_path, to_addrs=to_addrs, subject=subject)

    if sent:
        print(f"[send] Report {report_path} sent successfully.")
    else:
        print("[send] Failed to send report. Check SMTP configuration and send_test_report_email.py")

    # exit with pytest exit code so CI systems can detect test failure
    sys.exit(exit_code if isinstance(exit_code, int) else 1)


if __name__ == "__main__":
    main()
