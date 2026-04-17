import streamlit as st
import requests
import json
from datetime import datetime

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="NoshGuard",
    page_icon="🛡️",
    layout="wide"
)

# ─────────────────────────────────────────────
# CUSTOM STYLING
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0f1117; color: #e8e8e8; }
    .block-container { padding-top: 2rem; }

    .ng-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-left: 5px solid #e63946;
        padding: 1.5rem 2rem;
        border-radius: 8px;
        margin-bottom: 2rem;
    }
    .ng-header h1 { color: #e63946; font-size: 2.4rem; margin: 0; letter-spacing: 2px; }
    .ng-header p  { color: #a0a0b0; margin: 0.4rem 0 0; font-size: 1rem; }

    .recall-card {
        background: #1a1a2e;
        border: 1px solid #2a2a4a;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }
    .recall-card.class1 { border-left: 4px solid #e63946; }
    .recall-card.class2 { border-left: 4px solid #f4a261; }
    .recall-card.class3 { border-left: 4px solid #52b788; }

    .severity-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .s1 { background: #e63946; color: white; }
    .s2 { background: #f4a261; color: #1a1a1a; }
    .s3 { background: #52b788; color: #1a1a1a; }

    .match-card {
        background: #1a1a2e;
        border: 1px solid #e63946;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }
    .match-name   { color: #e63946; font-weight: bold; font-size: 1.1rem; }
    .match-detail { color: #c0c0d0; font-size: 0.9rem; margin-top: 0.3rem; }

    .alert-sent {
        background: #1b3a2a;
        border: 1px solid #52b788;
        color: #52b788;
        padding: 0.6rem 1rem;
        border-radius: 6px;
        margin-bottom: 0.4rem;
        font-size: 0.9rem;
    }

    .stat-box {
        background: #1a1a2e;
        border: 1px solid #2a2a4a;
        border-radius: 8px;
        padding: 1.2rem;
        text-align: center;
    }
    .stat-number { font-size: 2.2rem; font-weight: bold; color: #e63946; }
    .stat-label  { font-size: 0.8rem; color: #a0a0b0; text-transform: uppercase; letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FAKE CUSTOMER DATABASE
# Demo data — in production this connects to
# a grocery loyalty / POS integration
# ─────────────────────────────────────────────
CUSTOMERS = [
    {
        "id": "C-1001",
        "name": "Maria Gonzalez",
        "phone": "+15551110001",
        "email": "maria.g@email.com",
        "store": "Whole Foods #847 – Austin, TX",
        "purchase_date": "April 9, 2025",
        "purchases": ["spinach", "baby spinach", "dole spinach", "organic spinach"]
    },
    {
        "id": "C-1002",
        "name": "James Carter",
        "phone": "+15551110002",
        "email": "jcarter@email.com",
        "store": "Kroger #312 – Nashville, TN",
        "purchase_date": "April 11, 2025",
        "purchases": ["ground beef", "beef", "hamburger", "angus beef"]
    },
    {
        "id": "C-1003",
        "name": "Linda Park",
        "phone": "+15551110003",
        "email": "lpark@email.com",
        "store": "Publix #229 – Atlanta, GA",
        "purchase_date": "April 10, 2025",
        "purchases": ["chicken salad", "chicken", "rotisserie chicken", "deli chicken"]
    },
    {
        "id": "C-1004",
        "name": "Robert Johnson",
        "phone": "+15551110004",
        "email": "rjohnson@email.com",
        "store": "Safeway #451 – Denver, CO",
        "purchase_date": "April 12, 2025",
        "purchases": ["lettuce", "romaine", "iceberg lettuce", "salad kit"]
    },
    {
        "id": "C-1005",
        "name": "Susan Chen",
        "phone": "+15551110005",
        "email": "schen@email.com",
        "store": "HEB #88 – Houston, TX",
        "purchase_date": "April 8, 2025",
        "purchases": ["deli meat", "turkey", "sliced turkey", "lunch meat", "cold cuts"]
    },
    {
        "id": "C-1006",
        "name": "Derek Williams",
        "phone": "+15551110006",
        "email": "dwilliams@email.com",
        "store": "Meijer #67 – Columbus, OH",
        "purchase_date": "April 13, 2025",
        "purchases": ["frozen pizza", "pizza", "digiorno", "frozen meals"]
    },
]


# ─────────────────────────────────────────────
# FDA RECALL FETCHER
# ─────────────────────────────────────────────
@st.cache_data(ttl=3600)
def fetch_recalls(limit=25):
    url = f"https://api.fda.gov/food/enforcement.json?limit={limit}&sort=report_date:desc"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        cleaned = []
        for r in data.get("results", []):
            cleaned.append({
                "product": r.get("product_description", "Unknown product"),
                "company": r.get("recalling_firm", "Unknown firm"),
                "reason":  r.get("reason_for_recall", "No reason provided"),
                "date":    _fmt_date(r.get("report_date", "")),
                "class":   r.get("classification", "Unknown"),
                "state":   r.get("distribution_pattern", "Unknown distribution"),
                "status":  r.get("status", ""),
            })
        return cleaned
    except Exception as e:
        st.error(f"Could not reach FDA API: {e}")
        return []


def _fmt_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y%m%d").strftime("%b %d, %Y")
    except:
        return date_str


def _severity(cls):
    if "Class I"   in cls: return "class1", "s1", "Class I – High Risk"
    if "Class II"  in cls: return "class2", "s2", "Class II – Moderate Risk"
    if "Class III" in cls: return "class3", "s3", "Class III – Low Risk"
    return "class3", "s3", cls


# ─────────────────────────────────────────────
# MATCHING ENGINE
# ─────────────────────────────────────────────
def match_recalls_to_customers(recalls):
    matches = []
    seen = set()

    for recall in recalls:
        product_lower = recall["product"].lower()

        for customer in CUSTOMERS:
            for keyword in customer["purchases"]:
                if keyword.lower() in product_lower:
                    key = (customer["id"], recall["product"][:40])
                    if key not in seen:
                        seen.add(key)
                        matches.append({
                            "customer_id":   customer["id"],
                            "name":          customer["name"],
                            "phone":         customer["phone"],
                            "email":         customer["email"],
                            "store":         customer["store"],
                            "purchase_date": customer["purchase_date"],
                            "product":       recall["product"],
                            "reason":        recall["reason"],
                            "class":         recall["class"],
                            "recall_date":   recall["date"],
                            "company":       recall["company"],
                        })
                    break
    return matches


# ─────────────────────────────────────────────
# NOTIFICATION BUILDER
# Swap print() for Twilio / SendGrid in production
# ─────────────────────────────────────────────
def build_alert_message(m):
    first = m["name"].split()[0]
    store = m["store"].split("–")[0].strip()
    return (
        f"⚠️ NoshGuard ALERT\n\n"
        f"Hi {first}, a product you purchased on {m['purchase_date']} "
        f"at {store} has been recalled by {m['company']}.\n\n"
        f"Product: {m['product']}\n"
        f"Reason:  {m['reason']}\n"
        f"Severity: {m['class']}\n\n"
        f"Please discard or return this item immediately. Do not consume.\n"
        f"— NoshGuard | Protecting your family at every meal."
    )


# ─────────────────────────────────────────────
# UI — HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="ng-header">
    <h1>🛡️ NOSHGUARD</h1>
    <p>Real-time food recall detection & consumer notification &nbsp;|&nbsp; Live FDA data</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
with st.spinner("Fetching live FDA recall data..."):
    recalls = fetch_recalls()

matches = match_recalls_to_customers(recalls)
class1_count = sum(1 for r in recalls if "Class I" in r["class"])


# ─────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""<div class="stat-box">
        <div class="stat-number">{len(recalls)}</div>
        <div class="stat-label">Active Recalls</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""<div class="stat-box">
        <div class="stat-number">{class1_count}</div>
        <div class="stat-label">High Risk (Class I)</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""<div class="stat-box">
        <div class="stat-number">{len(CUSTOMERS)}</div>
        <div class="stat-label">Monitored Customers</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""<div class="stat-box">
        <div class="stat-number" style="color: {'#e63946' if matches else '#52b788'}">{len(matches)}</div>
        <div class="stat-label">Customers At Risk</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TWO COLUMN LAYOUT
# ─────────────────────────────────────────────
left, right = st.columns([3, 2])

# ── LEFT: LIVE RECALL FEED ──
with left:
    st.subheader("🚨 Live FDA Recall Feed")
    st.caption("Source: FDA Enforcement Reports API • Updates hourly")

    if not recalls:
        st.warning("No recall data loaded.")
    else:
        for r in recalls[:15]:
            card_class, badge_class, severity_label = _severity(r["class"])
            st.markdown(f"""
            <div class="recall-card {card_class}">
                <span class="severity-badge {badge_class}">{severity_label}</span>&nbsp;&nbsp;
                <small style="color:#666">{r['date']}</small><br>
                <strong style="color:#e8e8e8">{r['product'][:90]}{'...' if len(r['product']) > 90 else ''}</strong><br>
                <span style="color:#a0a0b0; font-size:0.85rem">{r['company']}</span><br>
                <span style="color:#c0c0d0; font-size:0.82rem; margin-top:4px; display:block">
                    📋 {r['reason'][:120]}{'...' if len(r['reason']) > 120 else ''}
                </span>
            </div>
            """, unsafe_allow_html=True)


# ── RIGHT: MATCHED CUSTOMERS ──
with right:
    st.subheader("⚠️ Affected Customers")

    if not matches:
        st.markdown("""
        <div style="background:#1a1a2e; border:1px solid #2a2a4a; border-radius:8px;
                    padding:1.5rem; text-align:center; color:#52b788;">
            ✅ No customers matched to current recalls
        </div>
        """, unsafe_allow_html=True)
    else:
        for m in matches:
            _, badge_class, severity_label = _severity(m["class"])
            st.markdown(f"""
            <div class="match-card">
                <div class="match-name">⚠️ {m['name']}</div>
                <div class="match-detail">🏪 {m['store']}</div>
                <div class="match-detail">🛒 Purchased: {m['purchase_date']}</div>
                <div class="match-detail" style="margin-top:6px">
                    <span class="severity-badge {badge_class}">{severity_label}</span>
                </div>
                <div class="match-detail" style="margin-top:6px; color:#e8e8e8">
                    {m['product'][:80]}{'...' if len(m['product']) > 80 else ''}
                </div>
                <div class="match-detail">📋 {m['reason'][:100]}{'...' if len(m['reason']) > 100 else ''}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── SEND ALERTS BUTTON ──
    st.subheader("📲 Notification Center")

    if not matches:
        st.info("No alerts to send right now.")
    else:
        st.write(f"**{len(matches)} customer(s)** ready to be notified.")

        if st.button("🚀 Send All Alerts Now", type="primary", use_container_width=True):
            st.markdown("**Alerts dispatched:**")
            for m in matches:
                msg = build_alert_message(m)
                st.markdown(f"""
                <div class="alert-sent">
                    ✅ Alert sent → <strong>{m['name']}</strong>
                    ({m['email']} / {m['phone']})<br>
                    <small>{m['product'][:60]}</small>
                </div>
                """, unsafe_allow_html=True)
                # Preview message in expander
                with st.expander(f"Preview: {m['name']}'s alert message"):
                    st.code(msg)

            st.success(f"✅ {len(matches)} notification(s) sent successfully!")
            st.caption("🔧 Production mode: replace simulated sends with Twilio SMS + SendGrid email")


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#444; font-size:0.8rem; padding: 1rem 0;">
    🛡️ NoshGuard MVP &nbsp;|&nbsp; Powered by FDA Open Data API &nbsp;|&nbsp;
    <em>Protecting families from recalled food — one notification at a time.</em>
</div>
""", unsafe_allow_html=True)
