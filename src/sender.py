import base64
import time
import uuid
from email.mime.text import MIMEText
from email.utils import formatdate
from datetime import datetime
from .config import DELAY_BETWEEN_EMAILS, MAX_CONSECUTIVE_FAILURES
from .merger import personalize_content
from .tracker import log_sent_email

def create_message(sender, to, subject, body):
    """Create email message - always use HTML to preserve formatting."""
    # Always send as HTML to preserve formatting from draft
    message = MIMEText(body, 'html')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    message['Date'] = formatdate(localtime=True)
    message['Message-Id'] = f"<{uuid.uuid4()}@{sender.split('@')[1]}>"
    message['MIME-Version'] = '1.0'
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_emails(service, template_subject, template_body, recipients, sender_email):
    """Send personalized emails to all recipients with rate limiting."""
    total = len(recipients)
    sent_count = 0
    failed_count = 0
    consecutive_failures = 0
    
    print(f"\n{'='*60}")
    print(f"Starting to send {total} emails...")
    print(f"Delay between emails: {DELAY_BETWEEN_EMAILS} seconds")
    print(f"{'='*60}\n")
    
    for i, recipient in enumerate(recipients, 1):
        email = recipient['email']
        company = recipient.get('company_name', 'Unknown')
        
        try:
            # Personalize content
            subject = personalize_content(template_subject, recipient)
            body = personalize_content(template_body, recipient)
            
            # Create and send message
            message = create_message(sender_email, email, subject, body)
            service.users().messages().send(userId='me', body=message).execute()
            
            # Log success
            log_sent_email(email, company, 'SUCCESS')
            sent_count += 1
            consecutive_failures = 0
            
            print(f"✓ [{i}/{total}] Sent to: {email} ({company})")
            
        except Exception as e:
            failed_count += 1
            consecutive_failures += 1
            
            # Log failure
            log_sent_email(email, company, f'FAILED: {str(e)}')
            
            print(f"✗ [{i}/{total}] Failed to: {email} ({company})")
            print(f"  Error: {str(e)}")
            
            # Stop if 2 consecutive failures
            if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                print(f"\n{'!'*60}")
                print(f"STOPPED: {MAX_CONSECUTIVE_FAILURES} consecutive failures occurred.")
                print(f"Successfully sent: {sent_count}")
                print(f"Remaining: {total - i}")
                print(f"{'!'*60}")
                return sent_count, failed_count
        
        # Delay between emails (except for the last one)
        if i < total:
            time.sleep(DELAY_BETWEEN_EMAILS)
    
    print(f"\n{'='*60}")
    print(f"COMPLETED!")
    print(f"Total sent: {sent_count}")
    print(f"Total failed: {failed_count}")
    print(f"{'='*60}\n")
    
    return sent_count, failed_count
