import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
from datetime import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="VexilGuard",
    page_icon="🛡️",
    layout="wide"
)

# =========================
# SESSION STATE
# =========================
def init_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_role" not in st.session_state:
        st.session_state.user_role = "developer"
    if "completed_steps" not in st.session_state:
        st.session_state.completed_steps = {}
    if "demo_issues" not in st.session_state:
        st.session_state.demo_issues = []


# =========================
# CACHED HELPERS
# =========================
@st.cache_data(ttl=300)
def load_report(report_path):
    if not os.path.exists(report_path):
        return None
    with open(report_path, "r") as f:
        return json.load(f)


@st.cache_data(ttl=300)
def calculate_metrics(issues):
    if not issues:
        return {"total": 0, "high": 0, "medium": 0, "low": 0}

    return {
        "total": len(issues),
        "high": len([i for i in issues if i.get("severity") == "HIGH"]),
        "medium": len([i for i in issues if i.get("severity") == "MEDIUM"]),
        "low": len([i for i in issues if i.get("severity") == "LOW"]),
    }


@st.cache_data(ttl=300)
def get_severity_distribution(issues):
    if not issues:
        return {"HIGH": 0, "MEDIUM": 0, "LOW": 0}

    dist = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for issue in issues:
        sev = issue.get("severity", "LOW")
        if sev in dist:
            dist[sev] += 1
    return dist


@st.cache_data(ttl=300)
def get_issue_types(issues):
    if not issues:
        return {}

    types = {}
    for issue in issues:
        name = issue.get("issue", "Unknown")
        types[name] = types.get(name, 0) + 1
    return types


def export_to_csv(issues):
    if not issues:
        return None
    df = pd.DataFrame(issues)
    return df.to_csv(index=False)


def export_to_json(issues):
    if not issues:
        return None
    return json.dumps(issues, indent=2)


