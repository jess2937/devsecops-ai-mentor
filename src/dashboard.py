import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="VexilGuard",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #888;
        font-weight: 300;
        margin-bottom: 1rem;
    }

    .grade-card {
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }

    .grade-letter {
        font-size: 5rem;
        font-weight: 700;
        line-height: 1;
    }

    .grade-label {
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 0.5rem;
    }

    .status-blocked {
        background: linear-gradient(135deg, #ff416c, #ff4b2b);
        border-radius: 16px;
        padding: 1.2rem 2rem;
        color: white;
        font-weight: 600;
        font-size: 1rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(255, 65, 108, 0.3);
    }
    
    .status-passed {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        border-radius: 16px;
        padding: 1.2rem 2rem;
        color: white;
        font-weight: 600;
        font-size: 1rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(56, 239, 125, 0.3);
    }

    .metric-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #2a2a4a;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
    }

    .metric-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }

    .metric-label {
        font-size: 0.8rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .section-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #e0e0e0;
        margin: 2rem 0 1rem 0;
    }

    .history-row {
        background: #1a1a2e;
        border: 1px solid #2a2a4a;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .badge-high { background: rgba(255,65,108,0.2); color: #ff416c; }
    .badge-medium { background: rgba(247,151,30,0.2); color: #f7971e; }
    .badge-low { background: rgba(17,153,142,0.2); color: #11998e; }

    .footer {
        text-align: center;
        color: #444;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding: 1rem;
        border-top: 1px solid #1a1a2e;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown("## 🛡️ VexilGuard")
    st.markdown("---")
    st.markdown("### 📊 Scan Metadata")
    st.markdown(f"**🕐 Scan Time:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    st.markdown("**🔧 Scanner Engine:** Bandit v1.8")
    st.markdown("**🔐 Secret Scanner:** Gitleaks")
    st.markdown("**🤖 AI Engine:** Groq LLaMA 3.3")
    st.markdown("**📁 Target:** `src/`")
    st.markdown("**🌿 Branch:** `main`")
    st.markdown("---")
    st.markdown("### ⚙️ Pipeline Tools")
    st.markdown("✅ GitHub Actions")
    st.markdown("✅ Bandit SAST")
    st.markdown("✅ Gitleaks")
    st.markdown("✅ Groq AI")
    st.markdown("✅ Streamlit Dashboard")
    st.markdown("---")
    st.caption("VexilGuard v1.0.0 · Built by Jesinda Rachel")

# ── Hero ──
st.markdown('<p class="hero-title">🛡️ VexilGuard</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">AI-Powered DevSecOps Pipeline — Scans vulnerabilities and teaches you how to fix them</p>', unsafe_allow_html=True)
st.divider()

# ── Load Report ──
report_path = "reports/ai_report.json"

if not os.path.exists(report_path):
    st.warning("⚠️ No security report found. Push code to trigger the pipeline!")
    st.stop()

with open(report_path, "r") as f:
    issues = json.load(f)

total = len(issues)
high = len([i for i in issues if i.get("severity") == "HIGH"])
medium = len([i for i in issues if i.get("severity") == "MEDIUM"])
low = len([i for i in issues if i.get("severity") == "LOW"])

# ── Security Health Score ──
st.markdown('<div class="section-title">🏆 Security Health Score</div>', unsafe_allow_html=True)

if high == 0 and medium == 0:
    grade = "A"
    score = 100
    color = "#38ef7d"
    label = "Excellent — No issues found!"
elif high == 0 and medium <= 2:
    grade = "B"
    score = 75
    color = "#667eea"
    label = "Good — Minor issues to fix"
elif high <= 1:
    grade = "C"
    score = 50
    color = "#f7971e"
    label = "Fair — Critical issues found"
else:
    grade = "F"
    score = 20
    color = "#ff416c"
    label = "Poor — Multiple critical issues!"

col_grade, col_bar = st.columns([1, 3])

with col_grade:
    st.markdown(f'''
    <div class="grade-card" style="background: linear-gradient(135deg, #1a1a2e, #16213e); border: 2px solid {color};">
        <div class="grade-letter" style="color: {color}">{grade}</div>
        <div class="grade-label" style="color: {color}">{label}</div>
    </div>''', unsafe_allow_html=True)

with col_bar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"**Security Score: {score}/100**")
    st.progress(score / 100)
    st.markdown(f"*{high} critical · {medium} medium · {low} low severity issues*")

st.divider()

# ── Status Banner ──
if high > 0:
    st.markdown(f'<div class="status-blocked">🚫 PIPELINE BLOCKED — {high} critical issue(s) detected. Fix before merging.</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-passed">✅ PIPELINE PASSED — No critical vulnerabilities. Safe to merge!</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Metric Cards ──
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'''<div class="metric-card">
        <div class="metric-label">Total Issues</div>
        <div class="metric-number" style="color:#667eea">{total}</div>
    </div>''', unsafe_allow_html=True)

with col2:
    st.markdown(f'''<div class="metric-card">
        <div class="metric-label">🔴 Critical</div>
        <div class="metric-number" style="color:#ff416c">{high}</div>
    </div>''', unsafe_allow_html=True)

with col3:
    st.markdown(f'''<div class="metric-card">
        <div class="metric-label">🟡 Medium</div>
        <div class="metric-number" style="color:#f7971e">{medium}</div>
    </div>''', unsafe_allow_html=True)

with col4:
    st.markdown(f'''<div class="metric-card">
        <div class="metric-label">🟢 Low</div>
        <div class="metric-number" style="color:#11998e">{low}</div>
    </div>''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.divider()

# ── Build History ──
st.markdown('<div class="section-title">📜 Build History</div>', unsafe_allow_html=True)

build_history = [
    {"commit": "ec817e7", "message": "fix: switch to Groq API", "status": "🔴 Blocked", "issues": 3, "time": "2 hours ago"},
    {"commit": "697b643", "message": "feat: add Gemini AI mentor", "status": "🔴 Blocked", "issues": 3, "time": "3 hours ago"},
    {"commit": "306ae31", "message": "fix: ensure reports directory exists", "status": "✅ Passed", "issues": 0, "time": "4 hours ago"},
    {"commit": "0b53383", "message": "fix: upgrade upload-artifact to v4", "status": "✅ Passed", "issues": 0, "time": "5 hours ago"},
    {"commit": "8781da1", "message": "feat: initial project setup", "status": "🔴 Blocked", "issues": 1, "time": "6 hours ago"},
]

for build in build_history:
    col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
    with col1:
        st.code(build["commit"], language="text")
    with col2:
        st.markdown(f"**{build['message']}**")
        st.caption(build["time"])
    with col3:
        st.markdown(f"**Issues:** {build['issues']}")
    with col4:
        st.markdown(build["status"])

st.divider()

# ── Vulnerability Details ──
st.markdown('<div class="section-title">📋 Vulnerability Analysis & AI Fix Recommendations</div>', unsafe_allow_html=True)

for idx, issue in enumerate(issues):
    severity = issue.get("severity", "UNKNOWN")

    if severity == "HIGH":
        icon = "🔴"
        badge_class = "badge-high"
    elif severity == "MEDIUM":
        icon = "🟡"
        badge_class = "badge-medium"
    else:
        icon = "🟢"
        badge_class = "badge-low"

    with st.expander(f"{icon} [{severity}] {issue.get('issue')} — Line {issue.get('line')}"):
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown(f'<span class="badge {badge_class}">{severity}</span>', unsafe_allow_html=True)
            st.markdown("**📁 File**")
            st.code(issue.get("file"), language="text")
            st.markdown("**❌ Vulnerable Code**")
            st.code(issue.get("code"), language="python")

        with col2:
            st.markdown("**🤖 AI Mentor Recommendation**")
            st.info(issue.get("ai_feedback", "No feedback available."))

        # ── Remediation Checklist ──
        st.markdown("---")
        st.markdown("**✅ Developer Remediation Checklist**")

        steps = [
            "Read and understand the vulnerability description above",
            "Review the vulnerable code in your editor",
            "Apply the AI recommended fix",
            "Run the scanner locally to verify the fix",
            "Commit the fix with a descriptive message",
            "Push and confirm pipeline passes"
        ]

        completed = 0
        for step in steps:
            if st.checkbox(step, key=f"check_{idx}_{step}"):
                completed += 1

        progress = completed / len(steps)
        st.progress(progress)

        if completed == len(steps):
            st.success("🎉 All steps completed! You're ready to push your fix.")
        elif completed > 0:
            st.info(f"⏳ {completed}/{len(steps)} steps completed. Keep going!")

st.divider()

# ── Footer ──
st.markdown('<div class="footer">🛡️ VexilGuard v1.0.0 · Built with GitHub Actions • Bandit • Gitleaks • Groq AI • Streamlit</div>', unsafe_allow_html=True)