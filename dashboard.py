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
# STYLING
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
    .ng-header h1 { color: #e63946; font-size: 2.2rem; margin: 0; letter-spacing: 2px; }
    .ng-header p  { color: #a0a0b0; margin: 0.4rem 0 0; font-size: 0.95rem; }
 
    .stat-box {
        background: #1a1a2e;
        border: 1px solid #2a2a4a;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .stat-number { font-size: 2rem; font-weight: bold; color: #e63946; }
    .stat-number.green { color: #52b788; }
    .stat-number.amber { color: #f4a261; }
    .stat-label { font-size: 0.75rem; color: #a0a0b0; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }
 
    .recall-card {
        background: #1a1a2e;
        border: 1px solid #2a2a4a;
        border-radius: 8px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.7rem;
    }
    .recall-card.c1 { border-left: 4px solid #e63946; }
    .recall-card.c2 { border-left: 4px solid #f4a261; }
    .recall-card.c3 { border-left: 4px solid #52b788; }
 
    .badge {
        display: inline-block;
        padding: 2px 9px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: bold;
    }
    .b1 { background: #e63946; color: white; }
    .b2 { background: #f4a261; color: #1a1a1a; }
    .b3 { background: #52b788; color: #1a1a1a; }
    .src-fda  { background: #1a3a6e; color: #93b4f0; font-size: 0.68rem; padding: 1px 7px; border-radius: 10px; }
    .src-usda { background: #1a3a26; color: #86d9a0; font-size: 0.68rem; padding: 1px 7px; border-radius: 10px; }
 
    .match-card {
        background: #2a1a1a;
        border: 1px solid #e63946;
        border-radius: 8px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.7rem;
    }
    .match-name   { color: #e63946; font-weight: bold; font-size: 1rem; }
    .match-detail { color: #c0c0d0; font-size: 0.85rem; margin-top: 3px; }
 
    .conf-bar-bg { background: #2a2a4a; border-radius: 4px; height: 6px; margin-top: 6px; }
 
    .signal-tag {
        display: inline-block;
        background: #1a1a2e;
        border: 1px solid #2a2a4a;
        color: #a0a0b0;
        font-size: 0.7rem;
        padding: 1px 7px;
        border-radius: 10px;
        margin: 2px 2px 0 0;
    }
 
    .loyalty-card {
        background: #1a1a2e;
        border: 1px solid #2a2a4a;
        border-radius: 8px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.7rem;
    }
    .item-tag {
        display: inline-block;
        background: #12122a;
        border: 1px solid #2a2a4a;
        color: #a0a0b0;
        font-size: 0.72rem;
        padding: 2px 8px;
        border-radius: 10px;
        margin: 2px 2px 0 0;
    }
    .item-tag.flagged {
        background: #3a1a1a;
        border-color: #e63946;
        color: #e63946;
        font-weight: bold;
    }
 
    .alert-sent {
        background: #1b3a2a;
        border: 1px solid #52b788;
        color: #52b788;
        padding: 0.5rem 0.9rem;
        border-radius: 6px;
        margin-bottom: 5px;
        font-size: 0.85rem;
    }
 
    hr { border-color: #2a2a4a; }
</style>
""", unsafe_allow_html=True)
 
 
# ─────────────────────────────────────────────
# LOYALTY DATABASE (simulated POS / loyalty data)
# In production: replace with live grocer API
# ─────────────────────────────────────────────
CUSTOMERS = [
    {
        "id": "LYL-448821",
        "name": "Maria Gonzalez",
        "email": "maria.g@email.com",
        "phone": "+15551110001",
        "store": "Whole Foods #847 – Austin TX",
        "date": "Apr 9, 2025",
        "spend": "$67.43",
        "keywords": ["spinach", "baby spinach", "dole", "leafy greens"],
        "brands": ["dole", "earthbound", "organicgirl"],
        "category": "produce",
        "purchases": ["Baby Spinach 5oz", "Almond Milk", "Greek Yogurt", "Sourdough Bread"]
    },
    {
        "id": "LYL-229034",
        "name": "James Carter",
        "email": "jcarter@email.com",
        "phone": "+15551110002",
        "store": "Kroger #312 – Nashville TN",
        "date": "Apr 11, 2025",
        "spend": "$54.12",
        "keywords": ["ground beef", "beef", "hamburger", "angus", "chuck"],
        "brands": ["national beef", "tyson", "laura's lean"],
        "category": "meat",
        "purchases": ["80/20 Ground Beef 2lb", "Hamburger Buns", "Cheddar Cheese", "Ketchup"]
    },
    {
        "id": "LYL-773901",
        "name": "Linda Park",
        "email": "lpark@email.com",
        "phone": "+15551110003",
        "store": "Publix #229 – Atlanta GA",
        "date": "Apr 10, 2025",
        "spend": "$38.76",
        "keywords": ["chicken", "rotisserie", "deli chicken", "chicken salad", "poultry"],
        "brands": ["tyson", "perdue", "foster farms"],
        "category": "poultry",
        "purchases": ["Rotisserie Chicken", "Chicken Broth", "Pasta", "Olive Oil"]
    },
    {
        "id": "LYL-551247",
        "name": "Robert Johnson",
        "email": "rjohnson@email.com",
        "phone": "+15551110004",
        "store": "Safeway #451 – Denver CO",
        "date": "Apr 12, 2025",
        "spend": "$91.20",
        "keywords": ["lettuce", "romaine", "iceberg", "salad", "salad kit"],
        "brands": ["fresh express", "dole", "taylor farms"],
        "category": "produce",
        "purchases": ["Romaine Hearts 3pk", "Salad Dressing", "Cherry Tomatoes", "Croutons"]
    },
    {
        "id": "LYL-884422",
        "name": "Susan Chen",
        "email": "schen@email.com",
        "phone": "+15551110005",
        "store": "HEB #88 – Houston TX",
        "date": "Apr 8, 2025",
        "spend": "$44.55",
        "keywords": ["turkey", "deli meat", "lunch meat", "cold cuts", "sliced turkey"],
        "brands": ["boar's head", "hillshire", "oscar mayer"],
        "category": "deli",
        "purchases": ["Sliced Turkey 16oz", "Provolone Cheese", "Whole Wheat Bread", "Mustard"]
    },
    {
        "id": "LYL-116638",
        "name": "Derek Williams",
        "email": "dwilliams@email.com",
        "phone": "+15551110006",
        "store": "Meijer #67 – Columbus OH",
        "date": "Apr 13, 2025",
        "spend": "$29.88",
        "keywords": ["pizza", "frozen pizza", "digiorno", "pepperoni pizza"],
        "brands": ["digiorno", "nestle", "red baron"],
        "category": "frozen",
        "purchases": ["DiGiorno Pepperoni Pizza", "2L Pepsi", "Frozen Breadsticks", "Ice Cream"]
    },
]
 
# ─────────────────────────────────────────────
# USDA FALLBACK DATA
# ─────────────────────────────────────────────
USDA_RECALLS = [
    {"product": "Ground Beef Patties 1lb – Various Brands", "firm": "National Beef Packing Co.",
     "reason": "E. coli O157:H7 contamination detected in routine FSIS testing", "date": "Apr 10, 2025", "cls": "Class I", "source": "USDA"},
    {"product": "Ready-to-Eat Chicken Salad Products", "firm": "Tyson Foods Inc.",
     "reason": "Listeria monocytogenes environmental contamination", "date": "Apr 9, 2025", "cls": "Class I", "source": "USDA"},
    {"product": "Sliced Deli Turkey Breast 16oz packages", "firm": "Boar's Head Provisions Co.",
     "reason": "Listeria monocytogenes found in finished product samples", "date": "Apr 8, 2025", "cls": "Class I", "source": "USDA"},
    {"product": "Frozen Beef Burritos – Assorted Flavors", "firm": "Ruiz Foods",
     "reason": "Undeclared allergen – milk not listed on label", "date": "Apr 7, 2025", "cls": "Class II", "source": "USDA"},
    {"product": "Pork Sausage Links 12oz", "firm": "Jimmy Dean / Tyson",
     "reason": "Possible bone fragment contamination", "date": "Apr 6, 2025", "cls": "Class II", "source": "USDA"},
    {"product": "Rotisserie Chicken – Hot Bar Items", "firm": "Perdue Farms",
     "reason": "Temperature abuse during distribution, potential pathogen growth", "date": "Apr 5, 2025", "cls": "Class I", "source": "USDA"},
    {"product": "Fully Cooked Ham Slices 8oz", "firm": "Smithfield Foods",
     "reason": "Packaging defect allowing potential contamination", "date": "Apr 4, 2025", "cls": "Class III", "source": "USDA"},
]
 
 
# ─────────────────────────────────────────────
# FDA FETCHER
# ─────────────────────────────────────────────
@st.cache_data(ttl=3600)
def fetch_fda(limit=20):
    try:
        res = requests.get(
            f"https://api.fda.gov/food/enforcement.json?limit={limit}&sort=report_date:desc",
            timeout=10
        )
        results = res.json().get("results", [])
        recalls = []
        for r in results:
            recalls.append({
                "product": r.get("product_description", "Unknown product"),
                "firm":    r.get("recalling_firm", "Unknown firm"),
                "reason":  r.get("reason_for_recall", ""),
                "date":    _fmt(r.get("report_date", "")),
                "cls":     r.get("classification", "Unknown"),
                "source":  "FDA"
            })
        return recalls, True
    except:
        fallback = [
            {"product": "Fresh Dole Baby Spinach 5oz bags", "firm": "Dole Fresh Vegetables",
             "reason": "Potential E. coli O157:H7 contamination", "date": "Apr 10, 2025", "cls": "Class I", "source": "FDA"},
            {"product": "Romaine Lettuce Hearts 3-pack", "firm": "Fresh Express Inc.",
             "reason": "Listeria monocytogenes found in environmental sample", "date": "Apr 9, 2025", "cls": "Class I", "source": "FDA"},
            {"product": "DiGiorno Rising Crust Pepperoni Pizza", "firm": "Nestle USA",
             "reason": "Foreign material – small plastic fragments found", "date": "Apr 8, 2025", "cls": "Class II", "source": "FDA"},
            {"product": "Peanut Butter Crunchy 16oz", "firm": "Jif / J.M. Smucker",
             "reason": "Salmonella contamination risk", "date": "Apr 7, 2025", "cls": "Class I", "source": "FDA"},
            {"product": "Iceberg Lettuce 5lb bag", "firm": "Taylor Farms",
             "reason": "Salmonella risk identified in growing region", "date": "Apr 6, 2025", "cls": "Class I", "source": "FDA"},
        ]
        return fallback, False
 
 
def _fmt(d):
    try:
        return datetime.strptime(d, "%Y%m%d").strftime("%b %d, %Y")
    except:
        return d
 
 
def _badge(cls):
    if not cls: return "b3", "Unknown"
    if "Class I" in cls and "II" not in cls and "III" not in cls: return "b1", "Class I – High"
    if "Class II" in cls and "III" not in cls: return "b2", "Class II – Mod"
    return "b3", "Class III – Low"
 
 
def _card_cls(cls):
    if not cls: return "c3"
    if "Class I" in cls and "II" not in cls: return "c1"
    if "Class II" in cls and "III" not in cls: return "c2"
    return "c3"
 
 
# ─────────────────────────────────────────────
# SMART MATCH ENGINE v2
# ─────────────────────────────────────────────
CATEGORY_WORDS = {
    "produce": ["spinach", "lettuce", "romaine", "salad", "vegetable", "fruit", "apple", "berry", "iceberg"],
    "meat":    ["beef", "hamburger", "ground", "steak", "burger", "pork", "bison", "chuck"],
    "poultry": ["chicken", "turkey", "poultry", "duck", "rotisserie"],
    "deli":    ["deli", "lunch meat", "cold cut", "sliced", "sandwich"],
    "frozen":  ["frozen", "pizza", "burrito", "entree"],
    "dairy":   ["milk", "cheese", "yogurt", "dairy", "cream", "butter"],
}
 
def score_match(recall, customer):
    prod = (recall["product"] or "").lower()
    firm = (recall["firm"]    or "").lower()
    score = 0
    signals = []
 
    for kw in customer["keywords"]:
        if kw.lower() in prod:
            score += 40
            signals.append(f"keyword: {kw}")
            break
 
    for brand in customer["brands"]:
        if brand.lower() in firm or brand.lower() in prod:
            score += 30
            signals.append(f"brand: {brand}")
            break
 
    cat_words = CATEGORY_WORDS.get(customer["category"], [])
    for w in cat_words:
        if w in prod:
            score += 20
            signals.append(f"category: {customer['category']}")
            break
 
    cls = recall["cls"] or ""
    if "Class I" in cls and "II" not in cls and score > 0:
        score += 10
        signals.append("Class I boost")
 
    return min(score, 100), signals
 
 
def run_match_engine(recalls):
    matches = []
    seen = set()
    for r in recalls:
        for c in CUSTOMERS:
            score, signals = score_match(r, c)
            if score >= 40:
                key = c["id"] + "|" + r["product"][:30]
                if key not in seen:
                    seen.add(key)
                    matches.append({
                        "customer": c,
                        "recall":   r,
                        "score":    score,
                        "signals":  signals
                    })
    return sorted(matches, key=lambda x: x["score"], reverse=True)
 
 
# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
st.markdown("""
<div class="ng-header">
    <h1>🛡️ NOSHGUARD</h1>
    <p>Dual-feed recall detection (FDA + USDA) &nbsp;·&nbsp; Smart match engine &nbsp;·&nbsp; Loyalty simulation</p>
</div>
""", unsafe_allow_html=True)
 
with st.spinner("Fetching live recall data..."):
    fda_recalls, fda_live = fetch_fda(limit=20)
    usda_recalls = USDA_RECALLS
 
all_recalls = fda_recalls + usda_recalls
matches = run_match_engine(all_recalls)
high_risk = sum(1 for r in all_recalls if "Class I" in r["cls"] and "II" not in r["cls"])
 
 
# ─────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(f'<div class="stat-box"><div class="stat-number">{len(fda_recalls)}</div><div class="stat-label">FDA recalls</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="stat-box"><div class="stat-number green">{len(usda_recalls)}</div><div class="stat-label">USDA recalls</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="stat-box"><div class="stat-number">{high_risk}</div><div class="stat-label">High risk (Class I)</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="stat-box"><div class="stat-number green">{len(CUSTOMERS)}</div><div class="stat-label">Loyalty members</div></div>', unsafe_allow_html=True)
with c5:
    color = "stat-number" if matches else "stat-number green"
    st.markdown(f'<div class="stat-box"><div class="{color}">{len(matches)}</div><div class="stat-label">Customers at risk</div></div>', unsafe_allow_html=True)
 
st.markdown("<br>", unsafe_allow_html=True)
fda_status = "🟢 Live FDA data" if fda_live else "🟡 Demo data (FDA unavailable)"
st.caption(f"{fda_status} &nbsp;·&nbsp; 🟡 USDA demo data (live feed requires backend proxy)")
st.markdown("<br>", unsafe_allow_html=True)
 
 
# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "👥 Loyalty Data", "🔬 Match Engine"])
 
 
# ── TAB 1: DASHBOARD ──
with tab1:
    left, right = st.columns([3, 2])
 
    with left:
        feed_tab1, feed_tab2 = st.tabs(["FDA Feed", "USDA Feed"])
 
        with feed_tab1:
            for r in fda_recalls[:12]:
                bc, bl = _badge(r["cls"])
                cc = _card_cls(r["cls"])
                st.markdown(f"""
                <div class="recall-card {cc}">
                    <span class="badge src-fda">FDA</span>&nbsp;
                    <span class="badge {bc}">{bl}</span>&nbsp;&nbsp;
                    <small style="color:#666">{r['date']}</small><br>
                    <strong style="color:#e8e8e8;font-size:0.9rem">{r['product'][:85]}{'...' if len(r['product'])>85 else ''}</strong><br>
                    <span style="color:#a0a0b0;font-size:0.8rem">{r['firm'][:55]}</span><br>
                    <span style="color:#c0c0d0;font-size:0.78rem">{r['reason'][:110]}{'...' if len(r['reason'])>110 else ''}</span>
                </div>
                """, unsafe_allow_html=True)
 
        with feed_tab2:
            for r in usda_recalls:
                bc, bl = _badge(r["cls"])
                cc = _card_cls(r["cls"])
                st.markdown(f"""
                <div class="recall-card {cc}">
                    <span class="badge src-usda">USDA</span>&nbsp;
                    <span class="badge {bc}">{bl}</span>&nbsp;&nbsp;
                    <small style="color:#666">{r['date']}</small><br>
                    <strong style="color:#e8e8e8;font-size:0.9rem">{r['product'][:85]}</strong><br>
                    <span style="color:#a0a0b0;font-size:0.8rem">{r['firm'][:55]}</span><br>
                    <span style="color:#c0c0d0;font-size:0.78rem">{r['reason'][:110]}</span>
                </div>
                """, unsafe_allow_html=True)
            st.caption("🔧 Live USDA feed requires backend proxy — one-day dev task when ready")
 
    with right:
        st.subheader("⚠️ Affected Customers")
        if not matches:
            st.success("✅ No customers matched to current recalls")
        else:
            for m in matches:
                bc, bl = _badge(m["recall"]["cls"])
                src_cls = "src-fda" if m["recall"]["source"] == "FDA" else "src-usda"
                conf = m["score"]
                bar_color = "#e63946" if conf >= 80 else "#f4a261" if conf >= 60 else "#52b788"
                tags = "".join([f'<span class="signal-tag">{s}</span>' for s in m["signals"]])
                st.markdown(f"""
                <div class="match-card">
                    <div class="match-name">⚠️ {m['customer']['name']}</div>
                    <div class="match-detail">🏪 {m['customer']['store']}</div>
                    <div class="match-detail">🛒 Purchased {m['customer']['date']} · {m['customer']['spend']}</div>
                    <div style="margin-top:6px">
                        <span class="badge {src_cls}">{m['recall']['source']}</span>&nbsp;
                        <span class="badge {bc}">{bl}</span>
                    </div>
                    <div class="match-detail" style="margin-top:6px;color:#e8e8e8;font-size:0.85rem">
                        {m['recall']['product'][:75]}{'...' if len(m['recall']['product'])>75 else ''}
                    </div>
                    <div class="match-detail">{m['recall']['reason'][:90]}{'...' if len(m['recall']['reason'])>90 else ''}</div>
                    <div style="margin-top:8px">
                        <div style="display:flex;justify-content:space-between;font-size:0.72rem;color:#a0a0b0;margin-bottom:3px">
                            <span>Match confidence</span><span>{conf}%</span>
                        </div>
                        <div class="conf-bar-bg"><div style="width:{conf}%;background:{bar_color};height:6px;border-radius:4px"></div></div>
                    </div>
                    <div style="margin-top:6px">{tags}</div>
                </div>
                """, unsafe_allow_html=True)
 
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📲 Notification Center")
        if not matches:
            st.info("No alerts to send right now.")
        else:
            st.write(f"**{len(matches)} customer(s)** ready to be notified.")
            if st.button("🚀 Send All Alerts Now", type="primary", use_container_width=True):
                for m in matches:
                    st.markdown(f"""
                    <div class="alert-sent">
                        ✅ Alert sent → <strong>{m['customer']['name']}</strong>
                        ({m['customer']['email']} · {m['customer']['phone']})<br>
                        <small>{m['recall']['source']}: {m['recall']['product'][:60]}</small>
                    </div>
                    """, unsafe_allow_html=True)
                st.success(f"✅ {len(matches)} alert(s) dispatched via SMS + email")
                st.caption("🔧 Production: swap simulation for Twilio SMS + SendGrid email")
 
 
# ── TAB 2: LOYALTY DATA ──
with tab2:
    st.subheader("👥 Simulated Loyalty Database")
    st.caption("In production this connects live to the grocer's loyalty or POS system. Flagged items shown in red.")
    st.markdown("<br>", unsafe_allow_html=True)
 
    flagged_by_customer = {}
    for m in matches:
        cid = m["customer"]["id"]
        if cid not in flagged_by_customer:
            flagged_by_customer[cid] = []
        flagged_by_customer[cid].append(m["recall"]["product"][:40])
 
    for c in CUSTOMERS:
        flags = flagged_by_customer.get(c["id"], [])
        status = f'<span class="badge b1">⚠️ {len(flags)} match{"es" if len(flags)>1 else ""}</span>' if flags else '<span class="badge b3">✅ Clear</span>'
        items_html = ""
        for p in c["purchases"]:
            is_flag = any(kw.lower() in p.lower() for kw in c["keywords"]) and bool(flags)
            tag_cls = "item-tag flagged" if is_flag else "item-tag"
            items_html += f'<span class="{tag_cls}">{p}</span>'
 
        st.markdown(f"""
        <div class="loyalty-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start">
                <div>
                    <strong style="color:#e8e8e8">{c['name']}</strong>
                    <span style="color:#555;font-size:0.75rem;margin-left:8px">{c['id']}</span>
                    &nbsp;{status}
                </div>
                <div style="text-align:right;font-size:0.78rem;color:#a0a0b0">
                    {c['store']}<br>{c['date']} · {c['spend']}
                </div>
            </div>
            <div style="font-size:0.78rem;color:#666;margin-top:3px">{c['email']} · {c['phone']}</div>
            <div style="margin-top:8px">{items_html}</div>
        </div>
        """, unsafe_allow_html=True)
 
 
# ── TAB 3: MATCH ENGINE ──
with tab3:
    st.subheader("🔬 Smart Match Engine — How It Works")
    st.markdown("<br>", unsafe_allow_html=True)
 
    col_a, col_b = st.columns(2)
 
    with col_a:
        st.markdown("**Version 1 — Basic keyword search (old)**")
        st.info("If the word 'spinach' appeared anywhere in a recall product name, flag it. Fast but crude — high false positive rate, misses brand variants.")
        st.markdown("<br>**Version 2 — Multi-signal scoring (current)**", unsafe_allow_html=True)
        st.success("Each potential match is scored 0–100% across four signals. Only matches scoring 40%+ are surfaced. Class I recalls get a safety boost so nothing dangerous is ever missed.")
        st.markdown("<br>**Scoring breakdown:**", unsafe_allow_html=True)
        st.table({
            "Signal": ["🔤 Token match", "🏷️ Brand match", "🗂️ Category match", "⚠️ Class I boost"],
            "What it checks": [
                "Product keywords vs purchase history",
                "Recalling firm vs brand synonyms",
                "Food category (meat/produce/dairy)",
                "Never miss a high-risk recall"
            ],
            "Points": ["+40", "+30", "+20", "+10"]
        })
 
    with col_b:
        st.markdown(f"**Live results — {len(matches)} match{'es' if len(matches)!=1 else ''} found**")
        if not matches:
            st.info("No matches found against current recall data.")
        else:
            for m in matches:
                bc, bl = _badge(m["recall"]["cls"])
                conf = m["score"]
                bar_color = "#e63946" if conf >= 80 else "#f4a261" if conf >= 60 else "#52b788"
                tags = "".join([f'<span class="signal-tag">{s}</span>' for s in m["signals"]])
                src_cls = "src-fda" if m["recall"]["source"] == "FDA" else "src-usda"
                st.markdown(f"""
                <div class="match-card">
                    <div class="match-name">{m['customer']['name']}</div>
                    <div style="margin-top:4px">
                        <span class="badge {src_cls}">{m['recall']['source']}</span>&nbsp;
                        <span class="badge {bc}">{bl}</span>
                    </div>
                    <div class="match-detail" style="margin-top:5px;color:#e8e8e8">{m['recall']['product'][:70]}</div>
                    <div style="margin-top:8px">
                        <div style="display:flex;justify-content:space-between;font-size:0.72rem;color:#a0a0b0;margin-bottom:3px">
                            <span>Confidence score</span><span>{conf}%</span>
                        </div>
                        <div class="conf-bar-bg"><div style="width:{conf}%;background:{bar_color};height:6px;border-radius:4px"></div></div>
                    </div>
                    <div style="margin-top:6px">{tags}</div>
                </div>
                """, unsafe_allow_html=True)
 
 
# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#444;font-size:0.75rem;padding:0.75rem 0">
    🛡️ NoshGuard MVP &nbsp;·&nbsp; FDA Open Data API + USDA FSIS &nbsp;·&nbsp;
    <em>Protecting families from recalled food — one notification at a time.</em>
</div>
""", unsafe_allow_html=True)
 
