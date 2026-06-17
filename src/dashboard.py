import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path
import base64
from io import BytesIO

# =====================
# ENHANCEMENT 1: PERFORMANCE & ARCHITECTURE
# =====================

# Cache heavy computations
@st.cache_data(ttl=300)
def load_report(report_path):
    """Load and parse security report with caching"""
    if not os.path.exists(report_path):
        return None
    with open(report_path, "r") as f:
        return json.load(f)

@st.cache_data(ttl=600)
def calculate_metrics(issues):
    """Calculate all metrics efficiently"""
    if not issues:
        return {"total": 0, "high": 0, "medium": 0, "low": 0}
    return {
        "total": len(issues),
        "high": len([i for i in issues if i.get("severity") == "HIGH"]),
        "medium": len([i for i in issues if i.get("severity") == "MEDIUM"]),
        "low": len([i for i in issues if i.get("severity") == "LOW"])
    }

@st.cache_data(ttl=600)
def get_severity_distribution(issues):
    """Get severity distribution for charts"""
    if not issues:
        return []
    dist = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for issue in issues:
        severity = issue.get("severity", "UNKNOWN")
        if severity in dist:
            dist[severity] += 1
    return dist

@st.cache_data(ttl=600)
def get_issue_types(issues):
    """Get issue types distribution"""
    if not issues:
        return []
    types = {}
    for issue in issues:
        issue_type = issue.get("issue", "Unknown")
        types[issue_type] = types.get(issue_type, 0) + 1
    return types

