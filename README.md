# 📧 Gmail Mail Merger

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Gmail API](https://img.shields.io/badge/Gmail%20API-v1-red.svg)](https://developers.google.com/gmail/api)

> A powerful, professional mail merge tool for Gmail with HTML formatting support

Send personalized emails to hundreds of recipients using your Gmail drafts. Perfect for outreach campaigns, newsletters, and professional communication while maintaining a personal touch.

![Demo](https://via.placeholder.com/800x400/4A90E2/FFFFFF?text=Gmail+Mail+Merger+Demo)

## ✨ Features

- 🎨 **HTML Email Support** - Preserves formatting, signatures, links, and styling from Gmail drafts
- 📊 **Excel & CSV Support** - Import recipients from .xlsx or .csv files
- 🎯 **Smart Personalization** - Template variables with automatic fallback (e.g., "Sir/Ma'am" for missing names)
- ⏱️ **Rate Limiting** - Built-in 2-second delays to respect Gmail quotas
- 🛡️ **Safety Features** - Preview mode, confirmation prompts, and failure tracking
- 📈 **Progress Tracking** - Real-time logs saved to CSV with timestamps
- 🔒 **Secure** - OAuth2 authentication with local token storage

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/[YOUR_USERNAME]/gmail-mail-merger.git
cd gmail-mail-merger

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **Gmail API** (APIs & Services → Library)
4. Create **OAuth 2.0 credentials**:
   - Type: Desktop application
   - Download JSON → rename to `credentials.json`
   - Place in project root

### 3. Prepare Your Data

Create `data/recipients.xlsx` (or `.csv`):

| email | company_name | employee_name |
|-------|-------------|---------------|
| john@company.com | Acme Corp | John Doe |
| jane@startup.io | Tech Inc | Jane Smith |
| info@business.com | Business LLC | *(empty)* |

*Empty `employee_name` will automatically use "Sir/Ma'am"*

### 4. Create Gmail Draft

Compose in Gmail with placeholders:

```
Subject: Partnership Opportunity with {{company_name}}

Hi {{employee_name}},

I noticed {{company_name}} is doing amazing work in the industry...

Best regards,
[Your Signature]
```

**Available placeholders:**
- `{{email}}` - Recipient's email address
- `{{company_name}}` or `{{company}}` - Company name
- `{{employee_name}}` or `{{name}}` - Employee name

Save as **draft** (don't send yet!)

### 5. Run

```bash
# Option 1: Using the run script
./run.sh

# Option 2: Using Python module
python -m gmail_mail_merger.main

# Option 3: After pip install
gmail-mail-merger
```

**Workflow:**
1. Authenticate with Gmail (browser opens)
2. Select your draft from the list
3. Preview first 3 personalized emails
4. Confirm to send
5. Track progress in `data/sent_log.csv`

## 📊 Gmail API Limits

| Account Type | Daily Limit | Rate |
|--------------|-------------|------|
| Gmail (Personal) | ~100-500 emails/day | 2s delay between sends |
| Google Workspace | Higher limits | Configurable |

The script automatically enforces a 2-second delay between emails to prevent rate limiting.

## 🏗️ Project Structure

```
gmail-mail-merger/
├── src/                    # Source code
│   ├── __init__.py
│   ├── main.py            # Entry point
│   ├── auth.py            # Gmail OAuth2
│   ├── drafts.py          # Draft management
│   ├── recipients.py      # Excel/CSV parsing
│   ├── merger.py          # Template processing
│   ├── sender.py          # Email sending
│   ├── tracker.py         # Logging
│   ├── config.py          # Configuration
│   └── data/              # Data files (gitignored)
│       ├── .gitkeep
│       └── recipients_example.csv
├── docs/                   # Documentation
│   ├── DESIGN.md          # Architecture docs
│   └── EXAMPLES.md        # Usage examples
├── tests/                  # Test suite
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
└── run.sh                 # Quick start script
```

See [DESIGN.md](docs/DESIGN.md) for detailed architecture documentation.

## 🔒 Security

- **Never commit `credentials.json` or `token.json`** - They are in `.gitignore`
- OAuth tokens are stored locally and refreshed automatically
- Emails are sent individually (not BCC) to appear personal
- No data leaves your local machine except through Gmail API

## ⚙️ Configuration

Edit `gmail_mail_merger/config.py` to customize:

```python
DELAY_BETWEEN_EMAILS = 2      # Seconds between sends
MAX_CONSECUTIVE_FAILURES = 2  # Stop after N failures
```

## 📝 Examples

See [docs/EXAMPLES.md](docs/EXAMPLES.md) for:
- Advanced template examples
- Bulk recipient management
- Error handling scenarios
- Best practices

## 🐛 Troubleshooting

**"credentials.json not found"**
- Download OAuth credentials from Google Cloud Console
- Rename to `credentials.json` and place in project root

**"No drafts found"**
- Ensure you have saved drafts in Gmail (not sent)
- Check you're using the correct Gmail account

**"Rate limit exceeded"**
- Gmail has daily sending limits
- Wait 24 hours or upgrade to Google Workspace

**"NaN in email"**
- Fixed! Empty names now automatically use "Sir/Ma'am"

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [Yet Another Mail Merge (YAMM)](https://yamm.com)
- Built with [Google Gmail API](https://developers.google.com/gmail/api)
- Powered by Python 🐍

---

<p align="center">Made with ❤️ for efficient email outreach</p>
