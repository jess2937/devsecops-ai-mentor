import streamlit as st
import json
import os

st.set_page_config(
    page_title="DevSecOps AI Mentor",
    page_icon="🔒",
    layout="wide"
)

# Header
st.title("🔒 DevSecOps AI Security Dashboard")
st.markdown("### Automated Security Scanner + AI Mentor")
st.divider()

# Load report
report_path = "reports/ai_report.json"

if not os.path.exists(report_path):
    st.warning("⚠️ No security report found. Run the pipeline first!")
    st.stop()

with open(report_path, "r") as f:
    issues = json.load(f)

# Summary metrics
total = len(issues)
high = len([i for i in issues if i.get("severity") == "HIGH"])
medium = len([i for i in issues if i.get("severity") == "MEDIUM"])
low = len([i for i in issues if i.get("severity") == "LOW"])

# Status card
if high > 0:
    st.error(f"❌ PIPELINE BLOCKED — {high} HIGH severity issue(s) found!")
else:
    st.success("✅ PIPELINE PASSED — No critical issues found!")

st.divider()

# Metrics row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Issues", total)
col2.metric("🔴 High", high)
col3.metric("🟡 Medium", medium)
col4.metric("🟢 Low", low)

st.divider()

# Vulnerability details
st.subheader("📋 Vulnerability Details & AI Fix Recommendations")

for i, issue in enumerate(issues):
    severity = issue.get("severity", "UNKNOWN")
    
    # Color based on severity
    if severity == "HIGH":
        color = "🔴"
    elif severity == "MEDIUM":
        color = "🟡"
    else:
        color = "🟢"
    
    with st.expander(f"{color} [{severity}] {issue.get('issue')} — Line {issue.get('line')}"):
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📁 File:**")
            st.code(issue.get("file"), language="text")
            
            st.markdown("**❌ Vulnerable Code:**")
            st.code(issue.get("code"), language="python")
        
        with col2:
            st.markdown("**🤖 AI Mentor Feedback:**")
            st.markdown(issue.get("ai_feedback", "No feedback available."))

st.divider()
st.caption("Built with GitHub Actions + Bandit + Gitleaks + Groq AI + Streamlit")