#!/usr/bin/env python3
"""
Send text emails using Gmail SMTP.

This module provides functions for sending plain text emails through Gmail's SMTP server.
It uses app password authentication for security.

_usage:_
    python send_email.py --to <email> --subject <subject> --body <content>
    python send_email.py --to <email> --from-file <filepath>
    python send_email.py --test

_examples:_
    # Send a simple text email
    python send_email.py --to recipient@example.com --subject "Test" --body "Hello"
    
    # Send from file
    python send_email.py --to recipient@example.com --subject "Report" --from-file report.txt
    
    # Test email
    python send_email.py --test
"""

import smtplib
import argparse
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional, List

from .utils import load_credentials, validate_email_address


def create_email(
    to_address: str,
    subject: str,
    body: str,
    from_address: Optional[str] = None,
    attachments: Optional[List[str]] = None,
    creds: Optional[dict] = None
) -> bool:
    """
    Create and send a text email.
    
    Args:
        to_address: Recipient email address
        subject: Email subject line
        body: Email body text
        from_address: Sender address (optional, uses credentials default)
        attachments: List of file paths to attach (optional)
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
    
    # Attach body
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach files if provided
    if attachments:
        for filepath in attachments:
            try:
                with open(filepath, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename="{filepath.split("/")[-1]}"'
                    )
                    msg.attach(part)
            except Exception as e:
                print(f"Warning: Could not attach {filepath}: {e}", file=sys.stderr)
    
    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(creds['username'], creds['app_password'])
        server.sendmail(from_address, to_address, msg.as_string())
        server.quit()
        print(f"✓ Email sent to {to_address}")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"✗ Authentication failed: {e}", file=sys.stderr)
        print("💡 Check your app password is correct and 2FA is enabled", file=sys.stderr)
        return False
    except smtplib.SMTPRecipientsRefused as e:
        print(f"✗ Recipient refused: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"✗ Error sending email to {to_address}: {e}", file=sys.stderr)
        return False


# Backward compatibility alias
send_text_email = create_email


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Send text email via Gmail SMTP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python send_email.py --to recipient@example.com --subject "Test" --body "Hello"
    python send_email.py --to recipient@example.com --from-file body.txt --subject "Report"
    python send_email.py --test
        """
    )
    
    parser.add_argument("--to", required=True, help="Recipient email address")
    parser.add_argument("--subject", default="LLM Email Automation", help="Email subject")
    parser.add_argument("--body", help="Email body content")
    parser.add_argument("--from-file", help="Read body from file")
    parser.add_argument("--test", action="store_true", help="Send test email")
    
    args = parser.parse_args()
    
    if args.test:
        success = create_email(
            to_address="daryl.allen.jr@gmail.com",
            subject="Email System Test",
            body="Email system is working correctly with app password authentication."
        )
        sys.exit(0 if success else 1)
    
    if not args.body and not args.from_file:
        parser.error("Must provide --body or --from-file")
    
    body = args.body
    if args.from_file:
        with open(args.from_file, 'r') as f:
            body = f.read()
    
    success = create_email(args.to, args.subject, body)
    sys.exit(0 if success else 1)
