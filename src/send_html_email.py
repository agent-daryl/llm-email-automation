#!/usr/bin/env python3
"""
Send HTML emails using Gmail SMTP.

This module provides functions for sending HTML-formatted emails through Gmail's SMTP server.
It uses app password authentication for security.

_usage:_
    python send_html_email.py <to_email> <subject> < <html_file>
    python send_html_email.py --to <email> --subject <subject> --html <content>

_examples:_
    python send_html_email.py recipient@example.com "Test HTML" < body.html
    python send_html_email.py --to recipient@example.com --subject "Report" --html "<html>..."
"""

import smtplib
import argparse
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from .utils import load_credentials, validate_email_address


def send_html_email(
    to_address: str,
    subject: str,
    html_content: str,
    from_address: Optional[str] = None,
    creds: Optional[dict] = None
) -> bool:
    """
    Send an HTML-formatted email.
    
    Args:
        to_address: Recipient email address
        subject: Email subject line
        html_content: HTML content string (full HTML document)
        from_address: Sender address (optional, uses credentials default)
        creds: Credentials dict (optional, loads from default location)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    # Load credentials if not provided
    if creds is None:
        creds = load_credentials()
    
    # Validate recipient address
    if not validate_email_address(to_address):
        print(f"Error: Invalid email address: {to_address}", file=sys.stderr)
        return False
    
    # Set up message
    from_address = from_address or creds['username']
    
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    
    # Attach HTML content
    msg.attach(MIMEText(html_content, 'html'))
    
    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(creds['username'], creds['app_password'])
        server.sendmail(from_address, to_address, msg.as_string())
        server.quit()
        print(f"✓ HTML email sent to {to_address}")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"✗ Authentication failed: {e}", file=sys.stderr)
        print("💡 Check your app password is correct and 2FA is enabled", file=sys.stderr)
        return False
    except smtplib.SMTPRecipientsRefused as e:
        print(f"✗ Recipient refused: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"✗ Error sending HTML email to {to_address}: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Send HTML email via Gmail SMTP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python send_html_email.py recipient@example.com "Test" < body.html
    python send_html_email.py --to recipient@example.com --subject "Test"
    python send_html_email.py --to recipient@example.com --subject "Test" --html "<html>..."
        """
    )
    
    parser.add_argument("to_email", nargs='?', help="Recipient email address")
    parser.add_argument("subject", nargs='?', help="Email subject")
    parser.add_argument("--to", help="Recipient email address (alternative)")
    parser.add_argument("--subject", help="Email subject (alternative)")
    parser.add_argument("--html", help="HTML content as string")
    parser.add_argument("--from-file", help="Read HTML from file")
    parser.add_argument("--test", action="store_true", help="Send test email")
    
    args = parser.parse_args()
    
    # Determine recipient and subject
    if args.to:
        to_email = args.to
    elif args.to_email:
        to_email = args.to_email
    else:
        parser.error("Must provide --to or <to_email> argument")
    
    if args.subject:
        subject = args.subject
    elif args.subject:
        subject = args.subject
    elif args.subject:
        subject = args.subject
    else:
        parser.error("Must provide --subject or <subject> argument")
    
    if args.test:
        html_content = """
        <html>
        <body>
            <h1>Email System Test</h1>
            <p>Email system is working correctly with app password authentication.</p>
        </body>
        </html>
        """
    elif args.html:
        html_content = args.html
    elif args.from_file:
        with open(args.from_file, 'r') as f:
            html_content = f.read()
    else:
        # Read from stdin
        html_content = sys.stdin.read()
    
    success = send_html_email(to_email, subject, html_content)
    sys.exit(0 if success else 1)
