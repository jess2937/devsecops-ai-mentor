import streamlit as st
import json
import os

st.set_page_config(
    page_title="DevSecOps AI Mentor",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .main { background-color: #0a0a0f; }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #888;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    .status-blocked {
        background: linear-gradient(135deg, #ff416c, #ff4b2b);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(255, 65, 108, 0.3);
    }
    
    .status-passed {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(56, 239, 125, 0.3);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #2a2a4a;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: transform 0.2s;
    }
    
    .metric-card:hover { transform: translateY(-4px); }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .vuln-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid;
        transition: transform 0.2s;
    }
    
    .vuln-card:hover { transform: translateX(4px); }
    
    .vuln-high { border-color: #ff416c; }
    .vuln-medium { border-color: #f7971e; }
    .vuln-low { border-color: #11998e; }
    
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
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #e0e0e0;
        margin: 2rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .footer {
        text-align: center;
        color: #444;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding: 1rem;
        border-top: 1px solid #1a1a2e;
    }

    .stExpander {
        background: #1a1a2e !important;
        border: 1px solid #2a2a4a !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown('<p class="hero-title">🛡️ DevSecOps AI Mentor</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Automated Security Scanner powered by AI — finds vulnerabilities and teaches you how to fix them</p>', unsafe_allow_html=True)

st.divider()

# Load report
report_path = "reports/ai_report.json"

if not os.path.exists(report_path):
    st.warning("⚠️ No security report found. Push code to trigger the pipeline!")
    st.stop()

with open(report_path, "r") as f:
    issues = json.load(f)

# Metrics
total = len(issues)
high = len([i for i in issues if i.get("severity") == "HIGH"])
medium = len([i for i in issues if i.get("severity") == "MEDIUM"])
low = len([i for i in issues if i.get("severity") == "LOW"])

# Status Banner
if high > 0:
    st.markdown(f'<div class="status-blocked">🚫 PIPELINE BLOCKED — {high} critical issue(s) detected. Review and fix before merging.</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-passed">✅ PIPELINE PASSED — No critical vulnerabilities detected. Safe to merge!</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Metric Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-label">Total Issues</div>
        <div class="metric-number" style="color:#667eea">{total}</div>
    </div>''', unsafe_allow_html=True)

with col2:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-label">🔴 Critical</div>
        <div class="metric-number" style="color:#ff416c">{high}</div>
    </div>''', unsafe_allow_html=True)

with col3:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-label">🟡 Medium</div>
        <div class="metric-number" style="color:#f7971e">{medium}</div>
    </div>''', unsafe_allow_html=True)

with col4:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-label">🟢 Low</div>
        <div class="metric-number" style="color:#11998e">{low}</div>
    </div>''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.divider()

# Vulnerability Details
st.markdown('<div class="section-title">📋 Vulnerability Analysis & AI Fix Recommendations</div>', unsafe_allow_html=True)

for issue in issues:
    severity = issue.get("severity", "UNKNOWN")
    
    if severity == "HIGH":
        icon = "🔴"
        badge_class = "badge-high"
        card_class = "vuln-high"
    elif severity == "MEDIUM":
        icon = "🟡"
        badge_class = "badge-medium"
        card_class = "vuln-medium"
    else:
        icon = "🟢"
        badge_class = "badge-low"
        card_class = "vuln-low"

    with st.expander(f"{icon} {issue.get('issue')} — Line {issue.get('line')}"):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f'<span class="badge {badge_class}">{severity}</span>', unsafe_allow_html=True)
            st.markdown("**📁 File Location**")
            st.code(issue.get("file"), language="text")
            st.markdown("**❌ Vulnerable Code**")
            st.code(issue.get("code"), language="python")
        
        with col2:
            st.markdown("**🤖 AI Security Mentor Says:**")
            st.info(issue.get("ai_feedback", "No feedback available."))

# Footer
st.markdown('<div class="footer">Built with ❤️ using GitHub Actions • Bandit • Gitleaks • Groq AI • Streamlit</div>', unsafe_allow_html=True)