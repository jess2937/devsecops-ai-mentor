import streamlit as st
import time

# 1. Page Configuration & Theme Anchoring
st.set_page_config(
    page_title="Vexil CI | Autonomous DevSecOps Pipeline",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Universal Dark/Green Theme Overrides (Locks layout to Dark Mode globally)
st.markdown("""
    <style>
        /* Force app backgrounds to dark charcoal/slate */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #0b0f19 !important;
            color: #e2e8f0 !important;
        }
        
        /* Force all standard headers and text to bright white/light gray */
        h1, h2, h3, h4, h5, h6, p, span, label {
            color: #f1f5f9 !important;
        }
        
        /* Custom Vexil Green Highlights & Badges */
        .hero-badge {
            background-color: #064e3b;
            color: #34d399;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            border: 1px solid #059669;
            display: inline-block;
            margin-bottom: 1rem;
        }
        
        /* Main Typography and Visual Gradients */
        .hero-title {
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(135deg, #34d399 0%, #ffffff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        
        .hero-subtitle {
            color: #94a3b8;
            font-size: 1.15rem;
            margin-bottom: 2rem;
            font-weight: 400;
            max-width: 800px;
        }

        /* Modernized Metric Layout Cards */
        .metric-card {
            background-color: #111827;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #1f2937;
            text-align: center;
        }
        .metric-value {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 5px;
        }

        /* Expander Box Resets (Keeps them dark even in browser Light Mode) */
        .streamlit-expanderHeader, [data-testid="stExpander"] {
            background-color: #111827 !important;
            border: 1px solid #1f2937 !important;
            color: #f1f5f9 !important;
        }
        
        /* Table Border Formatting */
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border-bottom: 1px solid #1f2937 !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Branded Header Block
st.markdown('<div class="hero-badge">⚡ Continuous Assurance Engine</div>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">Vexil CI</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Great code takes iteration! Let\'s analyze your recent commits and refine your security posture together.</p>', unsafe_allow_html=True)

# 4. Interactive Simulation Component (With Encouraging Mentor Copy)
st.markdown("#### 🚀 Validate Your Recent Changes")
scan_col1, scan_col2 = st.columns([1, 2])

with scan_col1:
    if st.button("⚡ Run Security Validation Scan", use_container_width=True):
        with st.spinner("Vexil Core auditing code assets... You're doing great, just compiling reports..."):
            time.sleep(1.2)
        st.info("💡 Scan Analyzed! We found a few quick learning opportunities below to optimize your security layer.")

with scan_col2:
    st.markdown("<p style='color: #94a3b8; font-size: 0.95rem; margin-top: 6px;'>Pushing updates frequently is an excellent engineering practice. Click above anytime to run an on-demand code health checkup.</p>", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# 5. Core Security Statistics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-card"><div style="color: #94a3b8; font-size: 0.9rem;">Total Reviews</div><div class="metric-value" style="color: #f1f5f9;">3</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card"><div style="color: #f87171; font-size: 0.9rem;">🔴 High Priority</div><div class="metric-value" style="color: #ef4444;">1</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><div style="color: #fbbf24; font-size: 0.9rem;">🟡 Medium Priority</div><div class="metric-value" style="color: #f59e0b;">2</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-card"><div style="color: #34d399; font-size: 0.9rem;">🟢 Low Priority</div><div class="metric-value" style="color: #10b981;">0</div></div>', unsafe_allow_html=True)

st.markdown("<br><hr><br>", unsafe_allow_html=True)

# 6. FIXED FORMAT: Vulnerability Analysis & AI Fix Recommendations
st.markdown("#### 🔍 Structural Vulnerability Analysis")
st.markdown("<p style='color: #94a3b8; margin-top: -10px; font-size: 0.95rem;'>Click into an identified issue to access clear educational code blueprints provided by your AI Mentor.</p>", unsafe_allow_html=True)

with st.expander("🔴 Issue #01: Cryptographic Weakness Detected (app.py — Line 6)", expanded=True):
    st.markdown("<div style='color: #e2e8f0; font-size: 1rem; margin-bottom: 15px;'><strong>Diagnostic Finding:</strong> The application utilizes an outdated MD5 hashing algorithm which is vulnerable to collision attacks.</div>", unsafe_allow_html=True)
    
    # Modern Side-by-Side Presentation Layout
    code_left, code_right = st.columns(2)
    with code_left:
        st.markdown("<p style='color: #f87171; font-weight: 600; font-size: 0.9rem; margin-bottom:2px;'>❌ Current Vulnerable Logic</p>", unsafe_allow_html=True)
        st.code("""def hash_user_data(password):\n    return hashlib.md5(password.encode()).hexdigest()""", language="python")
    
    with code_right:
        st.markdown("<p style='color: #34d399; font-weight: 600; font-size: 0.9rem; margin-bottom:2px;'>🛡️ AI Mentor Recommended Fix</p>", unsafe_allow_html=True)
        st.code("""def hash_user_data(password):\n    return hashlib.sha256(password.encode()).hexdigest()""", language="python")
        
    st.markdown("""
    <div style="background-color: #0b0f19; padding: 16px; border-radius: 8px; border: 1px solid #1f2937; margin-top: 15px;">
        <span style="font-weight: 600; color: #34d399; font-size: 0.95rem;">👩‍🏫 The Security Lesson:</span>
        <p style="font-size: 0.9rem; color: #94a3b8; margin-top: 6px; margin-bottom: 0;">
            Don't worry, matching cryptography requirements can be tricky at first! Modern servers can decode standard MD5 hashes incredibly quickly using lookup charts. Moving up to <strong>SHA-256</strong> is a simple adjustment that instantly makes your system significantly harder for malicious users to breach. You've got this!
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><hr><br>", unsafe_allow_html=True)

# 7. FIXED FORMAT: Remediation Sandbox (Single Unified Checkbox Approval Step)
st.markdown("#### 🛠️ Developer Remediation Sandbox")
st.markdown("<p style='color: #94a3b8; margin-top: -10px; font-size: 0.95rem;'>Review the AI guidance above, implement the fix in your local workspace, and toggle verification once resolved.</p>", unsafe_allow_html=True)

# Single primary checkbox to clear current batch issues instead of repeating checkboxes
sandbox_left, sandbox_right = st.columns([2, 1])

with sandbox_left:
    st.markdown("""
    <div style="background-color: #111827; padding: 15px; border-radius: 8px; border: 1px solid #1f2937;">
        <span style="font-weight: 600; color: #f1f5f9;">Active Action Plan:</span>
        <ul style="color: #94a3b8; margin-top: 8px; padding-left: 20px; font-size: 0.9rem;">
            <li>Upgrade MD5 hashing implementations inside the active auth files to SHA-256 blocks.</li>
            <li>Re-test locally to verify changes align cleanly with existing codebase structures.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Unified resolution target
    resolved = st.checkbox("Mark all current code vulnerability adjustments as resolved")

with sandbox_right:
    if resolved:
        st.balloons()
        st.markdown("""
            <div style="background-color: #064e3b; border-left: 4px solid #10b981; padding: 15px; border-radius: 8px; text-align: center;">
                <div style="font-size: 1.1rem; font-weight: 700; color: #a7f3d0;">✨ Spectacular Job!</div>
                <div style="font-size: 0.85rem; color: #cbd5e1; margin-top: 4px;">All changes are fully verified. Your code updates are perfectly secure and ready to merge!</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background-color: #1f2937; border-left: 4px solid #94a3b8; padding: 15px; border-radius: 8px; text-align: center;">
                <div style="font-size: 0.9rem; font-weight: 600; color: #cbd5e1;">Reviewing Adjustments</div>
                <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">Take your time patching things up! Check the box whenever your revisions are complete.</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br><hr><br>", unsafe_allow_html=True)

# 8. FIXED FORMAT: Cleaned & Relevant Pipeline History Log
st.markdown("#### ⏳ Vexil CI Project Build Log")

history_data = [
    {"Commit": "fix: migrate database encryption to sha256 arrays", "User": "Developer", "Status": "✅ Build Passed", "Issues": "0 Defects"},
    {"Commit": "feat: integrated core credential routing structures", "User": "Developer", "Status": "❌ Build Blocked", "Issues": "1 High, 2 Med"},
    {"Commit": "docs: generated initial system readme documentation", "User": "Developer", "Status": "✅ Build Passed", "Issues": "0 Defects"},
]

table_html = """
<table style="width:100%; color: #cbd5e1; font-size: 0.9rem;">
    <tr style="text-align: left; color: #94a3b8;">
        <th style="padding: 12px;">Commit Integrity Verification Log</th>
        <th style="padding: 12px;">Committed By</th>
        <th style="padding: 12px;">Pipeline Execution Result</th>
        <th style="padding: 12px;">Audit Summary</th>
    </tr>
"""
for log in history_data:
    status_color = "#34d399" if "Passed" in log['Status'] else "#f87171"
    table_html += f"""
    <tr>
        <td style="padding: 14px; font-family: monospace; color: #f1f5f9;">{log['Commit']}</td>
        <td style="padding: 14px;">{log['User']}</td>
        <td style="padding: 14px; font-weight: 600; color: {status_color};">{log['Status']}</td>
        <td style="padding: 14px; color: #94a3b8;">{log['Issues']}</td>
    </tr>
    """
table_html += "</table>"
st.markdown(table_html, unsafe_allow_html=True)