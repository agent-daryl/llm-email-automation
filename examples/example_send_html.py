#!/usr/bin/env python3
"""
Example: Sending an HTML email with a template.

This example demonstrates how to create and send an HTML email using
the LLM Email Automation system.
"""

import sys
from pathlib import Path

# Add parent directory to path to import local modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.send_html_email import send_html_email


def send_welcome_email(email_address: str, user_name: str) -> bool:
    """
    Send a welcome email to a new user.
    
    Args:
        email_address: Recipient email address
        user_name: User's first name
    
    Returns:
        bool: True if email sent successfully
    """
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .container {{
                background: #f8f9fa;
                border-radius: 12px;
                padding: 30px;
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }}
            .highlight {{
                background: #e8f4f8;
                border-left: 4px solid #3498db;
                padding: 15px;
                margin: 20px 0;
            }}
            .btn {{
                display: inline-block;
                background: #3498db;
                color: white;
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 6px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome, {user_name}! 🎉</h1>
            
            <p>Thank you for signing up! We're excited to have you on board.</p>
            
            <div class="highlight">
                <strong>What's next?</strong><br>
                - Complete your profile<br>
                - Explore our features<br>
                - Join our community
            </div>
            
            <p>If you have any questions, just reply to this email.</p>
            
            <p>Best regards,<br>
            <strong>The Team</strong></p>
        </div>
    </body>
    </html>
    """
    
    return send_html_email(
        to_address=email_address,
        subject=f"Welcome to Our Platform, {user_name}!",
        html_content=html_content
    )


def send_report_email(email_address: str, report_title: str, stats: dict) -> bool:
    """
    Send a report email with statistics.
    
    Args:
        email_address: Recipient email address
        report_title: Title of the report
        stats: Dictionary of statistics to include
    
    Returns:
        bool: True if email sent successfully
    """
    stats_html = ""
    for key, value in stats.items():
        stats_html += f"""
        <tr>
            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{key}</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right; font-weight: bold;">{value}</td>
        </tr>
        """
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body>
        <h1>{report_title}</h1>
        <table style="width:100%; border-collapse: collapse; margin: 20px 0;">
            {stats_html}
        </table>
        <p>Please let me know if you have any questions about these results.</p>
    </body>
    </html>
    """
    
    return send_html_email(
        to_address=email_address,
        subject=f"Report: {report_title}",
        html_content=html_content
    )


if __name__ == "__main__":
    # Example usage
    print("Testing HTML email sender...")
    
    # Example 1: Welcome email
    success = send_welcome_email(
        email_address="recipient@example.com",
        user_name="John"
    )
    
    if success:
        print("✓ Welcome email sent successfully")
    else:
        print("✗ Failed to send welcome email")