# Session state management
def init_session_state():
    """Initialize session state with defaults"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_role" not in st.session_state:
        st.session_state.user_role = "developer"
    if "completed_steps" not in st.session_state:
        st.session_state.completed_steps = set()
    if "scan_history" not in st.session_state:
        st.session_state.scan_history = []

# =====================
# ENHANCEMENT 2: AUTHENTICATION & SECURITY
# =====================

def show_login_page():
    """Simple login page (replace with proper auth in production)"""
    st.set_page_config(page_title="VexilGuard - Login", layout="centered")
    
    st.markdown("""
    <style>
        body {
            background-color: #030a03 !important;
            color: #e0e0e0 !important;
        }
        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .login-card {
            background: #050f05;
            border: 1px solid #0d2b0d;
            border-radius: 16px;
            padding: 3rem;
            width: 400px;
            text-align: center;
        }
        .login-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 2.5rem;
            color: #00ff41;
            margin-bottom: 1rem;
        }
        .login-input {
            width: 100%;
            padding: 0.8rem;
            margin: 0.5rem 0;
            background: #030a03;
            border: 1px solid #0d2b0d;
            border-radius: 8px;
            color: #e0e0e0;
        }
        .login-btn {
            width: 100%;
            padding: 1rem;
            margin: 1rem 0;
            background: #00ff41;
            color: #000;
            border: none;
            border-radius: 8px;
            font-weight: 700;
            cursor: pointer;
        }
    </style>
    <div class="login-container">
        <div class="login-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🛡️</div>
            <div class="login-title">VexilGuard</div>
            <div style="color: #666; margin-bottom: 2rem;">Security Intelligence Platform</div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.title("🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["developer", "security_team", "admin"])
        
        if st.button("Login", type="primary"):
            # Replace with proper authentication
            if username and password:
                st.session_state.authenticated = True
                st.session_state.user_role = role
                st.rerun()
            else:
                st.error("Please enter username and password")

# =====================
# ENHANCEMENT 3: ADVANCED VISUALIZATIONS
# =====================

def create_severity_pie_chart(issues):
    """Create interactive pie chart for severity distribution"""
    dist = get_severity_distribution(issues)
    
    fig = px.pie(
        values=list(dist.values()),
        names=list(dist.keys()),
        colors=["#ff4444", "#ffa500", "#00ff41"],
        title="Severity Distribution",
        hover_name="Severity",
        textinfo="label+percent+value"
    )
    fig.update_layout(
        background="transparent",
        paper_bgcolor="transparent",
        plot_bgcolor="transparent",
        font={"color": "#e0e0e0"},
        margin=dict(l=0, r=0, t=40, b=0)
    )
    return fig

def create_issue_types_bar_chart(issues):
    """Create bar chart for issue types"""
    types = get_issue_types(issues)
    if not types:
        return None
    
    df = pd.DataFrame({
        "Issue Type": list(types.keys()),
        "Count": list(types.values())
    })
    df = df.sort_values("Count", ascending=False)
    
    fig = px.bar(
        df,
        x="Issue Type",
        y="Count",
        color="Count",
        colors=["#00ff41"],
        title="Issue Types Distribution",
        hover_data={"Issue Type": True, "Count": True}
    )
    fig.update_layout(
        background="transparent",
        paper_bgcolor="transparent",
        plot_bgcolor="transparent",
        font={"color": "#e0e0e0"},
        xaxis_title="Issue Type",
        yaxis_title="Count"
    )
    return fig

def create_security_trend_chart(build_history):
    """Create trend chart for security score over time"""
    if not build_history:
        return None
    
    df = pd.DataFrame(build_history)
    df["issues"] = df["issues"].astype(int)
    df["score"] = 100 - (df["issues"] * 20)
    df["score"] = df["score"].clip(lower=0)
    
    fig = px.line(
        df,
        x="time",
        y="score",
        markers=True,
        color="score",
        colors=["#00ff41"],
        title="Security Score Trend",
        hover_name="Commit"
    )
    fig.update_layout(
        background="transparent",
        paper_bgcolor="transparent",
        plot_bgcolor="transparent",
        font={"color": "#e0e0e0"},
        xaxis_title="Time",
        yaxis_title="Security Score"
    )
    return fig

# =====================
# ENHANCEMENT 4: USER EXPERIENCE IMPROVEMENTS
# =====================

def show_custom_theme():
    """Enhanced dark theme with more features"""
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

        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0d2b0d;
        }
        ::-webkit-scrollbar-thumb {
            background: #00ff41;
            border-radius: 4px;
        }

        /* Enhanced buttons */
        .stButton>button {
            background: #00ff41 !important;
            color: #000 !important;
            border: 1px solid #00ff41 !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.3s !important;
        }
        .stButton>button:hover {
            box-shadow: 0 0 20px #00ff4140 !important;
            transform: translateY(-2px) !important;
        }

        /* Enhanced cards */
        .card {
            background: #050f05;
            border: 1px solid #0d2b0d;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            transition: all 0.3s;
        }
        .card:hover {
            border-color: #00ff41;
            box-shadow: 0 0 30px #00ff4110;
        }

        /* Progress bar enhanced */
        .stProgress > div > div {
            background: #00ff41 !important;
            box-shadow: 0 0 10px #00ff4180;
        }

        /* Code blocks enhanced */
        code, .stCode {
            background: #050f05 !important;
            color: #00ff41 !important;
            border: 1px solid #0d2b0d !important;
            border-radius: 8px !important;
        }

        /* Nav */
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
            color: #00ff41 !important;
        }

        .nav-links {
            display: flex;
            gap: 2rem;
            font-size: 0.85rem;
            text-transform: uppercase;
        }

        .nav-links a {
            color: #888 !important;
            text-decoration: none;
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
        }

        /* Hero */
        .hero-tag {
            display: inline-block;
            border: 1px solid #00ff41;
            color: #00ff41 !important;
            padding: 0.3rem 1rem;
            border-radius: 4px;
            font-size: 0.75rem;
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

        /* Status */
        .status-blocked {
            background: linear-gradient(90deg, rgba(255,40,40,0.15), transparent);
            border-left: 3px solid #ff2828;
            border-radius: 0 8px 8px 0;
            padding: 1rem 1.5rem;
            color: #ff6b6b !important;
            font-weight: 600;
            margin: 1.5rem 0;
        }

        .status-passed {
            background: linear-gradient(90deg, rgba(0,255,65,0.1), transparent);
            border-left: 3px solid #00ff41;
            border-radius: 0 8px 8px 0;
            padding: 1rem 1.5rem;
            color: #00ff41 !important;
            font-weight: 600;
            margin: 1.5rem 0;
        }

        /* Grade card */
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
            text-transform: uppercase;
            margin-top: 0.5rem;
        }

        /* Metric cards */
        .metric-card {
            background: #050f05;
            border: 1px solid #0d2b0d;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
        }

        .metric-number {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 2.8rem;
            font-weight: 700;
            margin: 0.3rem 0;
        }

        .metric-label {
            font-size: 0.75rem;
            color: #555 !important;
            text-transform: uppercase;
        }

        /* Section titles */
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
        }

        /* Vulnerability cards */
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

        .ai-feedback-box {
            background: #030a03;
            border: 1px solid #0d2b0d;
            border-radius: 8px;
            padding: 1rem;
            font-size: 0.88rem;
            color: #aaa !important;
            line-height: 1.7;
        }

        /* Badges */
        .badge {
            display: inline-block;
            padding: 0.25rem 0.7rem;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
        }

        .badge-high { background: rgba(255,40,40,0.15); color: #ff4444 !important; }
        .badge-medium { background: rgba(255,165,0,0.15); color: #ffa500 !important; }
        .badge-low { background: rgba(0,255,65,0.1); color: #00ff41 !important; }
        .badge-pass { background: rgba(0,255,65,0.1); color: #00ff41 !important; }
        .badge-fail { background: rgba(255,40,40,0.15); color: #ff4444 !important; }

        /* Footer */
        .footer {
            margin-top: 4rem;
            padding: 2rem 0;
            border-top: 1px solid #0d2b0d;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: #333 !important;
            font-size: 0.8rem;
        }

        .footer-logo {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1rem;
            font-weight: 700;
            color: #00ff41 !important;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .hero-title { font-size: 2.5rem !important; }
            .navbar { flex-direction: column; text-align: center; }
            .nav-links { gap: 1rem; }
            .grade-letter { font-size: 4rem !important; }
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# =====================
# ENHANCEMENT 5: DATA EXPORT (PDF, CSV)
# =====================

def export_to_csv(issues):
    """Export issues to CSV"""
    if not issues:
        return None
    
    df = pd.DataFrame(issues)
    csv = df.to_csv(index=False)
    return csv

def export_to_json(issues, filename="security_report.json"):
    """Export issues to JSON"""
    if not issues:
        return None
    
    json_str = json.dumps(issues, indent=2)
    return json_str

# =====================
# MAIN APPLICATION
# =====================

def main():
    """Main application"""
    init_session_state()
    
    # Check authentication
    if not st.session_state.authenticated:
        show_login_page()
        return
    
    # Setup page config
    st.set_page_config(
        page_title="VexilGuard",
        page_icon="🛡️",
        layout="wide"
    )
    
    # Apply theme
    show_custom_theme()
    
    # =====================
    # SIDEBAR WITH METADATA
    # =====================
    with st.sidebar:
        st.markdown("""
        <div style="padding:1rem 0; background:#030a03;">
            <div style="font-family:Space Grotesk; font-size:1.3rem; font-weight:700; color:#00ff41; margin-bottom:0.3rem;">🛡️ VexilGuard</div>
            <div style="font-size:0.75rem; color:#555; letter-spacing:2px; text-transform:uppercase;">Security Intelligence</div>
            <div style="font-size:0.7rem; color:#00ff41; margin-top:0.5rem;">Role: {role}</div>
        </div>
        """.format(role=st.session_state.user_role), unsafe_allow_html=True)
        
        st.divider()
        
        # Metadata section
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
        
        # Export section
        st.markdown('<div style="font-size:0.7rem; color:#00ff41; text-transform:uppercase; letter-spacing:2px; margin-bottom:1rem;">💾 Export Reports</div>', unsafe_allow_html=True)
        
        report_path = "reports/ai_report.json"
        issues = load_report(report_path)
        
        if issues:
            csv_data = export_to_csv(issues)
            json_data = export_to_json(issues)
            
            if csv_data:
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name="security_report.csv",
                    mime="text/csv",
                    style="width:100%"
                )
            
            if json_data:
                st.download_button(
                    label="📥 Download JSON",
                    data=json_data,
                    file_name="security_report.json",
                    mime="application/json",
                    style="width:100%"
                )
        
        st.divider()
        
        # Pipeline stack
        st.markdown('<div style="font-size:0.7rem; color:#00ff41; text-transform:uppercase; letter-spacing:2px; margin-bottom:1rem;">⚙️ Pipeline Stack</div>', unsafe_allow_html=True)
        
        for tool in ["GitHub Actions", "Bandit SAST", "Gitleaks", "Groq AI", "Streamlit"]:
            st.markdown(f'<div style="padding:0.4rem 0; font-size:0.85rem; color:#888;"><span style="color:#00ff41; margin-right:0.5rem;">▸</span>{tool}</div>', unsafe_allow_html=True)
        
        st.divider()
        st.markdown('<div style="font-size:0.75rem; color:#333; text-align:center;">VexilGuard v2.0.0<br>Built by Jesinda Rachel<br>🔐 {role} Mode</div>'.format(role=st.session_state.user_role), unsafe_allow_html=True)
    
    # =====================
    # NAVBAR
    # =====================
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
        <a href="/"><div class="nav-badge">⟳ LIVE SCAN</div></a>
    </div>
    <div id="dashboard"></div>
    """, unsafe_allow_html=True)
    
    # =====================
    # LOAD REPORT
    # =====================
    report_path = "reports/ai_report.json"
    issues = load_report(report_path)
    
    if not issues:
        st.markdown('<div class="status-blocked">⚠️ No security report found. Push code to trigger the pipeline!</div>', unsafe_allow_html=True)
        
        # Show demo data for testing
        with st.expander("📦 Load Demo Data"):
            st.info("No report found? Use demo data to test the dashboard")
            if st.button("Load Demo Security Report"):
                demo_issues = [
                    {
                        "issue": "Hardcoded API Key",
                        "severity": "HIGH",
                        "file": "src/config.py",
                        "line": 15,
                        "code": "API_KEY = \"sk-1234567890abcdef\"",
                        "ai_feedback": "Replace hardcoded API key with environment variable. Use: API_KEY = os.environ.get('API_KEY')"
                    },
                    {
                        "issue": "SQL Injection Vulnerability",
                        "severity": "HIGH",
                        "file": "src/database.py",
                        "line": 42,
                        "code": "cursor.execute(f\"SELECT * FROM users WHERE id = {user_id}\")",
                        "ai_feedback": "Use parameterized queries: cursor.execute(\"SELECT * FROM users WHERE id = ?\", (user_id,))"
                    },
                    {
                        "issue": "Weak Password Hashing",
                        "severity": "MEDIUM",
                        "file": "src/auth.py",
                        "line": 28,
                        "code": "password_hash = hashlib.md5(password.encode())",
                        "ai_feedback": "Use bcrypt or hashlib.sha256 with salting: from bcrypt import generate_password_hash"
                    },
                    {
                        "issue": "Unvalidated Redirect",
                        "severity": "LOW",
                        "file": "src/views.py",
                        "line": 67,
                        "code": "return redirect(user_input)",
                        "ai_feedback": "Validate redirect URL against whitelist: if user_input in ALLOWED_REDIRECTS: return redirect(user_input)"
                    }
                ]
                st.session_state.demo_issues = demo_issues
                st.rerun()
        
        issues = st.session_state.get("demo_issues", [])
    
    metrics = calculate_metrics(issues)
    
    # =====================
    # HERO SECTION
    # =====================
    col_hero, col_grade = st.columns([2, 1])
    
    with col_hero:
        st.markdown('<div class="hero-tag">🛡️ AI-Powered Security Scanner</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-title">Shift Security<br><span class="accent">Left.</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-desc">VexilGuard automatically scans every code push for vulnerabilities, secrets, and security misconfigurations — then teaches your team exactly how to fix them using AI.</div>', unsafe_allow_html=True)
        
        if metrics["high"] > 0:
            st.markdown(f'<div class="status-blocked">🚫 PIPELINE BLOCKED — {metrics["high"]} critical issue(s) found. You\'re close — just fix these and you\'re good to go!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-passed">✅ PIPELINE PASSED — Excellent work! Your code is clean and safe to merge.</div>', unsafe_allow_html=True)
    
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
    
    # =====================
    # METRICS CARDS
    # =====================
    col1, col2, col3, col4 = st.columns(4)
    metrics_data = [
        ("Total Issues", metrics["total"], "#00ff41"),
        ("🔴 Critical", metrics["high"], "#ff4444"),
        ("🟡 Medium", metrics["medium"], "#ffa500"),
        ("🟢 Low", metrics["low"], "#00ff41")
    ]
    
    for col, (label, value, color) in zip([col1, col2, col3, col4], metrics_data):
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-number" style="color:{color}">{value}</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # =====================
    # ENHANCEMENT 6: ADVANCED VISUALIZATIONS SECTION
    # =====================
    st.markdown('<div id="analytics"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">// analytics & insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Security Analytics Dashboard</div>', unsafe_allow_html=True)
    
    if issues:
        # Create charts
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown('<div style="font-size:0.9rem; color:#555; margin-bottom:1rem;">📊 Severity Breakdown</div>', unsafe_allow_html=True)
            fig_pie = create_severity_pie_chart(issues)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col_chart2:
            st.markdown('<div style="font-size:0.9rem; color:#555; margin-bottom:1rem;">📈 Issue Types</div>', unsafe_allow_html=True)
            fig_bar = create_issue_types_bar_chart(issues)
            if fig_bar:
                st.plotly_chart(fig_bar, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Risk heatmap
        st.markdown('<div style="font-size:0.9rem; color:#555; margin-bottom:1rem;">🔥 Risk Distribution by File</div>', unsafe_allow_html=True)
        
        # Create file risk data
        file_risks = {}
        for issue in issues:
            file = issue.get("file", "Unknown")
            severity = issue.get("severity", "UNKNOWN")
            risk_score = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}.get(severity, 0)
            file_risks[file] = file_risks.get(file, 0) + risk_score
        
        if file_risks:
            df_files = pd.DataFrame({
                "File": list(file_risks.keys()),
                "Risk Score": list(file_risks.values())
            })
            df_files = df_files.sort_values("Risk Score", ascending=False)
            
            fig_heatmap = px.bar(
                df_files,
                x="File",
                y="Risk Score",
                color="Risk Score",
                colors=["#00ff41", "#ffa500", "#ff4444"],
                title="Risk Score by File",
                hover_data={"File": True, "Risk Score": True}
            )
            fig_heatmap.update_layout(
                background="transparent",
                paper_bgcolor="transparent",
                plot_bgcolor="transparent",
                font={"color": "#e0e0e0"},
                xaxis_title="File",
                yaxis_title="Risk Score"
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # =====================
    # BUILD HISTORY
    # =====================
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
    
    # =====================
    # VULNERABILITY CARDS
    # =====================
    st.markdown('<div id="reports"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">// vulnerability analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">AI Fix Recommendations</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.9rem; color:#555; margin-bottom:1.5rem;">Great news — every issue below has a clear fix waiting for you. AI has already done the hard part! 🚀</div>', unsafe_allow_html=True)
    
    if not issues:
        st.info("No vulnerabilities found! Your code is clean. 🎉")
    else:
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
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # =====================
    # REMEDIATION SECTION
    # =====================
    st.markdown('<div id="remediation"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">// developer tools</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Remediation Sandbox</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.9rem; color:#555; margin-bottom:1.5rem;">You\'ve got this! Check off each step as you go — watch that progress bar fill up to 100% 🎯</div>', unsafe_allow_html=True)
    
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
        key = f"step_{step[:30]}"
        if st.checkbox(step, key=key, value=st.session_state.completed_steps.get(key, False)):
            st.session_state.completed_steps[key] = True
            completed += 1
        elif key in st.session_state.completed_steps:
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
    
    # =====================
    # FOOTER
    # =====================
    st.markdown("""
    <div class="footer">
        <div class="footer-logo">🛡️ VexilGuard</div>
        <div style="color:#333;">GitHub Actions · Bandit · Gitleaks · Groq AI · Streamlit</div>
        <div style="color:#333;">v2.0.0 · Built by Jesinda Rachel · 🔐 {role} Mode</div>
    </div>
    """.format(role=st.session_state.user_role), unsafe_allow_html=True)

if __name__ == "__main__":
    main()