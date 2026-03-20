# LLM Email Automation - Source modules
"""
Email modules for LLM automation.
"""

from .send_email import send_text_email
from .send_html_email import send_html_email
from .read_emails import read_unread_emails, search_emails
from .delete_emails import delete_emails
from .utils import load_credentials, validate_email_address

__all__ = [
    'send_text_email',
    'send_html_email',
    'read_unread_emails',
    'search_emails',
    'delete_emails',
    'load_credentials',
    'validate_email_address',
]
