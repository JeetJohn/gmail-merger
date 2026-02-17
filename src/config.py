import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"

# Find recipients file (supports .xlsx, .csv, or _example variants)
RECIPIENTS_FILE = None
for filename in ['recipients.xlsx', 'recipients.csv', 'recipients_example.xlsx', 'recipients_example.csv']:
    filepath = DATA_DIR / filename
    if filepath.exists():
        RECIPIENTS_FILE = filepath
        break

SENT_LOG_FILE = DATA_DIR / "sent_log.csv"

DELAY_BETWEEN_EMAILS = 2  # seconds
MAX_CONSECUTIVE_FAILURES = 2

GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
