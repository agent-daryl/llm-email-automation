"""
LLM Email Automation - A Python-based email system for LLM agents.

This package provides utilities for sending, reading, and managing emails
through Gmail accounts.

Features:
- Send text and HTML emails
- Read unread emails
- Search/filter emails
- Delete emails
- Credential management

Usage:
    from llm_email_automation.src.send_email import send_text_email
    send_text_email("to@example.com", "Subject", "Body")

    from llm_email_automation.src.read_emails import read_unread_emails
    emails = read_unread_emails()
"""

__version__ = "1.0.0"
__author__ = "LLM Email Automation Team"
