import re

import re

def personalize_content(template, recipient):
    """Replace placeholders with recipient data."""
    content = template
    
    # Get employee_name, use 'Sir/Ma\'am' if empty
    employee_name = recipient.get('employee_name', '')
    if not employee_name or str(employee_name).strip() == '':
        employee_name = "Sir/Ma'am"
    
    # Replace placeholders
    placeholders = {
        '{{email}}': recipient.get('email', ''),
        '{{company_name}}': recipient.get('company_name', ''),
        '{{employee_name}}': employee_name,
        '{{company}}': recipient.get('company_name', ''),  # alias
        '{{name}}': employee_name,     # alias
    }
    
    for placeholder, value in placeholders.items():
        content = content.replace(placeholder, str(value))
    
    return content

def preview_personalization(template_subject, template_body, recipient):
    """Generate preview for a recipient."""
    subject = personalize_content(template_subject, recipient)
    body = personalize_content(template_body, recipient)
    return subject, body
