#!/usr/bin/env python3
"""
Read emails from Gmail inbox.

This module provides functions for reading emails using IMAP.
It supports searching, filtering, and retrieving email content.

_usage:_
    python read_emails.py
    python read_emails.py --query "UNSEEN"
    python read_emails.py --query 'FROM "example.com"'

_examples:_
    # Read all unread emails
    python read_emails.py --query "UNSEEN"
    
    # Read emails from specific sender
    python read_emails.py --query 'FROM "boss@example.com"'
    
    # Read emails since date
    python read_emails.py --query 'SINCE "2024-01-01"'
"""

import imaplib
import email
import argparse
import sys
from email.header import decode_header
from typing import List, Dict, Optional

from .utils import load_credentials, validate_email_address


def decode_mime_header(header):
    """Decode a MIME header value."""
    if header is None:
        return ""
    
    decoded_parts = decode_header(header)
    result = []
    
    for text, encoding in decoded_parts:
        if isinstance(text, bytes):
            if encoding:
                try:
                    result.append(text.decode(encoding, errors='replace'))
                except LookupError:
                    # Unknown encoding, try utf-8
                    result.append(text.decode('utf-8', errors='replace'))
            else:
                result.append(text.decode('utf-8', errors='replace'))
        else:
            result.append(text)
    
    return ''.join(result)


def parse_email_body(msg) -> str:
    """Extract text body from email message."""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            
            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    charset = part.get_content_charset() or 'utf-8'
                    return part.get_payload(decode=True).decode(charset, errors='replace')
                except:
                    return part.get_payload(decode=True).decode('utf-8', errors='replace')
    else:
        try:
            charset = msg.get_content_charset() or 'utf-8'
            return msg.get_payload(decode=True).decode(charset, errors='replace')
        except:
            return msg.get_payload(decode=True).decode('utf-8', errors='replace')
    
    return ""


def read_unread_emails(
    folder: str = "inbox",
    limit: int = 10,
    creds: Optional[dict] = None
) -> List[Dict]:
    """
    Read unread emails from the specified folder.
    
    Args:
        folder: Mailbox folder (default: 'inbox')
        limit: Maximum number of emails to retrieve
        creds: Credentials dict (optional)
    
    Returns:
        List of email dictionaries with keys:
        - from: Sender address
        - subject: Email subject
        - body: Email text body
        - date: Received date
        - message_id: Unique message ID
    """
    if creds is None:
        creds = load_credentials()
    
    try:
        # Connect to IMAP server
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(creds['username'], creds['app_password'])
        
        # Select folder
        mail.select(folder)
        
        # Search for unread emails
        status, data = mail.search(None, 'UNSEEN')
        
        if status != 'OK':
            print("No unread emails found.", file=sys.stderr)
            mail.logout()
            return []
        
        # Get email IDs
        email_ids = data[0].split()
        
        if not email_ids:
            mail.logout()
            return []
        
        # Limit number of emails
        email_ids = email_ids[-limit:]
        
        emails = []
        
        for num in email_ids:
            status, msg_data = mail.fetch(num, '(RFC822)')
            
            if status != 'OK':
                continue
            
            msg = email.message_from_bytes(msg_data[0][1])
            
            email_data = {
                'from': decode_mime_header(msg.get('From')),
                'to': decode_mime_header(msg.get('To')),
                'subject': decode_mime_header(msg.get('Subject')),
                'body': parse_email_body(msg),
                'date': decode_mime_header(msg.get('Date')),
                'message_id': msg.get('Message-ID', ''),
                'headers': dict(msg.items())
            }
            
            emails.append(email_data)
        
        mail.close()
        mail.logout()
        
        return emails
        
    except imaplib.IMAP4.error as e:
        print(f"IMAP error: {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error reading emails: {e}", file=sys.stderr)
        return []


def search_emails(
    query: str,
    folder: str = "inbox",
    limit: int = 20,
    creds: Optional[dict] = None
) -> List[Dict]:
    """
    Search emails using IMAP query syntax.
    
    Args:
        query: IMAP search query (e.g., 'FROM "example.com"', 'UNSEEN')
        folder: Mailbox folder (default: 'inbox')
        limit: Maximum number of emails to retrieve
        creds: Credentials dict (optional)
    
    Returns:
        List of email dictionaries (same format as read_unread_emails)
    """
    if creds is None:
        creds = load_credentials()
    
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(creds['username'], creds['app_password'])
        mail.select(folder)
        
        # Search with query
        status, data = mail.search(None, query)
        
        if status != 'OK':
            print("No emails found matching query.", file=sys.stderr)
            mail.logout()
            return []
        
        email_ids = data[0].split()
        
        if not email_ids:
            mail.logout()
            return []
        
        # Limit number of emails
        email_ids = email_ids[-limit:]
        
        emails = []
        
        for num in email_ids:
            status, msg_data = mail.fetch(num, '(RFC822)')
            
            if status != 'OK':
                continue
            
            msg = email.message_from_bytes(msg_data[0][1])
            
            email_data = {
                'from': decode_mime_header(msg.get('From')),
                'to': decode_mime_header(msg.get('To')),
                'subject': decode_mime_header(msg.get('Subject')),
                'body': parse_email_body(msg),
                'date': decode_mime_header(msg.get('Date')),
                'message_id': msg.get('Message-ID', ''),
                'headers': dict(msg.items())
            }
            
            emails.append(email_data)
        
        mail.close()
        mail.logout()
        
        return emails
        
    except imaplib.IMAP4.error as e:
        print(f"IMAP error: {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error searching emails: {e}", file=sys.stderr)
        return []


def get_email_count(folder: str = "inbox", creds: Optional[dict] = None) -> int:
    """Get total email count in folder."""
    if creds is None:
        creds = load_credentials()
    
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(creds['username'], creds['app_password'])
        status, data = mail.select(folder)
        
        if status != 'OK':
            return 0
        
        count = int(data[0])
        mail.close()
        mail.logout()
        
        return count
        
    except:
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Read emails from Gmail inbox via IMAP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Read all unread emails
    python read_emails.py
    
    # Read unread emails with limit
    python read_emails.py --limit 5
    
    # Search for emails from specific sender
    python read_emails.py --query 'FROM "example.com"'
    
    # Search for unread emails
    python read_emails.py --query "UNSEEN"
    
    # Search for emails since date
    python read_emails.py --query 'SINCE "2024-01-01"'
    python read_emails.py --query 'BEFORE "2024-12-31"'
        """
    )
    
    parser.add_argument("--query", default="UNSEEN", help="IMAP search query (default: UNSEEN)")
    parser.add_argument("--folder", default="inbox", help="Mailbox folder (default: inbox)")
    parser.add_argument("--limit", type=int, default=10, help="Maximum emails to retrieve")
    
    args = parser.parse_args()
    
    if args.query == "UNSEEN":
        emails = read_unread_emails(folder=args.folder, limit=args.limit)
    else:
        emails = search_emails(args.query, folder=args.folder, limit=args.limit)
    
    if not emails:
        print("No emails found.")
        sys.exit(0)
    
    for i, email in enumerate(emails, 1):
        print(f"\n--- Email {i} ---")
        print(f"From: {email['from']}")
        print(f"Subject: {email['subject']}")
        print(f"Date: {email['date']}")
        print("-" * 60)
        print(f"Body preview: {email['body'][:200]}...")
    
    print(f"\nTotal: {len(emails)} email(s)")
