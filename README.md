# 🛡️ NoshGuard MVP

Real-time food recall detection and consumer notification platform.
Pulls live data from the FDA Enforcement Reports API and matches it
against customer purchase history, then sends targeted alerts.

---

## What this demo does

- Fetches the 25 most recent food recalls live from the FDA API
- Displays severity (Class I / II / III), company, reason, and date
- Matches recalls against 6 demo customers with realistic purchase histories
- Shows which customers are at risk and what they bought
- Simulates sending SMS/email alerts with a single button click
- Updates automatically every hour

---

## Run it FREE in 4 steps (Streamlit Community Cloud)

### Step 1 — Create a free GitHub account
Go to https://github.com and sign up (free).

### Step 2 — Create a new repository
- Click the green "New" button
- Name it: `noshguard-mvp`
- Set it to **Public**
- Click "Create repository"

### Step 3 — Upload your files
Upload these two files to your new repo:
- `dashboard.py`
- `requirements.txt`

(Click "uploading an existing file" on the repo page)

### Step 4 — Deploy on Streamlit Cloud
- Go to https://share.streamlit.io
- Sign in with your GitHub account
- Click "New app"
- Select your `noshguard-mvp` repo
- Set Main file path to: `dashboard.py`
- Click "Deploy"

Your app will be live at a public URL like:
`https://your-name-noshguard-mvp.streamlit.app`

**Total cost: $0. Total time: ~15 minutes.**

---

## Share your live demo link with grocery store prospects

Once deployed, you have a real, working URL you can:
- Send in a cold email ("here's a live demo of what I'm building")
- Screen-share during a Zoom call
- Include in your one-pager or pitch deck

---

## Upgrading to real SMS/email notifications

When you're ready to send real alerts, you'll add:

**Twilio (SMS):**
```python
from twilio.rest import Client
client = Client(TWILIO_SID, TWILIO_TOKEN)
client.messages.create(body=message, from_="+1XXXXXXXXXX", to=customer_phone)
```

**SendGrid (Email):**
```python
import sendgrid
sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_KEY)
# ... send email
```

Both have free tiers sufficient for demo/MVP use.

---

## File structure

```
noshguard-mvp/
├── dashboard.py       ← Everything: UI, logic, FDA feed, matching, alerts
└── requirements.txt   ← Just: streamlit + requests
```

---

## Next steps (roadmap)

- [ ] Connect to real grocery store POS / loyalty data via API
- [ ] Add USDA recall feed alongside FDA
- [ ] Build customer self-enrollment web form
- [ ] Enable real Twilio SMS + SendGrid email
- [ ] Add per-store admin dashboard for grocery managers
- [ ] Mobile app (Phase 2)

---

*NoshGuard — Protecting families from recalled food, one notification at a time.*
