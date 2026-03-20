#!/usr/bin/env python3
"""
Delete emails from Gmail.

This module provides functions for deleting emails using IMAP.
It supports deleting single or multiple emails based on search queries.

_usage:_
    python delete_emails.py --query "FROM 'spam@example.com'"
    python delete_emails.py --query "OLDER_THAN 30"

_examples:_
    # Delete all emails from a sender
    python delete_emails.py --query 'FROM "spam@example.com"'
    
    # Delete old emails (older than 30 days)
    python delete_emails.py --query "OLDER_THAN 30"
    
    # Delete unread emails
    python delete_emails.py --query "UNSEEN"
"""

import imaplib
import argparse
import sys
from typing import Optional, List

from .utils import load_credentials


def delete_emails(
    query: str,
    folder: str = "inbox",
    creds: Optional[dict] = None
) -> int:
    """
    Delete emails matching the query.
    
    Args:
        query: IMAP search query (e.g., 'FROM "example.com"', 'OLDER_THAN 30')
        folder: Mailbox folder (default: 'inbox')
        creds: Credentials dict (optional)
    
    Returns:
        int: Number of emails deleted
    """
    if creds is None:
        creds = load_credentials()
    
    emails_deleted = 0
    
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(creds['username'], creds['app_password'])
        mail.select(folder)
        
        # Search for emails matching query
        status, data = mail.search(None, query)
        
        if status != 'OK':
            print("No emails found matching query.", file=sys.stderr)
            mail.logout()
            return 0
        
        email_ids = data[0].split()
        
        if not email_ids:
            print("No emails found.")
            mail.logout()
            return 0
        
        print(f"Found {len(email_ids)} email(s) to delete")
        
        # Delete each email
        for num in email_ids:
            # Mark as deleted
            mail.store(num, '+FLAGS', '\\Deleted')
            emails_deleted += 1
            print(f"✓ Marked email {num} as deleted")
        
        # Permanently remove deleted emails (expunge)
        mail.expunge()
        
        mail.close()
        mail.logout()
        
        print(f"\n✓ Successfully deleted {emails_deleted} email(s)")
        return emails_deleted
        
    except imaplib.IMAP4.error as e:
        print(f"IMAP error: {e}", file=sys.stderr)
        return 0
    except Exception as e:
        print(f"Error deleting emails: {e}", file=sys.stderr)
        return 0


def delete_all_emails(
    folder: str = "inbox",
    creds: Optional[dict] = None
) -> int:
    """
    Delete ALL emails in a folder (use with caution!).
    
    Args:
        folder: Mailbox folder (default: 'inbox')
        creds: Credentials dict (optional)
    
    Returns:
        int: Number of emails deleted
    """
    if creds is None:
        creds = load_credentials()
    
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(creds['username'], creds['app_password'])
        mail.select(folder)
        
        # Search for all emails
        status, data = mail.search(None, 'ALL')
        
        if status != 'OK':
            print("No emails found.", file=sys.stderr)
            mail.logout()
            return 0
        
        email_ids = data[0].split()
        
        if not email_ids:
            print("No emails to delete.")
            mail.logout()
            return 0
        
        print(f"Found {len(email_ids)} email(s) to delete")
        
        # Delete each email
        for num in email_ids:
            mail.store(num, '+FLAGS', '\\Deleted')
        
        # Permanently remove
        mail.expunge()
        
        mail.close()
        mail.logout()
        
        print(f"\n✓ Successfully deleted {len(email_ids)} email(s)")
        return len(email_ids)
        
    except Exception as e:
        print(f"Error deleting emails: {e}", file=sys.stderr)
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Delete emails from Gmail via IMAP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Delete all emails from a sender
    python delete_emails.py --query 'FROM "spam@example.com"'
    
    # Delete old emails (older than 30 days)
    python delete_emails.py --query "OLDER_THAN 30"
    
    # Delete emails with specific subject
    python delete_emails.py --query 'SUBJECT "Newsletter"'
    
    # Delete unread emails
    python delete_emails.py --query "UNSEEN"
        """
    )
    
    parser.add_argument("--query", required=True, help="IMAP search query")
    parser.add_argument("--folder", default="inbox", help="Mailbox folder (default: inbox)")
    parser.add_argument("--all", action="store_true", help="Delete ALL emails (DANGEROUS!)")
    
    args = parser.parse_args()
    
    if args.all:
        print("⚠️  WARNING: This will delete ALL emails in the folder!")
        confirm = input("Type 'DELETE' to confirm: ")
        
        if confirm != "DELETE":
            print("Cancelled.")
            sys.exit(1)
        
        deleted = delete_all_emails(folder=args.folder)
    else:
        deleted = delete_emails(query=args.query, folder=args.folder)
    
    sys.exit(0 if deleted >= 0 else 1)
