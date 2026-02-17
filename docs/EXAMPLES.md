# Usage Examples

This document provides detailed examples and best practices for using Gmail Mail Merger.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Template Examples](#template-examples)
3. [Recipient Data Formats](#recipient-data-formats)
4. [Advanced Scenarios](#advanced-scenarios)
5. [Best Practices](#best-practices)

---

## Basic Usage

### Example 1: Simple Outreach Campaign

**Goal:** Send internship inquiry to 50 companies

**Step 1: Prepare Recipients**

Create `data/recipients.xlsx`:

| email | company_name | employee_name |
|-------|-------------|---------------|
| hr@techcorp.com | TechCorp |  |
| careers@startup.io | StartupIO | Sarah |
| info@bigcompany.com | BigCompany |  |

**Step 2: Create Gmail Draft**

```
Subject: Internship Opportunity - {{company_name}}

Dear {{employee_name}},

I hope this email finds you well. I am reaching out regarding potential internship opportunities at {{company_name}}.

A bit about me:
• Currently pursuing B.Tech in Computer Science
• Proficient in Python, JavaScript, and cloud technologies
• Previous experience at [Previous Company]

I would love to discuss how I can contribute to {{company_name}}'s mission. Please find my resume attached for your review.

Looking forward to hearing from you.

Best regards,
[Your Name]
[Your Phone]
[LinkedIn Profile]
```

**Step 3: Run**

```bash
python gmail_mail_merger/main.py
```

**Output:**
- Email to hr@techcorp.com: "Dear Sir/Ma'am" (empty name = fallback)
- Email to careers@startup.io: "Dear Sarah"
- Email to info@bigcompany.com: "Dear Sir/Ma'am"

---

## Template Examples

### Example 2: Partnership Proposal with Formatting

**Draft with Rich Formatting:**

```html
Subject: Partnership Opportunity - {{company_name}}

<p>Dear {{employee_name}},</p>

<p>I hope this email finds you well at <strong>{{company_name}}</strong>.</p>

<p>I'm writing to propose a strategic partnership that could benefit both our organizations:</p>

<ul>
  <li><strong>Joint Marketing:</strong> Co-branded campaigns</li>
  <li><strong>Technology Integration:</strong> API partnerships</li>
  <li><strong>Revenue Sharing:</strong> Mutually beneficial model</li>
</ul>

<p>Here are the key benefits:</p>

<ol>
  <li>Increased market reach</li>
  <li>Shared resources and expertise</li>
  <li>Cost optimization</li>
</ol>

<p>Would you be available for a 15-minute call next week?<br>
<a href="https://calendly.com/your-link">Book a time here</a></p>

<p>Best regards,</p>

<p>--<br>
<strong>Your Name</strong><br>
Title | Company<br>
📧 email@company.com<br>
🔗 <a href="https://linkedin.com/in/yourprofile">LinkedIn</a><br>
🌐 <a href="https://yourcompany.com">Website</a></p>
```

**Note:** When composing in Gmail, the formatting is automatic. Just use the rich text editor normally and add placeholders.

---

### Example 3: Newsletter Campaign

**Draft:**

```
Subject: {{company_name}} - Monthly Updates & Insights

Hi {{employee_name}},

Welcome to this month's newsletter! Here are the top stories:

🚀 **Product Updates**
   • New feature released
   • Performance improvements
   • Bug fixes

📊 **Industry Insights**
   • Market trends for {{company_name}}'s sector
   • Competitive analysis
   • Future predictions

🎯 **Action Items**
   1. Review Q1 goals
   2. Update {{company_name}} profile
   3. Schedule quarterly review

Questions? Reply to this email or contact our support team.

Until next month!

The Team
```

---

## Recipient Data Formats

### Format 1: Excel (.xlsx)

**Best for:** Large datasets, multiple sheets, formulas

**File:** `data/recipients.xlsx`

| email | company_name | employee_name | department |
|-------|-------------|---------------|------------|
| a@company.com | Company A | Alice | Sales |
| b@company.com | Company B | Bob | Marketing |
| c@company.com | Company C | | HR |

**Advantages:**
- Supports formulas for data manipulation
- Multiple sheets possible
- Better for visual editing

### Format 2: CSV (.csv)

**Best for:** Simple lists, version control compatibility

**File:** `data/recipients.csv`

```csv
email,company_name,employee_name,department
a@company.com,Company A,Alice,Sales
b@company.com,Company B,Bob,Marketing
c@company.com,Company C,,HR
```

**Advantages:**
- Human-readable
- Git-friendly (diffable)
- Universal compatibility

### Format 3: Minimal (Required Columns Only)

**File:** `data/recipients.xlsx`

| email | company_name |
|-------|-------------|
| info@company1.com | Company 1 |
| info@company2.com | Company 2 |

**Result:** All emails use "Sir/Ma'am" (professional fallback)

---

## Advanced Scenarios

### Scenario 1: Different Templates for Different Segments

**Problem:** You want to send different messages to different types of companies

**Solution:** Use multiple drafts and segment your data

**Step 1:** Create two drafts in Gmail:
- "Draft 1: Enterprise Outreach"
- "Draft 2: Startup Outreach"

**Step 2:** Segment your data

`data/enterprise_recipients.xlsx` (rename to recipients.xlsx):
| email | company_name | employee_name |
|-------|-------------|---------------|
| enterprise1@bigcorp.com | BigCorp | John |

`data/startup_recipients.xlsx` (rename to recipients.xlsx):
| email | company_name | employee_name |
|-------|-------------|---------------|
| founder@startup.io | StartupIO | Jane |

**Step 3:** Run twice, selecting appropriate draft each time

---

### Scenario 2: Batch Processing Large Lists

**Problem:** You have 500+ recipients and want to process in batches

**Solution:** Split into multiple files

**File 1:** `data/recipients_batch1.xlsx` (Recipients 1-100)
**File 2:** `data/recipients_batch2.xlsx` (Recipients 101-200)
...

**Workflow:**
1. Rename batch1 to recipients.xlsx
2. Run script
3. Rename batch2 to recipients.xlsx
4. Run script
5. Continue...

**Tip:** Check `data/sent_log.csv` to track progress across batches

---

### Scenario 3: Handling Bounces and Invalid Emails

**Problem:** Some emails bounce or are invalid

**Solution:** Use the sent log to identify and clean your list

**sent_log.csv:**
```csv
timestamp,email,company,status
2026-02-17 10:00:00,valid@company.com,Company A,SUCCESS
2026-02-17 10:00:02,invalid@company.com,Company B,FAILED: Invalid email
2026-02-17 10:00:04,bounced@company.com,Company C,FAILED: Bounce
```

**Clean-up Process:**
1. Open sent_log.csv
2. Filter for FAILED status
3. Update your source data
4. Re-run for corrected entries only

---

## Best Practices

### 1. Always Preview First

**Never skip the preview step!** The first 3 emails show you exactly what recipients will see.

**Check for:**
- Correct placeholder replacements
- HTML formatting intact
- Signature displaying properly
- Links are clickable

### 2. Test with Small Batches

**Before sending to 500 people:**
1. Create test list with 3-5 emails (your own, friends, colleagues)
2. Run the script
3. Verify emails look perfect
4. Only then proceed with full list

### 3. Respect Gmail Limits

| Account Type | Daily Limit | Recommended Batch |
|--------------|-------------|-------------------|
| New Gmail | ~100 | 50-75 |
| Established Gmail | ~500 | 200-300 |
| Google Workspace | Higher | 400-500 |

**Wait 24 hours between large batches**

### 4. Monitor the Sent Log

**Regularly check** `data/sent_log.csv` for:
- Failed deliveries
- Rate limit warnings
- Patterns in errors

### 5. Personalization Tips

**Good:**
```
"Dear {{employee_name}}, I noticed {{company_name}} recently..."
```

**Better (with research):**
```
"Dear {{employee_name}}, Congratulations on {{company_name}}'s recent Series B funding!"
```

**Pro Tip:** Add a "notes" column to your Excel for custom snippets per recipient

### 6. Subject Line Optimization

**Generic:**
```
Subject: Partnership Opportunity
```

**Personalized:**
```
Subject: Partnership Opportunity - {{company_name}}
```

**Even Better:**
```
Subject: Quick question about {{company_name}}'s expansion
```

### 7. Timing Your Sends

**Best Times:**
- Tuesday-Thursday
- 9:00-11:00 AM (recipient's timezone)
- Avoid Mondays (busy) and Fridays (checked out)

**With 2-second delays:**
- 100 emails = ~3.5 minutes
- 500 emails = ~17 minutes

### 8. Professional Signature

**Include:**
- Full name
- Title
- Company
- Phone (optional)
- LinkedIn (professional touch)

**Example:**
```
--
John Doe
Senior Developer | TechCorp
📧 john@techcorp.com
🔗 linkedin.com/in/johndoe
```

### 9. Follow-up Strategy

**Day 1:** Initial email
**Day 3-5:** Follow-up #1 (if no reply)
**Day 7-10:** Follow-up #2 (final)

**Track in spreadsheet:**
| email | company | status | sent_date | follow_up_1 | follow_up_2 |

### 10. Data Privacy

**Never:**
- Share recipient lists
- Include sensitive info in drafts
- Use BCC (defeats personalization purpose)

**Always:**
- Keep credentials secure
- Use dedicated sending account
- Respect unsubscribe requests

---

## Troubleshooting Common Issues

### Issue: "nan" appears in email

**Cause:** Empty cells in Excel become NaN (Not a Number)

**Solution:** Already fixed! Empty names now automatically use "Sir/Ma'am"

### Issue: Formatting lost in sent email

**Cause:** Plain text extraction instead of HTML

**Solution:** Already fixed! Script now preserves HTML formatting

### Issue: "Rate limit exceeded"

**Solution:** 
1. Wait 24 hours
2. Reduce batch size
3. Check Google Workspace upgrade options

### Issue: "No drafts found"

**Check:**
- Saved as draft (not sent)
- Using correct Gmail account
- Drafts not in trash

### Issue: "Credentials not found"

**Solution:**
1. Download from Google Cloud Console
2. Rename to `credentials.json`
3. Place in project root

---

## Quick Reference Card

### File Structure
```
data/
├── recipients.xlsx     # Your recipient list
└── sent_log.csv        # Auto-generated tracking

gmail_mail_merger/
├── main.py            # Run this
└── config.py          # Edit settings here
```

### Available Placeholders
```
{{email}}           → john@company.com
{{company_name}}    → Company Name
{{company}}         → Company Name (alias)
{{employee_name}}   → John Doe
{{name}}            → John Doe (alias)
```

### Commands
```bash
# Setup
pip install -r requirements.txt

# Run
python gmail_mail_merger/main.py

# Check logs
cat data/sent_log.csv
```

### Gmail Limits
- Standard: 100-500/day
- Delay: 2 seconds between sends
- Consecutive failures: Stop after 2

---

**Need more help?** Check the main [README.md](../README.md) or [DESIGN.md](DESIGN.md)
