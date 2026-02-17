# Design Documentation

## Architecture Overview

Gmail Mail Merger follows a modular, pipeline-based architecture designed for clarity, maintainability, and extensibility.

```
┌─────────────────────────────────────────────────────────────┐
│                        User Input                            │
│  ┌──────────┐  ┌──────────────┐  ┌─────────────────────┐   │
│  │ Draft ID │  │ Recipients   │  │ Gmail Credentials   │   │
│  └────┬─────┘  └──────┬───────┘  └──────────┬──────────┘   │
└───────┼───────────────┼────────────────────┼──────────────┘
        │               │                    │
        ▼               ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                    Gmail Mail Merger                         │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Auth       │───▶│   Drafts     │───▶│  Recipients  │  │
│  │  (OAuth2)    │    │  (Fetcher)   │    │   (Parser)   │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                   │                   │           │
│         └───────────────────┴───────────────────┘           │
│                             │                               │
│                             ▼                               │
│                   ┌──────────────────┐                     │
│                   │     Merger       │                     │
│                   │ (Personalization)│                     │
│                   └────────┬─────────┘                     │
│                            │                               │
│                            ▼                               │
│                   ┌──────────────────┐                     │
│                   │     Sender       │                     │
│                   │ (Rate Limited)   │                     │
│                   └────────┬─────────┘                     │
│                            │                               │
│                            ▼                               │
│                   ┌──────────────────┐                     │
│                   │     Tracker      │                     │
│                   │ (Logging)        │                     │
│                   └──────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│                      Gmail API                               │
│                   (Email Delivery)                           │
└─────────────────────────────────────────────────────────────┘
```

## Module Responsibilities

### 1. `auth.py` - Authentication Module
**Purpose:** Handle OAuth2 authentication with Gmail API

**Key Functions:**
- `get_gmail_service()` - Authenticate and return Gmail API service instance
- Token refresh on expiration
- Local token storage in `token.json`

**Security:**
- Credentials never stored in code
- Tokens refreshed automatically
- Scope limited to `gmail.modify` (minimum required permissions)

### 2. `drafts.py` - Draft Management
**Purpose:** Fetch and parse Gmail drafts

**Key Functions:**
- `list_drafts()` - Retrieve all user drafts with metadata
- `get_draft_content()` - Extract HTML content preserving formatting

**Design Decisions:**
- Prioritizes HTML over plain text to maintain formatting
- Extracts subject, body, from, and to headers
- Handles multipart MIME structures

### 3. `recipients.py` - Data Parser
**Purpose:** Load and validate recipient data

**Key Functions:**
- `load_recipients()` - Parse Excel (.xlsx) and CSV files
- Validates required columns (email, company_name)
- Handles missing optional columns (employee_name)

**Data Flow:**
```
recipients.xlsx ──▶ pandas ──▶ validation ──▶ list of dicts
```

**Error Handling:**
- Missing file → FileNotFoundError with helpful message
- Missing columns → ValueError with specific column names
- Empty cells → Converted to empty strings (not NaN)

### 4. `merger.py` - Template Engine
**Purpose:** Personalize email templates with recipient data

**Key Functions:**
- `personalize_content()` - Replace placeholders with actual values
- `preview_personalization()` - Generate preview for validation

**Placeholder System:**
- `{{email}}` - Recipient email
- `{{company_name}}` / `{{company}}` - Company name
- `{{employee_name}}` / `{{name}}` - Employee name (fallback: "Sir/Ma'am")

**Smart Fallbacks:**
```python
employee_name = recipient.get('employee_name', '')
if not employee_name:
    employee_name = "Sir/Ma'am"  # Professional fallback
```

### 5. `sender.py` - Email Dispatcher
**Purpose:** Send emails with rate limiting and error handling

**Key Functions:**
- `create_message()` - Build MIME message with HTML support
- `send_emails()` - Main sending loop with controls

**Rate Limiting:**
- Configurable delay between sends (default: 2 seconds)
- Prevents Gmail API rate limit violations
- Progress tracking with visual feedback

**Safety Features:**
- Consecutive failure threshold (default: 2)
- Automatic stop on repeated failures
- Individual error logging per recipient

### 6. `tracker.py` - Logging Module
**Purpose:** Track sent emails and status

**Key Functions:**
- `log_sent_email()` - Append to CSV log
- `init_sent_log()` - Create log file with headers

**Log Format:**
```csv
timestamp,email,company,status
2026-02-17 14:30:00,john@company.com,Acme Corp,SUCCESS
2026-02-17 14:30:02,jane@startup.io,Tech Inc,FAILED: Rate limit
```

### 7. `config.py` - Configuration
**Purpose:** Centralize all settings and paths

**Key Settings:**
- File paths (credentials, data, logs)
- Rate limiting parameters
- Gmail API scopes
- Recipient file discovery (multiple format support)

### 8. `main.py` - Orchestrator
**Purpose:** Main entry point and user interface

**Workflow:**
1. Display header and authenticate
2. List and select Gmail draft
3. Load and validate recipients
4. Show preview (first 3 emails)
5. Confirm before sending
6. Execute sending with progress
7. Display completion summary

**User Experience:**
- Clear visual separators
- Progress indicators
- Confirmation prompts
- Error messages with context

## Data Flow

