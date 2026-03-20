#!/usr/bin/env python3
"""
Credential utility module for LLM Email Automation.

This module provides helper functions for loading email credentials.
It is designed to be importable by other modules in the system.
"""

import os
import sys


def load_credentials(creds_file_path=None):
    """
    Load email credentials from a file.
    
    Args:
        creds_file_path (str): Path to credentials file. 
                             Defaults to 'email_creds.txt' in current directory.
    
    Returns:
        dict: Dictionary with keys 'username', 'password', 'app_password'
    
    Raises:
        FileNotFoundError: If credentials file not found
        ValueError: If credentials file format is invalid
    """
    if creds_file_path is None:
        # Look for credentials in multiple locations
        possible_paths = [
            'email_creds.txt',
            os.path.join(os.path.dirname(__file__), '..', 'email_creds.txt'),
            os.path.expanduser('~/.email_creds.txt'),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                creds_file_path = path
                break
        else:
            raise FileNotFoundError(
                "email_creds.txt not found. Please create credentials file.\n"
                "See README.md for formatting instructions."
            )
    
    if not os.path.exists(creds_file_path):
        raise FileNotFoundError(f"Credentials file not found: {creds_file_path}")
    
    credentials = {}
    
    try:
        with open(creds_file_path, 'r') as f:
            lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower()
                    value = value.strip()
                    
                    if key == 'username':
                        credentials['username'] = value
                    elif key == 'password':
                        credentials['password'] = value
                    elif key == 'app_password':
                        credentials['app_password'] = value
            
            # Validate required fields
            required_fields = ['username', 'app_password']
            missing = [f for f in required_fields if f not in credentials]
            
            if missing:
                raise ValueError(
                    f"Missing required credentials: {', '.join(missing)}\n"
                    f"See README.md for credentials file format."
                )
            
            return credentials
            
    except Exception as e:
        raise ValueError(f"Error reading credentials file: {e}")


def validate_email_address(email):
    """
    Validate that an email address has the basic structure.
    
    Args:
        email (str): Email address to validate
    
    Returns:
        bool: True if valid format, False otherwise
    """
    import re
    
    # Simple regex for basic email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


# Example usage
if __name__ == "__main__":
    try:
        creds = load_credentials()
        print("Credentials loaded successfully!")
        print(f"Username: {creds['username']}")
        print(f"App Password: {'*' * len(creds['app_password'])}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
