import csv
import os
from datetime import datetime
from .config import SENT_LOG_FILE

def init_sent_log():
    """Initialize the sent log file if it doesn't exist."""
    if not SENT_LOG_FILE.exists():
        with open(SENT_LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'email', 'company', 'status'])

def log_sent_email(email, company, status):
    """Log a sent email to the CSV file."""
    init_sent_log()
    
    with open(SENT_LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            email,
            company,
            status
        ])

def get_sent_count():
    """Get total number of sent emails from log."""
    if not SENT_LOG_FILE.exists():
        return 0
    
    with open(SENT_LOG_FILE, 'r') as f:
        return sum(1 for line in f) - 1  # Subtract header
