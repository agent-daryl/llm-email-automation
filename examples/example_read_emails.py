#!/usr/bin/env python3
"""
Example: Reading and processing unread emails.

This example demonstrates how to read unread emails and process them.
"""

import sys
from pathlib import Path

# Add parent directory to path to import local modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.read_emails import read_unread_emails, search_emails
from src.send_email import send_text_email


def process_inbox():
    """
    Read unread emails and process them.
    
    This is a simple example that shows how to:
    1. Read unread emails
    2. Filter by sender or subject
    3. Take action based on email content
    """
    print("Reading unread emails...")
    
    # Read all unread emails
    emails = read_unread_emails(limit=5)
    
    if not emails:
        print("No unread emails found.")
        return
    
    print(f"\nFound {len(emails)} unread email(s):\n")
    
    for i, email in enumerate(emails, 1):
        print(f"--- Email {i} ---")
        print(f"From: {email['from']}")
        print(f"Subject: {email['subject']}")
        print(f"Date: {email['date']}")
        print(f"Body preview: {email['body'][:150]}...")
        print()
    
    # Example: Process emails from a specific sender
    print("\nSearching for emails from 'example.com'...")
    
    example_emails = search_emails(query='FROM "example.com"')
    
    if example_emails:
        print(f"Found {len(example_emails)} email(s) from example.com")
        # Process them as needed
        for email in example_emails:
            print(f"- {email['subject']}")
    else:
        print("No emails from example.com found.")


def auto_respond_to_urgent():
    """
    Example: Auto-reply to urgent emails.
    
    This shows how to detect urgent emails and send an acknowledgment.
    """
    print("Checking for urgent emails...")
    
    # Search for emails with "urgent" in subject
    urgent_emails = search_emails(query='SUBJECT "urgent"')
    
    if not urgent_emails:
        print("No urgent emails found.")
        return
    
    for email in urgent_emails:
        # Send acknowledgment
        sender = email['from'].split('<')[0].strip() if '<' in email['from'] else email['from']
        
        response_body = f"""
        Thank you for your urgent email.
        
        I've received your message about: {email['subject']}
        
        I will get back to you as soon as possible.
        
        Best regards,
        [Your Automated Assistant]
        """
        
        # Note: You'd need to extract the actual sender address
        print(f"Would send acknowledgment to: {sender}")
        print(f"Subject: Re: {email['subject']}")


if __name__ == "__main__":
    # Run the example
    process_inbox()
