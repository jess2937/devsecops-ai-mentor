import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="VexilGuard",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    /* Force dark theme always */
    html, body, [class*="css"], .stApp, .main, section[data-testid="stSidebar"] {
        font-family: 'Inter', sans-serif !important;
        background-color: #030a03 !important;
        color: #e0e0e0 !important;
    }

    .block-container {
        padding: 2rem 3rem !important;
        max-width: 1400px !important;
        background-color: #030a03 !important;
    }

    /* Shield background */
    .main::before {
        content: '🛡';
        position: fixed;
        top: 50%;
        right: -5%;
        transform: translateY(-50%);
        font-size: 40rem;
        opacity: 0.015;
        z-index: 0;
        pointer-events: none;
        filter: blur(2px);
    }

    /* Force all text dark */
    p, span, div, h1, h2, h3, h4, h5, h6, label {
        color: inherit !important;
    }

    /* Streamlit elements dark override */
    .stExpander {
        background: #050f05 !important;
        border: 1px solid #0d2b0d !important;
        border-radius: 12px !important;
    }

    .stExpander summary {
        color: #e0e0e0 !important;
        background: #050f05 !important;
    }

    .stCheckbox label {
        color: #aaa !important;
        font-size: 0.9rem !important;
    }

    .stProgress > div > div {
        background: #00ff41 !important;
    }

    .stProgress {
        background: #0d2b0d !important;
    }

    code, .stCode {
        background: #050f05 !important;
        color: #00ff41 !important;
    }

    /* ── NAVBAR ── */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.2rem 0;
        border-bottom: 1px solid #0d2b0d;
        margin-bottom: 3rem;
        flex-wrap: wrap;
        gap: 1rem;
        background: transparent;
    }

    .nav-logo {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: #00ff41 !important;
        letter-spacing: -0.5px;
    }

    .nav-logo span { color: #ffffff !important; }

    .nav-links {
        display: flex;
        gap: 2rem;
        font-size: 0.85rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        flex-wrap: wrap;
        justify-content: center;
    }

    .nav-links a {
        color: #888 !important;
        text-decoration: none !important;
        transition: color 0.2s;
    }

    .nav-links a:hover { color: #00ff41 !important; }

    .nav-badge {
        background: #00ff41;
        color: #000 !important;
        padding: 0.4rem 1rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 1px;
        cursor: pointer;
    }

    /* ── HERO ── */
    .hero-tag {
        display: inline-block;
        border: 1px solid #00ff41;
        color: #00ff41 !important;
        padding: 0.3rem 1rem;
        border-radius: 4px;
        font-size: 0.75rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
    }

    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 4.5rem;
        font-weight: 800;
        line-height: 1.05;
        color: #ffffff !important;
        margin-bottom: 1rem;
        letter-spacing: -2px;
    }

    .hero-title .accent { color: #00ff41 !important; }

    .hero-desc {
        font-size: 1.1rem;
        color: #666 !important;
        max-width: 600px;
        line-height: 1.7;
        margin-bottom: 2rem;
    }

    /* ── STATUS ── */
    .status-blocked {
        background: linear-gradient(90deg, rgba(255,40,40,0.15), transparent);
        border-left: 3px solid #ff2828;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.5rem;
        color: #ff6b6b !important;
        font-weight: 600;
        font-size: 0.95rem;
        margin: 1.5rem 0;
    }

    .status-passed {
        background: linear-gradient(90deg, rgba(0,255,65,0.1), transparent);
        border-left: 3px solid #00ff41;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.5rem;
        color: #00ff41 !important;
        font-weight: 600;
        font-size: 0.95rem;
        margin: 1.5rem 0;
    }

    /* ── GRADE CARD ── */
    .grade-wrapper {
        background: #050f05;
        border: 1px solid #0d2b0d;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
    }

    .grade-letter {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 6rem;
        font-weight: 800;
        line-height: 1;
    }

    .grade-score {
        font-size: 0.85rem;
        color: #888 !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 0.5rem;
    }

    /* ── METRIC CARDS ── */
    .metric-card {
        background: #050f05;
        border: 1px solid #0d2b0d;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .metric-number {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0.3rem 0;
        line-height: 1;
    }

    .metric-label {
        font-size: 0.75rem;
        color: #555 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* ── SECTION TITLES ── */
    .section-tag {
        font-size: 0.7rem;
        color: #00ff41 !important;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 0.5rem;
    }

    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff !important;
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
    }

    /* ── BUILD HISTORY TABLE ── */
    .build-table-wrapper {
        background: #050f05;
        border: 1px solid #0d2b0d;
        border-radius: 12px;
        overflow: hidden;
    }

    .build-table-header {
        display: grid;
        grid-template-columns: 120px 1fr 80px 100px 80px;
        padding: 0.8rem 1.5rem;
        border-bottom: 1px solid #0d2b0d;
        gap: 1rem;
    }

    .build-table-header span {
        font-size: 0.65rem;
        color: #444 !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    .build-table-row {
        display: grid;
        grid-template-columns: 120px 1fr 80px 100px 80px;
        padding: 1rem 1.5rem;
        border-bottom: 1px solid #0a1a0a;
        gap: 1rem;
        align-items: center;
        transition: background 0.2s;
    }

    .build-table-row:last-child { border-bottom: none; }
    .build-table-row:hover { background: #070f07; }

    .commit-hash {
        font-family: monospace;
        color: #00ff41 !important;
        font-size: 0.85rem;
        background: rgba(0,255,65,0.08);
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        border: 1px solid rgba(0,255,65,0.15);
        display: inline-block;
    }

    .build-msg { color: #ccc !important; font-size: 0.88rem; }
    .build-time { color: #444 !important; font-size: 0.8rem; }
    .build-count { color: #888 !important; font-size: 0.88rem; }

    /* ── BADGES ── */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.7rem;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .badge-high { background: rgba(255,40,40,0.15); color: #ff4444 !important; border: 1px solid rgba(255,40,40,0.3); }
    .badge-medium { background: rgba(255,165,0,0.15); color: #ffa500 !important; border: 1px solid rgba(255,165,0,0.3); }
    .badge-low { background: rgba(0,255,65,0.1); color: #00ff41 !important; border: 1px solid rgba(0,255,65,0.2); }
    .badge-pass { background: rgba(0,255,65,0.1); color: #00ff41 !important; border: 1px solid rgba(0,255,65,0.2); }
    .badge-fail { background: rgba(255,40,40,0.15); color: #ff4444 !important; border: 1px solid rgba(255,40,40,0.3); }

    /* ── VULN CARDS ── */
    .vuln-card {
        background: #050f05;
        border: 1px solid #0d2b0d;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .vuln-card-high { border-left: 3px solid #ff4444; }
    .vuln-card-medium { border-left: 3px solid #ffa500; }
    .vuln-card-low { border-left: 3px solid #00ff41; }

    .vuln-card-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: #fff !important;
        margin-bottom: 0.3rem;
    }

    .vuln-card-meta {
        font-size: 0.78rem;
        color: #555 !important;
        margin-bottom: 1rem;
    }

    .vuln-section-label {
        font-size: 0.65rem;
        color: #555 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.4rem;
    }

    .ai-feedback-box {
        background: #030a03;
        border: 1px solid #0d2b0d;
        border-radius: 8px;
        padding: 1rem;
        font-size: 0.88rem;
        color: #aaa !important;
        line-height: 1.7;
        height: 100%;
    }

    /* ── REMEDIATION ── */
    .remediation-card {
        background: #050f05;
        border: 1px solid #0d2b0d;
        border-left: 3px solid #00ff41;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .remediation-issue-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: #fff !important;
        margin-bottom: 0.3rem;
    }

    .remediation-issue-meta {
        font-size: 0.78rem;
        color: #555 !important;
        margin-bottom: 1rem;
    }

    /* ── FOOTER ── */
    .footer {
        margin-top: 4rem;
        padding: 2rem 0;
        border-top: 1px solid #0d2b0d;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #333 !important;
        font-size: 0.8rem;
        flex-wrap: wrap;
        gap: 1rem;
    }

    .footer-logo {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1rem;
        font-weight: 700;
        color: #00ff41 !important;
    }

    /* ── RESPONSIVE ── */
    @media (max-width: 768px) {
        .hero-title { font-size: 2.5rem !important; letter-spacing: -1px !important; }
        .navbar { flex-direction: column; text-align: center; }
        .nav-links { gap: 1rem; justify-content: center; }
        .block-container { padding: 1rem !important; }
        .grade-letter { font-size: 4rem !important; }
        .section-title { font-size: 1.5rem !important; }
        .build-table-header, .build-table-row {
            grid-template-columns: 90px 1fr 60px 80px;
        }
        .build-table-header span:last-child,
        .build-table-row div:last-child { display: none; }
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0; background:#030a03;">
        <div style="font-family:Space Grotesk; font-size:1.3rem; font-weight:700; color:#00ff41; margin-bottom:0.3rem;">🛡️ VexilGuard</div>
        <div style="font-size:0.75rem; color:#555; letter-spacing:2px; text-transform:uppercase;">Security Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown('<div style="font-size:0.7rem; color:#00ff41; text-transform:uppercase; letter-spacing:2px; margin-bottom:1rem;">📊 Scan Metadata</div>', unsafe_allow_html=True)

    metadata = {
        "🕐 Scan Time": datetime.now().strftime('%Y-%m-%d %H:%M'),
        "🔧 SAST Engine": "Bandit v1.8",
        "🔐 Secret Scanner": "Gitleaks",
        "🤖 AI Engine": "Groq LLaMA 3.3",
        "📁 Target": "src/",
        "🌿 Branch": "main",
        "⚙️ Trigger": "git push"
    }

    for key, val in metadata.items():
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px solid #0d2b0d;">
            <span style="color:#555; font-size:0.8rem;">{key}</span>
            <span style="color:#ccc; font-size:0.8rem; font-family:monospace;">{val}</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown('<div style="font-size:0.7rem; color:#00ff41; text-transform:uppercase; letter-spacing:2px; margin-bottom:1rem;">⚙️ Pipeline Stack</div>', unsafe_allow_html=True)

    for tool in ["GitHub Actions", "Bandit SAST", "Gitleaks", "Groq AI", "Streamlit"]:
        st.markdown(f'<div style="padding:0.4rem 0; font-size:0.85rem; color:#888;"><span style="color:#00ff41; margin-right:0.5rem;">▸</span>{tool}</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown('<div style="font-size:0.75rem; color:#333; text-align:center;">VexilGuard v1.0.0<br>Built by Jesinda Rachel</div>', unsafe_allow_html=True)

# ── NAVBAR ──
st.markdown("""
<div class="navbar">
    <div class="nav-logo">Vexil<span>Guard</span></div>
    <div class="nav-links">
        <a href="#dashboard">Dashboard</a>
        <a href="#history">History</a>
        <a href="#reports">Reports</a>
        <a href="#remediation">Remediation</a>
    </div>
    <a href="/" style="text-decoration:none;"><div class="nav-badge">⟳ LIVE SCAN</div></a>
</div>
<div id="dashboard"></div>
""", unsafe_allow_html=True)

# ── LOAD REPORT ──
report_path = "reports/ai_report.json"

if not os.path.exists(report_path):
    st.markdown('<div class="status-blocked">⚠️ No security report found. Push code to trigger the pipeline!</div>', unsafe_allow_html=True)
    st.stop()

with open(report_path, "r") as f:
    issues = json.load(f)

total = len(issues)
high = len([i for i in issues if i.get("severity") == "HIGH"])
medium = len([i for i in issues if i.get("severity") == "MEDIUM"])
low = len([i for i in issues if i.get("severity") == "LOW"])

# ── HERO ──
col_hero, col_grade = st.columns([2, 1])

with col_hero:
    st.markdown('<div class="hero-tag">🛡️ AI-Powered Security Scanner</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Shift Security<br><span class="accent">Left.</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-desc">VexilGuard automatically scans every code push for vulnerabilities, secrets, and security misconfigurations — then teaches your team exactly how to fix them using AI.</div>', unsafe_allow_html=True)

    if high > 0:
        st.markdown(f'<div class="status-blocked">🚫 PIPELINE BLOCKED — {high} critical issue(s) found. You\'re close — just fix these and you\'re good to go!</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-passed">✅ PIPELINE PASSED — Excellent work! Your code is clean and safe to merge.</div>', unsafe_allow_html=True)

with col_grade:
    if high == 0 and medium == 0:
        grade, score, color, label = "A", 100, "#00ff41", "Excellent"
    elif high == 0 and medium <= 2:
        grade, score, color, label = "B", 75, "#7fff00", "Good"
    elif high <= 1:
        grade, score, color, label = "C", 50, "#ffa500", "Fair"
    else:
        grade, score, color, label = "F", 20, "#ff4444", "Needs Work"

    st.markdown(f"""
    <div class="grade-wrapper">
        <div style="font-size:0.7rem; color:#555; text-transform:uppercase; letter-spacing:2px; margin-bottom:1rem;">Security Health Score</div>
        <div class="grade-letter" style="color:{color}; text-shadow:0 0 40px {color}40">{grade}</div>
        <div class="grade-score">{score}/100 · {label}</div>
        <div style="margin-top:1.5rem; height:4px; background:#0d2b0d; border-radius:2px;">
            <div style="height:4px; width:{score}%; background:{color}; border-radius:2px; box-shadow:0 0 10px {color}80;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── METRICS ──
col1, col2, col3, col4 = st.columns(4)
metrics = [("Total Issues", total, "#00ff41"), ("🔴 Critical", high, "#ff4444"), ("🟡 Medium", medium, "#ffa500"), ("🟢 Low", low, "#00ff41")]
for col, (label, value, color) in zip([col1, col2, col3, col4], metrics):
    with col:
        st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-number" style="color:{color}">{value}</div></div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ── BUILD HISTORY ──
st.markdown('<div id="history"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-tag">// build history</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Pipeline Run Log</div>', unsafe_allow_html=True)
st.markdown('<div style="font-size:0.9rem; color:#555; margin-bottom:1.5rem;">Every push is tracked. Watch your security score improve over time as you fix issues! 💪</div>', unsafe_allow_html=True)

build_history = [
    {"commit": "ec817e7", "message": "fix: switch to Groq API for AI analysis", "status": "BLOCKED", "issues": 3, "time": "2h ago"},
    {"commit": "697b643", "message": "feat: add AI mentor to pipeline", "status": "BLOCKED", "issues": 3, "time": "3h ago"},
    {"commit": "306ae31", "message": "fix: ensure reports directory exists", "status": "PASSED", "issues": 0, "time": "4h ago"},
    {"commit": "0b53383", "message": "fix: upgrade artifact action to v4", "status": "PASSED", "issues": 0, "time": "5h ago"},
    {"commit": "8781da1", "message": "feat: initial pipeline setup", "status": "BLOCKED", "issues": 1, "time": "6h ago"},
]

# Table header
st.markdown("""
<div class="build-table-wrapper">
    <div class="build-table-header">
        <span>Commit</span>
        <span>Message</span>
        <span>Issues</span>
        <span>Status</span>
        <span>Time</span>
    </div>
""", unsafe_allow_html=True)

for build in build_history:
    badge = "badge-fail" if build["status"] == "BLOCKED" else "badge-pass"
    st.markdown(f"""
    <div class="build-table-row">
        <div><span class="commit-hash">{build['commit']}</span></div>
        <div class="build-msg">{build['message']}</div>
        <div class="build-count">{build['issues']}</div>
        <div><span class="badge {badge}">{build['status']}</span></div>
        <div class="build-time">{build['time']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ── VULNERABILITY CARDS ──
st.markdown('<div id="reports"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-tag">// vulnerability analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">AI Fix Recommendations</div>', unsafe_allow_html=True)
st.markdown('<div style="font-size:0.9rem; color:#555; margin-bottom:1.5rem;">Great news — every issue below has a clear fix waiting for you. AI has already done the hard part! 🚀</div>', unsafe_allow_html=True)

for idx, issue in enumerate(issues):
    severity = issue.get("severity", "UNKNOWN")

    if severity == "HIGH":
        icon, badge_class, card_class = "🔴", "badge-high", "vuln-card-high"
    elif severity == "MEDIUM":
        icon, badge_class, card_class = "🟡", "badge-medium", "vuln-card-medium"
    else:
        icon, badge_class, card_class = "🟢", "badge-low", "vuln-card-low"

    st.markdown(f"""
    <div class="vuln-card {card_class}">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:0.5rem;">
            <div>
                <div class="vuln-card-title">{icon} {issue.get('issue')}</div>
                <div class="vuln-card-meta">📁 {issue.get('file')} &nbsp;·&nbsp; Line {issue.get('line')}</div>
            </div>
            <span class="badge {badge_class}">{severity}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="vuln-section-label">❌ Vulnerable Code — spot what\'s wrong</div>', unsafe_allow_html=True)
        st.code(issue.get("code"), language="python")

    with col2:
        st.markdown('<div class="vuln-section-label">🤖 Your AI mentor has a fix ready</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ai-feedback-box">{issue.get("ai_feedback", "No feedback available.")}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

# ── REMEDIATION SECTION ──
st.markdown('<div id="remediation"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-tag">// developer tools</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Remediation Sandbox</div>', unsafe_allow_html=True)
st.markdown('<div style="font-size:0.9rem; color:#555; margin-bottom:1.5rem;">You\'ve got this! Check off each step as you go — watch that progress bar fill up to 100% 🎯</div>', unsafe_allow_html=True)

# Global remediation steps — shown once
steps = [
    "📖 Read and understand each vulnerability description above",
    "🖊️ Open the affected file in your code editor",
    "🔧 Apply the AI recommended secure fix for each issue",
    "🔍 Run Bandit locally to verify: `bandit -r src/`",
    "💾 Commit your fix with a clear message",
    "🚀 Push to GitHub and watch the pipeline turn green!"
]

st.markdown("""
<div class="remediation-card">
    <div class="remediation-issue-title">🛠️ Your Fix Checklist</div>
    <div class="remediation-issue-meta">Work through these steps for all issues above. You're one push away from a green pipeline!</div>
</div>
""", unsafe_allow_html=True)

completed = 0
for step in steps:
    if st.checkbox(step, key=f"global_step_{step[:30]}"):
        completed += 1

progress = completed / len(steps)
st.progress(progress)

if completed == len(steps):
    st.markdown('<div class="status-passed">🎉 Amazing work! All steps done — push your fix and celebrate that green pipeline! 🟢</div>', unsafe_allow_html=True)
elif completed > 0:
    st.markdown(f'<div style="font-size:0.85rem; color:#555; margin-top:0.5rem;">⏳ {completed}/{len(steps)} steps done — you\'re making great progress, keep going!</div>', unsafe_allow_html=True)
else:
    st.markdown('<div style="font-size:0.85rem; color:#555; margin-top:0.5rem;">👆 Start checking off steps as you fix the issues above!</div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ── FOOTER ──
st.markdown("""
<div class="footer">
    <div class="footer-logo">🛡️ VexilGuard</div>
    <div style="color:#333;">GitHub Actions · Bandit · Gitleaks · Groq AI · Streamlit</div>
    <div style="color:#333;">v1.0.0 · Built by Jesinda Rachel</div>
</div>
""", unsafe_allow_html=True)