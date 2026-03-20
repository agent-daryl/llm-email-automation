#!/usr/bin/env python3
"""
Search emails using Gmail IMAP.

This module provides email search functionality using IMAP queries.

_usage:_
    python search_emails.py --query "FROM 'example.com' --limit 5"
    python search_emails.py --query "UNSEEN"

_examples:_
    python search_emails.py --query 'FROM "boss@example.com"'
    python search_emails.py --query "OLDER_THAN 30"
    python search_emails.py --query 'SUBJECT "meeting"'
"""

import imaplib
import argparse
import sys
from email.header import decode_header
from typing import List, Dict, Optional

from .utils import load_credentials


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
        List of email dictionaries with keys:
        - from, to, subject, body, date, message_id, headers
    """
    if creds is None:
        creds = load_credentials()
    
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(creds['username'], creds['app_password'])
        mail.select(folder)
        
        status, data = mail.search(None, query)
        
        if status != 'OK':
            print("No emails found matching query.", file=sys.stderr)
            mail.logout()
            return []
        
        email_ids = data[0].split()
        
        if not email_ids:
            mail.logout()
            return []
        
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Search emails using IMAP queries",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--query", required=True, help="IMAP search query")
    parser.add_argument("--folder", default="inbox", help="Mailbox folder")
    parser.add_argument("--limit", type=int, default=20, help="Max emails to retrieve")
    
    args = parser.parse_args()
    
    emails = search_emails(args.query, folder=args.folder, limit=args.limit)
    
    if not emails:
        print("No emails found.")
        sys.exit(0)
    
    for i, email in enumerate(emails, 1):
        print(f"\n--- Email {i} ---")
        print(f"From: {email['from']}")
        print(f"Subject: {email['subject']}")
        print(f"Body: {email['body'][:200]}...")