# =========================
# THEME
# =========================
def apply_theme():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

        html, body, [class*="css"], .stApp, .main, section[data-testid="stSidebar"] {
            font-family: 'Inter', sans-serif !important;
            background-color: #030a03 !important;
            color: #e0e0e0 !important;
        }

        .block-container {
            padding: 2rem 3rem !important;
            max-width: 1400px !important;
        }

        .main::before {
            content: '🛡';
            position: fixed;
            top: 50%;
            right: -5%;
            transform: translateY(-50%);
            font-size: 38rem;
            opacity: 0.015;
            z-index: 0;
            pointer-events: none;
            filter: blur(2px);
        }

        p, span, div, h1, h2, h3, h4, h5, h6, label {
            color: inherit !important;
        }

        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.2rem 0;
            border-bottom: 1px solid #0d2b0d;
            margin-bottom: 2rem;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .nav-logo {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.6rem;
            font-weight: 700;
            color: #00ff41 !important;
        }

        .nav-logo span { color: #ffffff !important; }

        .nav-links {
            display: flex;
            gap: 1.5rem;
            font-size: 0.85rem;
            letter-spacing: 1px;
            text-transform: uppercase;
            flex-wrap: wrap;
        }

        .nav-links a {
            color: #888 !important;
            text-decoration: none !important;
        }

        .nav-links a:hover {
            color: #00ff41 !important;
        }

        .nav-badge {
            background: #00ff41;
            color: #000 !important;
            padding: 0.4rem 1rem;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 700;
        }

        .hero-tag {
            display: inline-block;
            border: 1px solid #00ff41;
            color: #00ff41 !important;
            padding: 0.3rem 1rem;
            border-radius: 4px;
            font-size: 0.75rem;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 1rem;
        }

        .hero-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 4rem;
            font-weight: 800;
            line-height: 1.05;
            color: #ffffff !important;
            margin-bottom: 1rem;
            letter-spacing: -2px;
        }

        .hero-title .accent {
            color: #00ff41 !important;
        }

        .hero-desc {
            font-size: 1.05rem;
            color: #777 !important;
            max-width: 650px;
            line-height: 1.7;
            margin-bottom: 1.5rem;
        }

        .status-blocked {
            background: linear-gradient(90deg, rgba(255,40,40,0.15), transparent);
            border-left: 3px solid #ff2828;
            border-radius: 0 8px 8px 0;
            padding: 1rem 1.5rem;
            color: #ff6b6b !important;
            font-weight: 600;
            margin: 1rem 0;
        }

        .status-passed {
            background: linear-gradient(90deg, rgba(0,255,65,0.12), transparent);
            border-left: 3px solid #00ff41;
            border-radius: 0 8px 8px 0;
            padding: 1rem 1.5rem;
            color: #00ff41 !important;
            font-weight: 600;
            margin: 1rem 0;
        }

        .grade-wrapper, .metric-card, .vuln-card, .remediation-card, .chart-card {
            background: #050f05;
            border: 1px solid #0d2b0d;
            border-radius: 12px;
        }

        .grade-wrapper {
            padding: 2rem;
            text-align: center;
        }

        .grade-letter {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 5.5rem;
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

        .metric-card {
            padding: 1.5rem;
            text-align: center;
        }

        .metric-number {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 2.4rem;
            font-weight: 700;
            margin-top: 0.3rem;
        }

        .metric-label {
            font-size: 0.75rem;
            color: #555 !important;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .section-tag {
            font-size: 0.7rem;
            color: #00ff41 !important;
            text-transform: uppercase;
            letter-spacing: 3px;
            margin-bottom: 0.4rem;
        }

        .section-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 2rem;
            font-weight: 700;
            color: #ffffff !important;
            margin-bottom: 1rem;
        }

        .vuln-card {
            padding: 1.5rem;
            margin-bottom: 1rem;
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
            font-size: 0.8rem;
            color: #555 !important;
        }

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
        .badge-low { background: rgba(0,255,65,0.10); color: #00ff41 !important; border: 1px solid rgba(0,255,65,0.2); }

        .ai-feedback-box {
            background: #030a03;
            border: 1px solid #0d2b0d;
            border-radius: 8px;
            padding: 1rem;
            font-size: 0.9rem;
            color: #aaa !important;
            line-height: 1.7;
            min-height: 160px;
        }

        .build-table-wrapper {
            background: #050f05;
            border: 1px solid #0d2b0d;
            border-radius: 12px;
            overflow: hidden;
        }

        .build-table-header, .build-table-row {
            display: grid;
            grid-template-columns: 120px 1fr 80px 100px 80px;
            gap: 1rem;
            padding: 0.9rem 1.2rem;
            align-items: center;
        }

        .build-table-header {
            border-bottom: 1px solid #0d2b0d;
        }

        .build-table-header span {
            font-size: 0.68rem;
            color: #444 !important;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }

        .build-table-row {
            border-bottom: 1px solid #0a1a0a;
        }

        .build-table-row:last-child {
            border-bottom: none;
        }

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

        .badge-pass { background: rgba(0,255,65,0.12); color: #00ff41 !important; border: 1px solid rgba(0,255,65,0.2); }
        .badge-fail { background: rgba(255,40,40,0.15); color: #ff4444 !important; border: 1px solid rgba(255,40,40,0.3); }

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

        .login-brand-wrap {
            text-align: center;
            margin-top: 1rem;
            margin-bottom: 2rem;
        }

        .login-brand-icon {
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }

        .login-brand-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 3rem;
            font-weight: 700;
            color: #00ff41 !important;
            margin-bottom: 0.4rem;
        }

        .login-brand-subtitle {
            color: #666 !important;
            font-size: 1rem;
        }

        .login-card {
            background: #050f05;
            border: 1px solid #0d2b0d;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 0 30px rgba(0,255,65,0.06);
        }

        .login-heading {
            text-align: center;
            font-size: 1.3rem;
            font-weight: 600;
            color: #fff !important;
            margin-bottom: 1rem;
        }

        @media (max-width: 768px) {
            .hero-title { font-size: 2.4rem !important; }
            .build-table-header, .build-table-row {
                grid-template-columns: 90px 1fr 60px 80px;
            }
            .build-table-header span:last-child,
            .build-table-row div:last-child {
                display: none;
            }
            .block-container {
                padding: 1rem !important;
            }
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


# =========================
# LOGIN PAGE
# =========================
def show_login_page():
    apply_theme()

    st.markdown("""
    <div class="login-brand-wrap">
        <div class="login-brand-icon">🛡️</div>
        <div class="login-brand-title">VexilGuard</div>
        <div class="login-brand-subtitle">Security Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([1.2, 1, 1.2])

    with center:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="login-heading">Login</div>', unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        role = st.selectbox("Role", ["developer", "security_team", "admin"])

        if st.button("Login", width="stretch"):
            if username and password:
                st.session_state.authenticated = True
                st.session_state.user_role = role
                st.rerun()
            else:
                st.error("Please enter username and password")

        st.markdown("</div>", unsafe_allow_html=True)


# =========================
# CHARTS
# =========================
def create_severity_chart(issues):
    dist = get_severity_distribution(issues)

    df = pd.DataFrame({
        "Severity": list(dist.keys()),
        "Count": list(dist.values())
    })

    fig = px.pie(
        df,
        values="Count",
        names="Severity",
        color="Severity",
        color_discrete_map={
            "HIGH": "#ff4444",
            "MEDIUM": "#ffa500",
            "LOW": "#00ff41"
        },
        title="Severity Distribution"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e0e0e0"),
        margin=dict(l=10, r=10, t=50, b=10)
    )

    return fig


def create_issue_type_chart(issues):
    issue_types = get_issue_types(issues)
    if not issue_types:
        return None

    df = pd.DataFrame({
        "Issue": list(issue_types.keys()),
        "Count": list(issue_types.values())
    }).sort_values("Count", ascending=False)

    fig = px.bar(
        df,
        x="Issue",
        y="Count",
        color="Count",
        color_continuous_scale=["#00ff41", "#ffa500", "#ff4444"],
        title="Issue Types"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e0e0e0"),
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis_title=None
    )

    return fig


# =========================
# MAIN APP
# =========================
def main():
    init_session_state()

    if not st.session_state.authenticated:
        show_login_page()
        return

    apply_theme()

    report_path = "reports/ai_report.json"
    issues = load_report(report_path)

    if not issues:
        issues = st.session_state.demo_issues

    with st.sidebar:
        st.markdown("""
        <div style="padding:1rem 0;">
            <div style="font-family:Space Grotesk; font-size:1.3rem; font-weight:700; color:#00ff41;">🛡️ VexilGuard</div>
            <div style="font-size:0.75rem; color:#555; letter-spacing:2px; text-transform:uppercase;">Security Intelligence</div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        st.markdown(
            '<div style="font-size:0.7rem; color:#00ff41; text-transform:uppercase; letter-spacing:2px; margin-bottom:1rem;">📊 Scan Metadata</div>',
            unsafe_allow_html=True
        )

        metadata = {
            "🕐 Scan Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "🔧 SAST Engine": "Bandit v1.8",
            "🔐 Secret Scanner": "Gitleaks",
            "🤖 AI Engine": "Groq LLaMA 3.3",
            "📁 Target": "src/",
            "🌿 Branch": "main",
            "⚙️ Trigger": "git push",
            "👤 Role": st.session_state.user_role
        }

        for key, val in metadata.items():
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px solid #0d2b0d;">
                <span style="color:#555; font-size:0.8rem;">{key}</span>
                <span style="color:#ccc; font-size:0.8rem; font-family:monospace;">{val}</span>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        st.markdown(
            '<div style="font-size:0.7rem; color:#00ff41; text-transform:uppercase; letter-spacing:2px; margin-bottom:1rem;">💾 Export Reports</div>',
            unsafe_allow_html=True
        )

        csv_data = export_to_csv(issues)
        json_data = export_to_json(issues)

        if csv_data:
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name="security_report.csv",
                mime="text/csv",
                width="stretch"
            )

        if json_data:
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name="security_report.json",
                mime="application/json",
                width="stretch"
            )

        st.divider()

        st.markdown(
            '<div style="font-size:0.7rem; color:#00ff41; text-transform:uppercase; letter-spacing:2px; margin-bottom:1rem;">⚙️ Pipeline Stack</div>',
            unsafe_allow_html=True
        )

        for tool in ["GitHub Actions", "Bandit SAST", "Gitleaks", "Groq AI", "Streamlit"]:
            st.markdown(
                f'<div style="padding:0.4rem 0; font-size:0.85rem; color:#888;"><span style="color:#00ff41; margin-right:0.5rem;">▸</span>{tool}</div>',
                unsafe_allow_html=True
            )

        st.divider()

        if st.button("Logout", width="stretch"):
            st.session_state.authenticated = False
            st.rerun()

        st.markdown(
            '<div style="font-size:0.75rem; color:#333; text-align:center; margin-top:1rem;">VexilGuard v2.1.0<br>Built by Jesinda Rachel</div>',
            unsafe_allow_html=True
        )

    st.markdown("""
    <div class="navbar">
        <div class="nav-logo">Vexil<span>Guard</span></div>
        <div class="nav-links">
            <a href="#dashboard">Dashboard</a>
            <a href="#history">History</a>
            <a href="#reports">Reports</a>
            <a href="#remediation">Remediation</a>
            <a href="#analytics">Analytics</a>
        </div>
        <div class="nav-badge">LIVE SCAN</div>
    </div>
    <div id="dashboard"></div>
    """, unsafe_allow_html=True)

    if not issues:
        st.markdown(
            '<div class="status-blocked">⚠️ No security report found. Push code to trigger the pipeline, or load demo data below.</div>',
            unsafe_allow_html=True
        )

        if st.button("Load Demo Data"):
            st.session_state.demo_issues = [
                {
                    "issue": "Hardcoded API Key",
                    "severity": "HIGH",
                    "file": "src/config.py",
                    "line": 15,
                    "code": 'API_KEY = "sk-test-123"',
                    "ai_feedback": "Move this secret into an environment variable and load it with os.environ.get()."
                },
                {
                    "issue": "SQL Injection",
                    "severity": "HIGH",
                    "file": "src/db.py",
                    "line": 42,
                    "code": 'cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")',
                    "ai_feedback": "Use parameterized queries instead of string interpolation."
                },
                {
                    "issue": "Weak Hashing Algorithm",
                    "severity": "MEDIUM",
                    "file": "src/auth.py",
                    "line": 28,
                    "code": 'hashed = hashlib.md5(password.encode()).hexdigest()',
                    "ai_feedback": "Replace MD5 with bcrypt or another password-safe algorithm."
                },
                {
                    "issue": "Open Redirect",
                    "severity": "LOW",
                    "file": "src/views.py",
                    "line": 77,
                    "code": 'return redirect(next_url)',
                    "ai_feedback": "Validate redirect destinations against an allowlist."
                }
            ]
            st.rerun()
        return

    metrics = calculate_metrics(issues)

    col_hero, col_grade = st.columns([2, 1])

    with col_hero:
        st.markdown('<div class="hero-tag">AI-Powered Security Scanner</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-title">Shift Security<br><span class="accent">Left.</span></div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="hero-desc">VexilGuard scans every code push for vulnerabilities, secrets, and security misconfigurations, then guides developers with AI-powered remediation tips.</div>',
            unsafe_allow_html=True
        )

        if metrics["high"] > 0:
            st.markdown(
                f'<div class="status-blocked">🚫 PIPELINE BLOCKED — {metrics["high"]} critical issue(s) found. Fix these issues before merge.</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="status-passed">✅ PIPELINE PASSED — No critical issues found. Safe to proceed.</div>',
                unsafe_allow_html=True
            )

    with col_grade:
        if metrics["high"] == 0 and metrics["medium"] == 0:
            grade, score, color, label = "A", 100, "#00ff41", "Excellent"
        elif metrics["high"] == 0 and metrics["medium"] <= 2:
            grade, score, color, label = "B", 75, "#7fff00", "Good"
        elif metrics["high"] <= 1:
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

    c1, c2, c3, c4 = st.columns(4)
    metric_data = [
        ("Total Issues", metrics["total"], "#00ff41"),
        ("Critical", metrics["high"], "#ff4444"),
        ("Medium", metrics["medium"], "#ffa500"),
        ("Low", metrics["low"], "#00ff41"),
    ]

    for col, (label, value, color) in zip([c1, c2, c3, c4], metric_data):
        with col:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-number" style="color:{color}">{value}</div></div>',
                unsafe_allow_html=True
            )

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown('<div id="analytics"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">// analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Security Analytics</div>', unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.plotly_chart(create_severity_chart(issues), width="stretch")

    with chart_col2:
        issue_chart = create_issue_type_chart(issues)
        if issue_chart is not None:
            st.plotly_chart(issue_chart, width="stretch")

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown('<div id="history"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">// build history</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Pipeline Run Log</div>', unsafe_allow_html=True)

    build_history = [
        {"commit": "ec817e7", "message": "fix: switch to Groq API for AI analysis", "status": "BLOCKED", "issues": 3, "time": "2h ago"},
        {"commit": "697b643", "message": "feat: add AI mentor to pipeline", "status": "BLOCKED", "issues": 3, "time": "3h ago"},
        {"commit": "306ae31", "message": "fix: ensure reports directory exists", "status": "PASSED", "issues": 0, "time": "4h ago"},
        {"commit": "0b53383", "message": "fix: upgrade artifact action to v4", "status": "PASSED", "issues": 0, "time": "5h ago"},
        {"commit": "8781da1", "message": "feat: initial pipeline setup", "status": "BLOCKED", "issues": 1, "time": "6h ago"},
    ]

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

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown('<div id="reports"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">// vulnerability analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">AI Fix Recommendations</div>', unsafe_allow_html=True)

    for issue in issues:
        severity = issue.get("severity", "LOW")

        if severity == "HIGH":
            icon, badge_class, card_class = "🔴", "badge-high", "vuln-card-high"
        elif severity == "MEDIUM":
            icon, badge_class, card_class = "🟡", "badge-medium", "vuln-card-medium"
        else:
            icon, badge_class, card_class = "🟢", "badge-low", "vuln-card-low"

        st.markdown(f"""
        <div class="vuln-card {card_class}">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:1rem; flex-wrap:wrap;">
                <div>
                    <div class="vuln-card-title">{icon} {issue.get("issue")}</div>
                    <div class="vuln-card-meta">📁 {issue.get("file")} · Line {issue.get("line")}</div>
                </div>
                <span class="badge {badge_class}">{severity}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        code_col, feedback_col = st.columns(2)

        with code_col:
            st.markdown("#### Vulnerable Code")
            st.code(issue.get("code", ""), language="python")

        with feedback_col:
            st.markdown("#### AI Mentor Feedback")
            st.markdown(
                f'<div class="ai-feedback-box">{issue.get("ai_feedback", "No feedback available.")}</div>',
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div id="remediation"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">// remediation</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Remediation Checklist</div>', unsafe_allow_html=True)

    steps = [
        "Read and understand each vulnerability description",
        "Open the affected file in your editor",
        "Apply the AI-recommended fix",
        "Run Bandit locally: bandit -r src/",
        "Commit the fix with a clear message",
        "Push to GitHub and verify the pipeline"
    ]

    st.markdown("""
    <div class="remediation-card" style="padding:1.5rem; margin-bottom:1rem;">
        <div style="font-family:'Space Grotesk', sans-serif; font-size:1rem; font-weight:600; color:#fff;">🛠️ Your Fix Checklist</div>
        <div style="font-size:0.85rem; color:#555; margin-top:0.4rem;">Track your remediation progress below.</div>
    </div>
    """, unsafe_allow_html=True)

    completed = 0
    for step in steps:
        key = f"step_{step}"
        checked = st.checkbox(step, key=key)
        if checked:
            completed += 1

    progress = completed / len(steps)
    st.progress(progress)

    if completed == len(steps):
        st.markdown(
            '<div class="status-passed">🎉 All remediation steps completed. Push your branch and re-run the scan.</div>',
            unsafe_allow_html=True
        )
    elif completed > 0:
        st.markdown(
            f'<div style="font-size:0.85rem; color:#666; margin-top:0.5rem;">⏳ {completed}/{len(steps)} steps completed.</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div style="font-size:0.85rem; color:#666; margin-top:0.5rem;">Start checking off steps as you fix the issues.</div>',
            unsafe_allow_html=True
        )

    st.markdown("""
    <div class="footer">
        <div class="footer-logo">🛡️ VexilGuard</div>
        <div>GitHub Actions · Bandit · Gitleaks · Groq AI · Streamlit</div>
        <div>v2.1.0 · Built by Jesinda Rachel</div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()