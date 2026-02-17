#!/usr/bin/env python3
"""
Gmail Mail Merger - Professional mail merge tool
A powerful, Gmail-based mail merge solution with HTML formatting support
"""

import sys
from .auth import get_gmail_service
from .drafts import list_drafts, get_draft_content
from .recipients import load_recipients
from .merger import preview_personalization
from .sender import send_emails
from .tracker import init_sent_log

def print_header():
    print("\n" + "="*60)
    print("  MASS MAILER - Gmail Mail Merge Tool")
    print("="*60 + "\n")

def select_draft(drafts):
    """Display drafts and let user select one."""
    print("Available Gmail Drafts:")
    print("-" * 60)
    
    for i, draft in enumerate(drafts, 1):
        print(f"{i}. {draft['subject']}")
        print(f"   Preview: {draft['snippet']}...")
        print()
    
    while True:
        try:
            choice = input(f"Select draft (1-{len(drafts)}): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(drafts):
                return drafts[idx]
            else:
                print(f"Please enter a number between 1 and {len(drafts)}")
        except ValueError:
            print("Please enter a valid number")

def show_preview(template_subject, template_body, recipients, count=3):
    """Show preview of first N personalized emails."""
    print("\n" + "="*60)
    print("PREVIEW MODE - Showing first 3 personalized emails:")
    print("="*60)
    
    for i, recipient in enumerate(recipients[:count], 1):
        subject, body = preview_personalization(template_subject, template_body, recipient)
        
        print(f"\n--- Email {i} ---")
        print(f"To: {recipient['email']}")
        print(f"Company: {recipient.get('company_name', 'N/A')}")
        print(f"Employee: {recipient.get('employee_name', 'N/A')}")
        print(f"Subject: {subject}")
        print(f"Body Preview: {body[:200]}...")
        print("-" * 40)

def confirm_send():
    """Ask user to confirm before sending."""
    print("\n" + "="*60)
    response = input("Do you want to proceed with sending? (yes/no): ").strip().lower()
    return response in ['yes', 'y']

def main():
    print_header()
    
    try:
        # Step 1: Authenticate with Gmail
        print("Authenticating with Gmail...")
        service = get_gmail_service()
        print("✓ Authentication successful!\n")
        
        # Get sender email
        profile = service.users().getProfile(userId='me').execute()
        sender_email = profile['emailAddress']
        print(f"Sending from: {sender_email}\n")
        
        # Step 2: List and select draft
        print("Fetching drafts from Gmail...")
        drafts = list_drafts(service)
        selected_draft = select_draft(drafts)
        print(f"\n✓ Selected: {selected_draft['subject']}\n")
        
        # Step 3: Get draft content
        draft_content = get_draft_content(service, selected_draft['id'])
        template_subject = draft_content['subject']
        template_body = draft_content['body']
        
        # Step 4: Load recipients
        print("Loading recipients from Excel...")
        recipients = load_recipients()
        print(f"✓ Loaded {len(recipients)} recipients\n")
        
        # Step 5: Show preview
        show_preview(template_subject, template_body, recipients)
        
        # Step 6: Confirm and send
        if confirm_send():
            # Initialize log
            init_sent_log()
            
            # Send emails
            send_emails(service, template_subject, template_body, recipients, sender_email)
            
            print(f"\n✓ Sent log saved to: data/sent_log.csv")
        else:
            print("\n✗ Sending cancelled by user.")
            
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print("\nSetup Instructions:")
        print("1. Download credentials.json from Google Cloud Console")
        print("2. Place it in the mass_mailer/ directory")
        print("3. Create data/recipients.xlsx with columns: email, company_name, employee_name")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
