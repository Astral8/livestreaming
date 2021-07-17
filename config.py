"""
File meant for holding Environment Variables.
Specifically for Google Authentication Secret Variables.
"""
import os

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