```
1. Authentication
   └─▶ OAuth2 flow → token.json (cached)

2. Draft Selection
   └─▶ Gmail API → list of drafts
   └─▶ User selects by number
   └─▶ Fetch full content (HTML preserved)

3. Recipient Loading
   └─▶ Discover file (.xlsx/.csv)
   └─▶ Parse with pandas
   └─▶ Validate columns
   └─▶ Return list[dict]

4. Personalization
   └─▶ For each recipient:
       └─▶ Replace placeholders
       └─▶ Apply fallback logic
       └─▶ Return personalized content

5. Sending
   └─▶ For each recipient:
       └─▶ Create MIME message (HTML)
       └─▶ Send via Gmail API
       └─▶ Log result
       └─▶ Delay N seconds
       └─▶ Check failure threshold

6. Completion
   └─▶ Display summary
   └─▶ Log file location
```

## Security Considerations

### 1. Credential Management
- `credentials.json` - OAuth client secrets (NEVER commit)
- `token.json` - OAuth access tokens (auto-generated, NEVER commit)
- Both files in `.gitignore`

### 2. Data Privacy
- All processing happens locally
- No data sent to third parties except Gmail API
- Recipient data stays on user's machine

### 3. API Security
- Minimum required scopes (`gmail.modify`)
- Token refresh on expiration
- Local authentication only

### 4. Email Privacy
- Individual sends (not BCC)
- No mass-mail detection by recipients
- Personal touch maintained

## Error Handling Strategy

### Levels of Error Handling

1. **Input Validation** (Early fail)
   - Missing files
   - Invalid columns
   - Empty recipient lists

2. **Runtime Errors** (Graceful degradation)
   - API failures → Log and continue
   - Rate limits → Wait and retry
   - Network issues → Stop after threshold

3. **User Feedback** (Clear messaging)
   - File not found → Setup instructions
   - Authentication failed → OAuth guide
   - Rate limit → Wait time information

### Failure Recovery

```python
consecutive_failures = 0
MAX_FAILURES = 2  # Configurable

for recipient in recipients:
    try:
        send_email(recipient)
        consecutive_failures = 0  # Reset on success
    except Exception as e:
        log_failure(recipient, e)
        consecutive_failures += 1
        
        if consecutive_failures >= MAX_FAILURES:
            stop_and_report()  # Prevent spamming errors
```

## Extensibility Points

### Adding New Placeholders

1. Update `merger.py`:
```python
placeholders = {
    # ... existing placeholders
    '{{custom_field}}': recipient.get('custom_field', ''),
}
```

2. Add column to Excel/CSV

### Adding Attachments

1. Modify `sender.py`:
```python
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

# Create multipart message
msg = MIMEMultipart()
msg.attach(MIMEText(body, 'html'))

# Add attachment
part = MIMEBase('application', 'octet-stream')
part.set_payload(open(filename, 'rb').read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', f'attachment; filename={filename}')
msg.attach(part)
```

### Supporting Different Email Providers

Create abstraction layer:
```python
class EmailProvider(ABC):
    @abstractmethod
    def authenticate(self): pass
    
    @abstractmethod
    def send(self, message): pass

class GmailProvider(EmailProvider): ...
class OutlookProvider(EmailProvider): ...
```

## Performance Considerations

### Memory Usage
- Recipients loaded as list of dicts (not DataFrame)
- One email processed at a time
- Minimal memory footprint

### API Efficiency
- Batch operations where possible
- Connection reuse via service object
- Token caching to avoid re-auth

### Rate Limiting
- 2-second default delay
- Configurable based on account type
- Respects Gmail API quotas

## Testing Strategy

### Unit Tests (Future Enhancement)
```python
def test_personalize_content():
    template = "Hi {{name}}"
    recipient = {'employee_name': 'John'}
    result = personalize_content(template, recipient)
    assert result == "Hi John"

def test_empty_name_fallback():
    template = "Hi {{name}}"
    recipient = {'employee_name': ''}
    result = personalize_content(template, recipient)
    assert result == "Hi Sir/Ma'am"
```

### Integration Tests
- OAuth flow (mock)
- Gmail API calls (mock)
- End-to-end with test account

## Deployment Considerations

### Local Development
- Virtual environment recommended
- Local credential files
- Test with small recipient list

### Production Use
- Google Workspace for higher limits
- Dedicated sending account
- Monitor sent_log.csv
- Regular token refresh

### Distribution
- PyPI package (setup.py included)
- GitHub releases
- Docker image (optional)

## Future Enhancements

1. **Scheduling** - Delayed sends via cron/APScheduler
2. **Templates** - Multiple draft templates
3. **Tracking** - Open/click tracking (via tracking pixels)
4. **Unsubscribe** - Automated unsubscribe handling
5. **Attachments** - File attachment support
6. **CC/BCC** - Support for carbon copy
7. **Reply-to** - Custom reply-to addresses
8. **HTML Editor** - WYSIWYG template editor

## Conclusion

Gmail Mail Merger is designed with:
- ✅ **Modularity** - Easy to understand and extend
- ✅ **Safety** - Multiple layers of protection
- ✅ **User Experience** - Clear feedback and guidance
- ✅ **Professionalism** - Enterprise-ready features

The architecture separates concerns clearly, making it easy to maintain, test, and extend for future requirements.
