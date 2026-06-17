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

    .block-container {
        padding: 2rem 3rem !important;
        max-width: 1400px !important;
    }

    /* ── NAV BAR ── */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.2rem 0;
        border-bottom: 1px solid #0d2b0d;
        margin-bottom: 3rem;
    }

    .nav-logo {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: #00ff41;
        letter-spacing: -0.5px;
    }

    .nav-logo span {
        color: #ffffff;
    }

    .nav-links {
        display: flex;
        gap: 2rem;
        font-size: 0.85rem;
        color: #888;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .nav-badge {
        background: #00ff41;
        color: #000;
        padding: 0.4rem 1rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 1px;
    }

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

    .hero-title .accent {
        color: #00ff41;
    }

    .hero-desc {
        font-size: 1.1rem;
        color: #666;
        max-width: 600px;
        line-height: 1.7;
        margin-bottom: 2rem;
    }

    .hero-cta {
        display: inline-block;
        background: #00ff41;
        color: #000;
        padding: 0.8rem 2rem;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.9rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-right: 1rem;
    }

    .hero-cta-outline {
        display: inline-block;
        border: 1px solid #333;
        color: #888;
        padding: 0.8rem 2rem;
        border-radius: 4px;
        font-size: 0.9rem;
        letter-spacing: 1px;
        text-transform: uppercase;
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
    .build-row {
        background: #050f05;
        border: 1px solid #0d2b0d;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        display: grid;
        grid-template-columns: 1fr 3fr 1fr 1fr;
        align-items: center;
        gap: 1rem;
    }

    .commit-hash {
        font-family: monospace;
        color: #00ff41;
        font-size: 0.85rem;
        background: rgba(0,255,65,0.1);
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
    }

    .build-msg {
        color: #ccc;
        font-size: 0.9rem;
    }

    .build-time {
        color: #555;
        font-size: 0.8rem;
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
    }

    .badge-high { background: rgba(255,40,40,0.15); color: #ff4444; border: 1px solid rgba(255,40,40,0.3); }
    .badge-medium { background: rgba(255,165,0,0.15); color: #ffa500; border: 1px solid rgba(255,165,0,0.3); }
    .badge-low { background: rgba(0,255,65,0.1); color: #00ff41; border: 1px solid rgba(0,255,65,0.2); }
    .badge-pass { background: rgba(0,255,65,0.1); color: #00ff41; border: 1px solid rgba(0,255,65,0.2); }
    .badge-fail { background: rgba(255,40,40,0.15); color: #ff4444; border: 1px solid rgba(255,40,40,0.3); }

    /* ── VULN CARDS ── */
    .vuln-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: #fff;
        margin-bottom: 0.3rem;
    }

    /* ── CHECKLIST ── */
    .checklist-title {
        font-size: 0.8rem;
        color: #00ff41;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 1rem 0 0.5rem 0;
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
    }

    .footer-logo {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1rem;
        font-weight: 700;
        color: #00ff41;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    /* Responsive fixes */
@media (max-width: 768px) {
    .hero-title {
        font-size: 2.5rem !important;
        letter-spacing: -1px !important;
    }
    .navbar {
        flex-direction: column;
        gap: 1rem;
        text-align: center;
    }
    .nav-links {
        gap: 1rem;
        flex-wrap: wrap;
        justify-content: center;
    }
    .metric-card {
        margin-bottom: 0.5rem;
    }
    .grade-letter {
        font-size: 4rem;
    }
    .block-container {
        padding: 1rem !important;
    }
}
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

    st.markdown("""
    <div style="font-size: 0.7rem; color: #00ff41; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 1rem;">
        📊 Scan Metadata
    </div>
    """, unsafe_allow_html=True)

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
        <div style="display: flex; justify-content: space-between; padding: 0.4rem 0; border-bottom: 1px solid #0d2b0d;">
            <span style="color: #555; font-size: 0.8rem;">{key}</span>
            <span style="color: #ccc; font-size: 0.8rem; font-family: monospace;">{val}</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style="font-size: 0.7rem; color: #00ff41; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 1rem;">
        ⚙️ Pipeline Stack
    </div>
    """, unsafe_allow_html=True)

    tools = ["GitHub Actions", "Bandit SAST", "Gitleaks", "Groq AI", "Streamlit"]
    for tool in tools:
        st.markdown(f"""
        <div style="padding: 0.4rem 0; font-size: 0.85rem; color: #888;">
            <span style="color: #00ff41; margin-right: 0.5rem;">▸</span>{tool}
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("""
    <div style="font-size: 0.75rem; color: #333; text-align: center;">
        VexilGuard v1.0.0<br>Built by Jesinda Rachel
    </div>
    """, unsafe_allow_html=True)

# ── NAVBAR ──
st.markdown("""
<div class="navbar">
    <div class="nav-logo">Vexil<span>Guard</span></div>
    <div class="nav-links">
        <a href="#dashboard" style="color:#888; text-decoration:none;">Dashboard</a>
        <a href="#history" style="color:#888; text-decoration:none;">History</a>
        <a href="#reports" style="color:#888; text-decoration:none;">Reports</a>
        <a href="#docs" style="color:#888; text-decoration:none;">Docs</a>
    </div>
    <a href="/" style="text-decoration:none;"><div class="nav-badge">⟳ LIVE SCAN</div></a></div>

<div id="dashboard"></div>
""", unsafe_allow_html=True)

# ── LOAD REPORT ──
report_path = "reports/ai_report.json"

if not os.path.exists(report_path):
    st.markdown("""
    <div class="status-blocked">⚠️ No security report found. Push code to trigger the pipeline!</div>
    """, unsafe_allow_html=True)
    st.stop()

with open(report_path, "r") as f:
    issues = json.load(f)

total = len(issues)
high = len([i for i in issues if i.get("severity") == "HIGH"])
medium = len([i for i in issues if i.get("severity") == "MEDIUM"])
low = len([i for i in issues if i.get("severity") == "LOW"])

# ── HERO SECTION ──
col_hero, col_grade = st.columns([2, 1])

with col_hero:
    st.markdown('<div class="hero-tag">🛡️ AI-Powered Security Scanner</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="hero-title">Shift Security<br><span class="accent">Left.</span></div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="hero-desc">
        VexilGuard automatically scans every code push for vulnerabilities, 
        secrets, and security misconfigurations — then teaches your team 
        exactly how to fix them using AI.
    </div>
    """, unsafe_allow_html=True)

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
        <div style="font-size: 0.7rem; color: #555; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 1rem;">Security Health Score</div>
        <div class="grade-letter" style="color: {color}; text-shadow: 0 0 40px {color}40">{grade}</div>
        <div class="grade-score">{score}/100 · {label}</div>
        <div style="margin-top: 1.5rem; height: 4px; background: #0d2b0d; border-radius: 2px;">
            <div style="height: 4px; width: {score}%; background: {color}; border-radius: 2px; box-shadow: 0 0 10px {color}80;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── METRIC CARDS ──
col1, col2, col3, col4 = st.columns(4)

metrics = [
    ("Total Issues", total, "#00ff41"),
    ("🔴 Critical", high, "#ff4444"),
    ("🟡 Medium", medium, "#ffa500"),
    ("🟢 Low", low, "#00ff41"),
]

for col, (label, value, color) in zip([col1, col2, col3, col4], metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-number" style="color:{color}">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ── BUILD HISTORY ──
st.markdown('<div class="section-tag">// build history</div>', unsafe_allow_html=True)
st.markdown('<div id="history"></div><div class="section-title">Pipeline Run Log</div>', unsafe_allow_html=True)
build_history = [
    {"commit": "ec817e7", "message": "fix: switch to Groq API for AI analysis", "status": "BLOCKED", "issues": 3, "time": "2 hours ago"},
    {"commit": "697b643", "message": "feat: add AI mentor analysis to pipeline", "status": "BLOCKED", "issues": 3, "time": "3 hours ago"},
    {"commit": "306ae31", "message": "fix: ensure reports directory exists", "status": "PASSED", "issues": 0, "time": "4 hours ago"},
    {"commit": "0b53383", "message": "fix: upgrade upload-artifact to v4", "status": "PASSED", "issues": 0, "time": "5 hours ago"},
    {"commit": "8781da1", "message": "feat: initial project setup with pipeline", "status": "BLOCKED", "issues": 1, "time": "6 hours ago"},
]

# Header row
col1, col2, col3, col4, col5 = st.columns([1, 3, 1, 1, 1])
for col, header in zip([col1, col2, col3, col4, col5], ["Commit", "Message", "Issues", "Status", "Time"]):
    with col:
        st.markdown(f"<div style='font-size:0.7rem; color:#555; text-transform:uppercase; letter-spacing:1px;'>{header}</div>", unsafe_allow_html=True)

for build in build_history:
    col1, col2, col3, col4, col5 = st.columns([1, 3, 1, 1, 1])
    with col1:
        st.markdown(f'<span class="commit-hash">{build["commit"]}</span>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<span class="build-msg">{build["message"]}</span>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<span style="color:#888; font-size:0.9rem;">{build["issues"]}</span>', unsafe_allow_html=True)
    with col4:
        badge = "badge-fail" if build["status"] == "BLOCKED" else "badge-pass"
        st.markdown(f'<span class="badge {badge}">{build["status"]}</span>', unsafe_allow_html=True)
    with col5:
        st.markdown(f'<span class="build-time">{build["time"]}</span>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ── VULNERABILITY DETAILS ──
st.markdown('<div class="section-tag">// vulnerability analysis</div>', unsafe_allow_html=True)
st.markdown('<div id="reports"></div><div class="section-title">AI Fix Recommendations</div>', unsafe_allow_html=True)

for idx, issue in enumerate(issues):
    severity = issue.get("severity", "UNKNOWN")

    if severity == "HIGH":
        icon, badge_class, border_color = "🔴", "badge-high", "#ff444440"
    elif severity == "MEDIUM":
        icon, badge_class, border_color = "🟡", "badge-medium", "#ffa50040"
    else:
        icon, badge_class, border_color = "🟢", "badge-low", "#00ff4140"

    with st.expander(f"{icon} {issue.get('issue')} — Line {issue.get('line')}"):

        st.markdown(f'<span class="badge {badge_class}">{severity}</span>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown('<div style="font-size:0.7rem; color:#00ff41; text-transform:uppercase; letter-spacing:2px; margin-bottom:0.5rem;">📁 File Location</div>', unsafe_allow_html=True)
            st.code(issue.get("file"), language="text")

            st.markdown('<div style="font-size:0.7rem; color:#ff4444; text-transform:uppercase; letter-spacing:2px; margin-bottom:0.5rem;">❌ Vulnerable Code</div>', unsafe_allow_html=True)
            st.code(issue.get("code"), language="python")

        with col2:
            st.markdown('<div style="font-size:0.7rem; color:#00ff41; text-transform:uppercase; letter-spacing:2px; margin-bottom:0.5rem;">🤖 AI Mentor Says</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background: #050f05; border: 1px solid #0d2b0d; border-radius: 8px; padding: 1rem; font-size: 0.9rem; color: #ccc; line-height: 1.7;">
                {issue.get("ai_feedback", "No feedback available.")}
            </div>
            """, unsafe_allow_html=True)

        # ── REMEDIATION CHECKLIST ──
        st.markdown('<div class="checklist-title">✅ Developer Remediation Checklist</div>', unsafe_allow_html=True)

        steps = [
            "Read and understand the vulnerability description",
            "Review the vulnerable code in your editor",
            "Apply the AI recommended secure fix",
            "Run the scanner locally to verify",
            "Commit fix with a descriptive message",
            "Push and confirm pipeline passes ✅"
        ]

        completed = 0
        for step in steps:
            if st.checkbox(step, key=f"check_{idx}_{step}"):
                completed += 1

        progress = completed / len(steps)
        st.progress(progress)

        if completed == len(steps):
            st.markdown('<div class="status-passed">🎉 All steps done! Ready to push your fix.</div>', unsafe_allow_html=True)
        elif completed > 0:
            st.markdown(f'<div style="font-size:0.85rem; color:#555;">⏳ {completed}/{len(steps)} steps completed</div>', unsafe_allow_html=True)

st.markdown('<div id="docs"></div>', unsafe_allow_html=True)

# ── FOOTER ──
st.markdown("""
<div class="footer">
    <div class="footer-logo">🛡️ VexilGuard</div>
    <div>GitHub Actions · Bandit · Gitleaks · Groq AI · Streamlit</div>
    <div>v1.0.0 · Built by Jesinda Rachel</div>
</div>
""", unsafe_allow_html=True)