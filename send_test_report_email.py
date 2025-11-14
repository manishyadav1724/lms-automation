#!/usr/bin/env python3
"""
send_test_report_email.py

Send the summary portion of a test report as the email body and attach the full
text report file.

Usage:
    python send_test_report_email.py --report reports/test_report_20251112_190045.txt \
        --to "manish@learntastic.com,sahil@learntastic.com" \
        --subject "Automation Test Summary"

If --report is omitted, the script will pick the latest file matching reports/test_report_*.txt.
"""

import os
import sys
import argparse
import smtplib
from email.message import EmailMessage
from datetime import datetime
import glob

# Try to import project config; otherwise fall back to environment variables
try:
    from src import config as project_config
except Exception:
    project_config = None


def find_latest_report(report_dir="reports", pattern="test_report_*.txt"):
    """Return the latest report file path or None if none found."""
    p = os.path.join(report_dir, pattern)
    files = glob.glob(p)
    if not files:
        return None
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]


def extract_summary_block(text):
    """
    Extract header + 'Summary' block from the text report.
    Expected structure (example):
      Test Run Report
      ================
      Start Time : ...
      End Time   : ...
      Total Time : ...

      Summary
      -------
      Total tests run : X
      Passed          : Y
      Failed          : Z
      Skipped         : A
      Unknown         : B
    This function returns that block as a string. If it can't find a clear block,
    it returns the entire file (safe fallback).
    """
    lines = text.splitlines()
    if not lines:
        return text

    # find indexes for "Start Time" and "Summary"
    start_idx = None
    summary_idx = None
    unknown_idx = None

    for i, ln in enumerate(lines):
        if start_idx is None and ln.strip().startswith("Start Time"):
            start_idx = i - 1  # include the "Test Run Report" header line above
            if start_idx < 0:
                start_idx = 0
        if summary_idx is None and ln.strip().startswith("Summary"):
            summary_idx = i
        if ln.strip().startswith("Unknown"):
            unknown_idx = i
            break

    # If we found start and summary and unknown, capture from start_idx..unknown_idx
    if start_idx is not None and summary_idx is not None and unknown_idx is not None:
        # include the blank line after unknown if present
        end_idx = unknown_idx + 1
        # include subsequent blank lines (optional)
        while end_idx < len(lines) and lines[end_idx].strip() == "":
            end_idx += 1
        block = "\n".join(lines[start_idx:end_idx]).strip() + "\n"
        return block

    # Fallback: try a simpler heuristic: include everything from "Start Time" through the next blank line after "Summary" block
    if start_idx is not None and summary_idx is not None:
        # try to find the blank line after summary section (look for blank line after "Summary" header)
        end_idx = summary_idx
        # move until two consecutive blank lines or until we hit "Details" or "End of report"
        for j in range(summary_idx, min(summary_idx + 30, len(lines))):
            if lines[j].strip().startswith("End of report") or lines[j].strip() == "":
                end_idx = j
                break
            end_idx = j + 1
        block = "\n".join(lines[start_idx:end_idx]).strip() + "\n"
        return block

    # As last resort, return the first ~20 lines
    return "\n".join(lines[:40]).strip() + "\n"


def send_email(report_path, recipients, subject=None,
               smtp_host=None, smtp_port=None,
               smtp_user=None, smtp_pass=None,
               smtp_use_tls=True, from_addr=None):
    """
    Read the report file, build an email whose body contains only the summary block,
    attach the full report, and send it to recipients.
    """
    if not os.path.exists(report_path):
        raise FileNotFoundError(f"Report file not found: {report_path}")

    with open(report_path, "r", encoding="utf-8") as fh:
        text = fh.read()

    # extract just the header + summary for the email body
    body_block = extract_summary_block(text)

    # Build message
    msg = EmailMessage()
    from_addr = from_addr or (getattr(project_config, "EMAIL_FROM", None) if project_config else "noreply@example.com")
    smtp_user = smtp_user or (getattr(project_config, "SMTP_USER", None) if project_config else None)
    smtp_pass = smtp_pass or (getattr(project_config, "SMTP_PASS", None) if project_config else None)
    smtp_host = smtp_host or (getattr(project_config, "SMTP_HOST", None) if project_config else os.environ.get("SMTP_HOST"))
    smtp_port = smtp_port or (getattr(project_config, "SMTP_PORT", None) if project_config else os.environ.get("SMTP_PORT", 587))
    smtp_use_tls = smtp_use_tls if smtp_use_tls is not None else (getattr(project_config, "SMTP_USE_TLS", True) if project_config else True)

    if isinstance(recipients, str):
        recipients_list = [r.strip() for r in recipients.split(",") if r.strip()]
    else:
        recipients_list = recipients

    if not recipients_list:
        raise RuntimeError("No recipients provided to send_email()")

    msg["From"] = from_addr
    msg["To"] = ", ".join(recipients_list)
    subject = subject or f"Crop 2.0 Dashboard – Daily Automation Summary  ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
    msg["Subject"] = subject

    # Plain-text body contains only the summary block
    msg.set_content(body_block)

    # Attach the full text report
    with open(report_path, "rb") as fh:
        data = fh.read()
    msg.add_attachment(data, maintype="text", subtype="plain", filename=os.path.basename(report_path))

    # Connect to SMTP and send
    if not smtp_host:
        raise RuntimeError("SMTP host not configured. Set src.config or environment variables.")

    smtp_port = int(smtp_port)
    print(f"[email] Connecting to {smtp_host}:{smtp_port} (user={smtp_user})")
    if smtp_use_tls:
        server = smtplib.SMTP(smtp_host, smtp_port, timeout=30)
        server.ehlo()
        server.starttls()
        server.ehlo()
    else:
        server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30)

    try:
        if smtp_user and smtp_pass:
            server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        print(f"[email] Sent report {os.path.basename(report_path)} to {recipients_list}")
    finally:
        try:
            server.quit()
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser(description="Send a test report: email the summary block as the body and attach full report.")
    parser.add_argument("--report", "-r", help="Path to text report file. If omitted, uses latest in ./reports/")
    parser.add_argument("--to", "-t", default=(getattr(project_config, "EMAIL_TO", None) if project_config else None),
                        help="Comma-separated recipients (overrides config).")
    parser.add_argument("--subject", "-s", default=None, help="Email subject (optional override).")
    args = parser.parse_args()

    report_path = args.report
    if not report_path:
        report_path = find_latest_report()
        if not report_path:
            print("No report found in ./reports/. Please provide --report <path>")
            sys.exit(1)
        print(f"Using latest report: {report_path}")

    recipients = args.to or (getattr(project_config, "EMAIL_TO", None) if project_config else None)
    if not recipients:
        print("No recipients configured. Use --to or set src.config.EMAIL_TO")
        sys.exit(1)

    # Send
    try:
        send_email(report_path, recipients, subject=args.subject)
    except Exception as e:
        print("Failed to send report:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
