#!/usr/bin/env python3
"""
Example: Sending a text email.

This example demonstrates how to send a simple text email using
the LLM Email Automation system.
"""

import sys
from pathlib import Path

# Add parent directory to path to import local modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.send_email import send_text_email


def send_simple_notification(to_address: str, message: str) -> bool:
    """
    Send a simple text notification email.
    
    Args:
        to_address: Recipient email address
        message: Message to send
    
    Returns:
        bool: True if email sent successfully
    """
    return send_text_email(
        to_address=to_address,
        subject="Notification",
        body=message
    )


def send_report(to_address: str, report_title: str, content: str) -> bool:
    """
    Send a text report email.
    
    Args:
        to_address: Recipient email address
        report_title: Title of the report
        content: Report content
    
    Returns:
        bool: True if email sent successfully
    """
    return send_text_email(
        to_address=to_address,
        subject=f"Report: {report_title}",
        body=f"Report: {report_title}\n\n{content}"
    )


if __name__ == "__main__":
    print("Testing text email sender...")
    
    # Example 1: Simple notification
    success = send_simple_notification(
        to_address="recipient@example.com",
        message="This is a test notification from LLM Email Automation."
    )
    
    if success:
        print("✓ Notification email sent successfully")
    else:
        print("✗ Failed to send notification email")
    
    # Example 2: Report email
    report_content = """
    Sales Report - Q1 2026
    ====================

    Total Sales: $125,000
    New Customers: 45
    Return Rate: 12%

    Next Quarter Goals:
    - Increase sales by 15%
    - Expand to 3 new regions
    - Launch new product line
    """
    
    success = send_report(
        to_address="recipient@example.com",
        report_title="Q1 2026 Sales Report",
        content=report_content
    )
    
    if success:
        print("✓ Report email sent successfully")
    else:
        print("✗ Failed to send report email")
