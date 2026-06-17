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

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #030a03 !important;
        color: #e0e0e0;
    }

    /* Background shield pattern */
    .main .block-container {
        background-image: 
            radial-gradient(circle at 80% 20%, rgba(0,255,65,0.03) 0%, transparent 50%),
            radial-gradient(circle at 20% 80%, rgba(0,255,65,0.02) 0%, transparent 50%);
        position: relative;
    }

    .main .block-container::before {
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

    .block-container {
        padding: 2rem 3rem !important;
        max-width: 1400px !important;
        position: relative;
        z-index: 1;
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
    }

    .nav-logo {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: #00ff41;
        letter-spacing: -0.5px;
    }

    .nav-logo span { color: #ffffff; }

    .nav-links {
        display: flex;
        gap: 2rem;
        font-size: 0.85rem;
        color: #888;
        letter-spacing: 1px;
        text-transform: uppercase;
        flex-wrap: wrap;
        justify-content: center;
    }

    .nav-links a:hover { color: #00ff41 !important; transition: color 0.2s; }

    .nav-badge {
        background: #00ff41;
        color: #000;
        padding: 0.4rem 1rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 1px;
        cursor: pointer;
        transition: all 0.2s;
    }

    .nav-badge:hover { background: #00cc33; }

    /* ── HERO ── */
    .hero-tag {
        display: inline-block;
        border: 1px solid #00ff41;
        color: #00ff41;
        padding: 0.3rem 1rem;
        border-radius: 4px;
        font-size: 0.75rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
    }

    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 4.5rem !important;
        font-weight: 800 !important;
        line-height: 1.05 !important;
        color: #ffffff !important;
        margin-bottom: 1rem !important;
        letter-spacing: -2px !important;
    }

    .hero-title .accent { color: #00ff41; }

    .hero-desc {
        font-size: 1.1rem;
        color: #666;
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
        color: #ff6b6b;
        font-weight: 600;
        font-size: 0.95rem;
        margin: 1.5rem 0;
    }

    .status-passed {
        background: linear-gradient(90deg, rgba(0,255,65,0.1), transparent);
        border-left: 3px solid #00ff41;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.5rem;
        color: #00ff41;
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
        position: relative;
        overflow: hidden;
    }

    .grade-wrapper::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(0,255,65,0.05) 0%, transparent 60%);
    }

    .grade-letter {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 6rem;
        font-weight: 800;
        line-height: 1;
    }

    .grade-score {
        font-size: 0.85rem;
        color: #888;
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
        position: relative;
        overflow: hidden;
        margin-bottom: 0.5rem;
    }

    .metric-card::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff41, transparent);
        opacity: 0.4;
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
        color: #555;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* ── SECTION TITLES ── */
    .section-tag {
        font-size: 0.7rem;
        color: #00ff41;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 0.5rem;
    }

    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
    }

    /* ── BUILD HISTORY ── */
    .build-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.88rem;
    }

    .build-table th {
        font-size: 0.7rem;
        color: #555;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 0.6rem 1rem;
        text-align: left;
        border-bottom: 1px solid #0d2b0d;
    }

    .build-table td {
        padding: 0.9rem 1rem;
        border-bottom: 1px solid #0d2b0d;
        color: #aaa;
        vertical-align: middle;
    }

    .build-table tr:hover td {
        background: #050f05;
    }

    .commit-hash {
        font-family: monospace;
        color: #00ff41;
        font-size: 0.85rem;
        background: rgba(0,255,65,0.1);
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        white-space: nowrap;
    }

    /* ── BADGES ── */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.7rem;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        white-space: nowrap;
    }

    .badge-high { background: rgba(255,40,40,0.15); color: #ff4444; border: 1px solid rgba(255,40,40,0.3); }
    .badge-medium { background: rgba(255,165,0,0.15); color: #ffa500; border: 1px solid rgba(255,165,0,0.3); }
    .badge-low { background: rgba(0,255,65,0.1); color: #00ff41; border: 1px solid rgba(0,255,65,0.2); }
    .badge-pass { background: rgba(0,255,65,0.1); color: #00ff41; border: 1px solid rgba(0,255,65,0.2); }
    .badge-fail { background: rgba(255,40,40,0.15); color: #ff4444; border: 1px solid rgba(255,40,40,0.3); }

    /* ── VULN CARDS (NEW FORMAT) ── */
    .vuln-card {
        background: #050f05;
        border: 1px solid #0d2b0d;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
    }

    .vuln-card-high { border-left: 3px solid #ff4444; }
    .vuln-card-medium { border-left: 3px solid #ffa500; }
    .vuln-card-low { border-left: 3px solid #00ff41; }

    .vuln-card-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: #fff;
        margin-bottom: 0.3rem;
    }

    .vuln-card-meta {
        font-size: 0.78rem;
        color: #555;
        margin-bottom: 1rem;
    }

    .vuln-section-label {
        font-size: 0.65rem;
        color: #555;
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
        color: #aaa;
        line-height: 1.7;
    }

    /* ── REMEDIATION ── */
    .remediation-section {
        background: #050f05;
        border: 1px solid #0d2b0d;
        border-radius: 12px;
        padding: 2rem;
        margin-top: 2rem;
    }

    .remediation-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.3rem;
    }

    .remediation-subtitle {
        font-size: 0.85rem;
        color: #555;
        margin-bottom: 1.5rem;
    }

    .checklist-item-label {
        font-size: 0.7rem;
        color: #00ff41;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 1.5rem 0 0.5rem 0;
    }

    /* ── FOOTER ── */
    .footer {
        margin-top: 4rem;
        padding: 2rem 0;
        border-top: 1px solid #0d2b0d;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #333;
        font-size: 0.8rem;
        flex-wrap: wrap;
        gap: 1rem;
    }

    .footer-logo {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1rem;
        font-weight: 700;
        color: #00ff41;
    }

    /* ── RESPONSIVE ── */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem !important;
            letter-spacing: -1px !important;
        }
        .navbar {
            flex-direction: column;
            text-align: center;
        }
        .nav-links {
            gap: 1rem;
            justify-content: center;
        }
        .block-container {
            padding: 1rem !important;
        }
        .grade-letter { font-size: 4rem; }
        .section-title { font-size: 1.5rem; }
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0;">
        <div style="font-family: Space Grotesk; font-size: 1.3rem; font-weight: 700; color: #00ff41; margin-bottom: 0.3rem;">🛡️ VexilGuard</div>
        <div style="font-size: 0.75rem; color: #555; letter-spacing: 2px; text-transform: uppercase;">Security Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown('<div style="font-size: 0.7rem; color: #00ff41; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 1rem;">📊 Scan Metadata</div>', unsafe_allow_html=True)

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

    st.markdown('<div style="font-size: 0.7rem; color: #00ff41; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 1rem;">⚙️ Pipeline Stack</div>', unsafe_allow_html=True)

    for tool in ["GitHub Actions", "Bandit SAST", "Gitleaks", "Groq AI", "Streamlit"]:
        st.markdown(f'<div style="padding:0.4rem 0; font-size:0.85rem; color:#888;"><span style="color:#00ff41; margin-right:0.5rem;">▸</span>{tool}</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown('<div style="font-size:0.75rem; color:#333; text-align:center;">VexilGuard v1.0.0<br>Built by Jesinda Rachel</div>', unsafe_allow_html=True)

# ── NAVBAR ──
st.markdown("""
<div class="navbar">
    <div class="nav-logo">Vexil<span>Guard</span></div>
    <div class="nav-links">
        <a href="#dashboard" style="color:#888; text-decoration:none;">Dashboard</a>
        <a href="#history" style="color:#888; text-decoration:none;">History</a>
        <a href="#reports" style="color:#888; text-decoration:none;">Reports</a>
        <a href="#remediation" style="color:#888; text-decoration:none;">Remediation</a>
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
        st.markdown(f'<div class="status-blocked">🚫 PIPELINE BLOCKED — {high} critical issue(s) detected. Review required before merge.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-passed">✅ PIPELINE PASSED — No critical vulnerabilities detected. Safe to merge!</div>', unsafe_allow_html=True)

with col_grade:
    if high == 0 and medium == 0:
        grade, score, color, label = "A", 100, "#00ff41", "Excellent"
    elif high == 0 and medium <= 2:
        grade, score, color, label = "B", 75, "#7fff00", "Good"
    elif high <= 1:
        grade, score, color, label = "C", 50, "#ffa500", "Fair"
    else:
        grade, score, color, label = "F", 20, "#ff4444", "Critical"

    st.markdown(f"""
    <div class="grade-wrapper">
        <div style="font-size:0.7rem; color:#555; text-transform:uppercase; letter-spacing:2px; margin-bottom:1rem;">Security Health Score</div>
        <div class="grade-letter" style="color:{color}; text-shadow: 0 0 40px {color}40">{grade}</div>
        <div class="grade-score">{score}/100 · {label}</div>
        <div style="margin-top:1.5rem; height:4px; background:#0d2b0d; border-radius:2px;">
            <div style="height:4px; width:{score}%; background:{color}; border-radius:2px; box-shadow: 0 0 10px {color}80;"></div>
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

build_history = [
    {"commit": "ec817e7", "message": "fix: switch to Groq API for AI analysis", "status": "BLOCKED", "issues": 3, "time": "2h ago"},
    {"commit": "697b643", "message": "feat: add AI mentor analysis to pipeline", "status": "BLOCKED", "issues": 3, "time": "3h ago"},
    {"commit": "306ae31", "message": "fix: ensure reports directory exists", "status": "PASSED", "issues": 0, "time": "4h ago"},
    {"commit": "0b53383", "message": "fix: upgrade upload-artifact to v4", "status": "PASSED", "issues": 0, "time": "5h ago"},
    {"commit": "8781da1", "message": "feat: initial project setup with pipeline", "status": "BLOCKED", "issues": 1, "time": "6h ago"},
]

table_html = """
<div style="overflow-x: auto;">
<table class="build-table">
    <thead>
        <tr>
            <th>Commit</th>
            <th>Message</th>
            <th>Issues</th>
            <th>Status</th>
            <th>Time</th>
        </tr>
    </thead>
    <tbody>
"""

for build in build_history:
    badge = "badge-fail" if build["status"] == "BLOCKED" else "badge-pass"
    table_html += f"""
        <tr>
            <td><span class="commit-hash">{build['commit']}</span></td>
            <td>{build['message']}</td>
            <td style="color:#888;">{build['issues']}</td>
            <td><span class="badge {badge}">{build['status']}</span></td>
            <td style="color:#555; font-size:0.8rem;">{build['time']}</td>
        </tr>
    """

table_html += "</tbody></table></div>"
st.markdown(table_html, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ── VULNERABILITY CARDS ──
st.markdown('<div id="reports"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-tag">// vulnerability analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">AI Fix Recommendations</div>', unsafe_allow_html=True)

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
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:0.5rem; margin-bottom:0.8rem;">
            <div>
                <div class="vuln-card-title">{icon} {issue.get('issue')}</div>
                <div class="vuln-card-meta">📁 {issue.get('file')} · Line {issue.get('line')}</div>
            </div>
            <span class="badge {badge_class}">{severity}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="vuln-section-label">❌ Vulnerable Code</div>', unsafe_allow_html=True)
        st.code(issue.get("code"), language="python")

    with col2:
        st.markdown('<div class="vuln-section-label">🤖 AI Mentor Says</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ai-feedback-box">{issue.get("ai_feedback", "No feedback available.")}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

# ── REMEDIATION SECTION ──
st.markdown('<div id="remediation"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-tag">// developer tools</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Remediation Sandbox</div>', unsafe_allow_html=True)

st.markdown("""
<div style="font-size:0.95rem; color:#666; margin-bottom:1.5rem;">
    Work through each vulnerability fix step by step. Track your progress and confirm when each issue is resolved.
</div>
""", unsafe_allow_html=True)

for idx, issue in enumerate(issues):
    severity = issue.get("severity", "UNKNOWN")
    if severity == "HIGH":
        icon, card_class = "🔴", "vuln-card-high"
    elif severity == "MEDIUM":
        icon, card_class = "🟡", "vuln-card-medium"
    else:
        icon, card_class = "🟢", "vuln-card-low"

    with st.expander(f"{icon} Fix #{idx+1} — {issue.get('issue')} (Line {issue.get('line')})"):
        st.markdown(f'<div style="font-size:0.8rem; color:#555; margin-bottom:1rem;">Follow these steps to resolve this {severity.lower()} severity issue.</div>', unsafe_allow_html=True)

        steps = [
            "Read and understand the vulnerability description above",
            "Open the file in your code editor",
            "Apply the AI recommended secure fix",
            "Run Bandit locally to verify: `bandit -r src/`",
            "Commit fix with message: `fix: resolve {issue}`",
            "Push and confirm pipeline passes ✅"
        ]

        completed = 0
        for step in steps:
            if st.checkbox(step.replace("{issue}", issue.get('issue', '')[:30]), key=f"rem_{idx}_{step[:20]}"):
                completed += 1

        progress = completed / len(steps)
        st.progress(progress)

        if completed == len(steps):
            st.markdown('<div class="status-passed">🎉 All steps done! Push your fix and watch the pipeline go green.</div>', unsafe_allow_html=True)
        elif completed > 0:
            st.markdown(f'<div style="font-size:0.85rem; color:#555; margin-top:0.5rem;">⏳ {completed}/{len(steps)} steps completed — keep going!</div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ── FOOTER ──
st.markdown("""
<div class="footer">
    <div class="footer-logo">🛡️ VexilGuard</div>
    <div>GitHub Actions · Bandit · Gitleaks · Groq AI · Streamlit</div>
    <div>v1.0.0 · Built by Jesinda Rachel</div>
</div>
""", unsafe_allow_html=True)