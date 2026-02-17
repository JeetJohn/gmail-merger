import base64
from email.mime.text import MIMEText

def list_drafts(service):
    """List all Gmail drafts and return them."""
    results = service.users().drafts().list(userId='me').execute()
    drafts = results.get('drafts', [])
    
    if not drafts:
        raise ValueError("No drafts found in your Gmail account.")
    
    draft_details = []
    for draft in drafts:
        draft_data = service.users().drafts().get(userId='me', id=draft['id']).execute()
        message = draft_data['message']
        headers = {h['name']: h['value'] for h in message['payload']['headers']}
        
        draft_details.append({
            'id': draft['id'],
            'message_id': message['id'],
            'subject': headers.get('Subject', '(No Subject)'),
            'snippet': message.get('snippet', '')[:100]
        })
    
    return draft_details

def get_draft_content(service, draft_id):
    """Get the full content of a specific draft."""
    draft_data = service.users().drafts().get(userId='me', id=draft_id).execute()
    message = draft_data['message']
    
    headers = {h['name']: h['value'] for h in message['payload']['headers']}
    
    # Get body content - prioritize HTML to preserve formatting
    body = ""
    body_html = None
    body_plain = None
    
    if 'parts' in message['payload']:
        for part in message['payload']['parts']:
            if part['mimeType'] == 'text/html':
                body_html = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
            elif part['mimeType'] == 'text/plain':
                body_plain = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
        # Use HTML if available, otherwise fall back to plain
        body = body_html if body_html else body_plain if body_plain else ""
    elif 'body' in message['payload'] and 'data' in message['payload']['body']:
        body = base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')
        # Check if this is HTML or plain
        if '<html' in body.lower() or '<body' in body.lower() or '<div' in body.lower():
            body_html = body
        else:
            body_plain = body
    
    return {
        'subject': headers.get('Subject', ''),
        'body': body,
        'from': headers.get('From', ''),
        'to': headers.get('To', '')
    }
