import streamlit as st
import json
import os
import hashlib
import secrets
import time
from datetime import datetime
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="VexilGuard",
    page_icon="🛡️",
    layout="wide"
)

USERS_FILE = "users.json"
REPORT_FILE = "reports/ai_report.json"

# =========================
# SESSION STATE
# =========================
def init_session():
    defaults = {
        "authenticated": False,
        "username": None,
        "name": None,
        "role": None,
        "page": "signin",
        "demo_issues": [],
        "scan_status": None,
        "scan_time": None,
        "completed_steps": {}
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# =========================
# SECURITY HELPERS
# =========================
def ensure_users_file():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump([], f, indent=2)

def load_users():
    ensure_users_file()
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    ).hex()
    return salt, hashed

def verify_password(password, salt, stored_hash):
    _, new_hash = hash_password(password, salt)
    return secrets.compare_digest(new_hash, stored_hash)

def username_exists(username):
    users = load_users()
    return any(u["username"].lower() == username.lower() for u in users)

def create_user(name, username, password, role):
    users = load_users()
    if username_exists(username):
        return False, "Username already exists."

    salt, password_hash = hash_password(password)
    users.append({
        "name": name,
        "username": username,
        "password_salt": salt,
        "password_hash": password_hash,
        "role": role,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_users(users)
    return True, "Account created successfully."

def authenticate_user(username, password):
    users = load_users()
    for user in users:
        if user["username"].lower() == username.lower():
            if verify_password(password, user["password_salt"], user["password_hash"]):
                return True, user
    return False, None

# =========================
# DATA HELPERS
# =========================
@st.cache_data(ttl=300)
def load_report():
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "r") as f:
            return json.load(f)
    return []

@st.cache_data(ttl=300)
def metrics_from_issues(issues):
    total = len(issues)
    high = len([i for i in issues if i.get("severity") == "HIGH"])
    medium = len([i for i in issues if i.get("severity") == "MEDIUM"])
    low = len([i for i in issues if i.get("severity") == "LOW"])
    return total, high, medium, low

def get_demo_issues():
    return [
        {
            "issue": "Hardcoded API Key",
            "severity": "HIGH",
            "file": "src/config.py",
            "line": 15,
            "code": 'API_KEY = "sk-1234567890abcdef"',
            "ai_feedback": "Move the API key into an environment variable and load it securely from os.environ."
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
            "issue": "Weak Hashing",
            "severity": "MEDIUM",
            "file": "src/auth.py",
            "line": 28,
            "code": "password_hash = hashlib.md5(password.encode()).hexdigest()",
            "ai_feedback": "Replace MD5 with a slow password hashing function such as bcrypt, Argon2, or PBKDF2."
        },
        {
            "issue": "Open Redirect",
            "severity": "LOW",
            "file": "src/views.py",
            "line": 67,
            "code": "return redirect(user_input)",
            "ai_feedback": "Validate the redirect target against an allowlist before redirecting."
        }
    ]

def run_live_scan():
    st.session_state.scan_status = "running"
    st.session_state.scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time.sleep(1)
    issues = load_report()
    if not issues:
        issues = get_demo_issues()
        st.session_state.demo_issues = issues
    st.session_state.scan_status = "complete"

def get_active_issues():
    issues = load_report()
    if issues:
        return issues
    if st.session_state.demo_issues:
        return st.session_state.demo_issues
    return get_demo_issues()

# =========================
# THEME
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    html, body, .stApp, [class*="css"] {
        background: #030a03 !important;
        color: #e6e6e6 !important;
        font-family: 'Inter', sans-serif !important;
    }

    .block-container {
        max-width: 1380px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }

    .brand {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        color: #00ff41;
        letter-spacing: -1px;
    }

    .muted {
        color: #8b8b8b;
        font-size: 0.95rem;
    }

    .glass {
        background: #071107;
        border: 1px solid #123312;
        border-radius: 16px;
        padding: 1.2rem;
    }

    .hero {
        background: linear-gradient(135deg, #071107 0%, #041004 100%);
        border: 1px solid #123312;
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 1rem;
    }

    .metric {
        background: #071107;
        border: 1px solid #123312;
        border-radius: 14px;
        padding: 1rem;
        text-align: center;
    }

    .metric-num {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
    }

    .badge {
        display: inline-block;
        padding: 0.25rem 0.7rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 700;
    }

    .high { background: rgba(255,68,68,0.15); color: #ff6767; }
    .medium { background: rgba(255,165,0,0.15); color: #ffb347; }
    .low { background: rgba(0,255,65,0.12); color: #00ff41; }

    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }

    .issue-card {
        background: #071107;
        border: 1px solid #123312;
        border-radius: 14px;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
        flex-wrap: wrap;
    }

    .auth-card {
        max-width: 420px;
        margin: 3rem auto;
        background: #071107;
        border: 1px solid #123312;
        border-radius: 18px;
        padding: 2rem;
    }

    .role-chip {
        background: rgba(0,255,65,0.1);
        color: #00ff41;
        border: 1px solid rgba(0,255,65,0.2);
        padding: 0.3rem 0.75rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 700;
        display: inline-block;
    }
    /* Green toggles */
    .stToggle > div > div {
        background-color: #00ff41 !important;
    }

    .stToggle [data-checked="true"] > div {
        background-color: #00ff41 !important;
    }

    div[data-testid="stToggle"] label div {
        background-color: #00ff41 !important;
    }

    /* Status styles */
    .status-blocked {
        background: linear-gradient(90deg, rgba(255,40,40,0.15), transparent);
        border-left: 3px solid #ff2828;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.5rem;
        color: #ff6b6b;
        font-weight: 600;
        font-size: 0.95rem;
        margin-top: 0.5rem;
    }

    .status-passed {
        background: linear-gradient(90deg, rgba(0,255,65,0.1), transparent);
        border-left: 3px solid #00ff41;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.5rem;
        color: #00ff41;
        font-weight: 600;
        font-size: 0.95rem;
        margin-top: 0.5rem;
    }
    #MainMenu {visibility: hidden;}
    header {visibility: hidden; height: 0 !important; min-height: 0 !important;}
    footer {visibility: hidden;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    .stAppHeader {display: none !important;}
    section[data-testid="stSidebarContent"] ~ div > div:first-child {display: none !important;}</style>
    """, unsafe_allow_html=True)

# =========================
# AUTH SCREENS
# =========================
def show_signup():
    left, center, right = st.columns([1.2, 1, 1.2])

    with center:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown('<div class="brand">🛡️ VexilGuard</div>', unsafe_allow_html=True)
        st.markdown('<p class="muted">Create a secure account to access your role-based dashboard.</p>', unsafe_allow_html=True)

        with st.form("signup_form"):
            name = st.text_input("Full name", placeholder="Enter your full name")
            username = st.text_input("Username", placeholder="Choose a username")
            password = st.text_input("Password", type="password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm password", type="password", placeholder="Re-enter password")
            role = st.selectbox("Role", ["developer", "security_team", "admin"])
            submitted = st.form_submit_button("Create account", use_container_width=True)

            if submitted:
                if not name or not username or not password or not confirm_password:
                    st.error("All fields are required.")
                elif len(password) < 8:
                    st.error("Password must be at least 8 characters long.")
                elif password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    ok, msg = create_user(name, username, password, role)
                    if ok:
                        st.success(msg)
                        st.session_state.page = "signin"
                        st.rerun()
                    else:
                        st.error(msg)

        if st.button("Already have an account? Sign in", use_container_width=True):
            st.session_state.page = "signin"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

def show_signin():
    left, center, right = st.columns([1.2, 1, 1.2])

    with center:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown('<div class="brand">🛡️ VexilGuard</div>', unsafe_allow_html=True)
        st.markdown('<p class="muted">Sign in to continue to your secured DevSecOps workspace.</p>', unsafe_allow_html=True)

        with st.form("signin_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Sign in", use_container_width=True)

            if submitted:
                ok, user = authenticate_user(username, password)
                if ok:
                    st.session_state.authenticated = True
                    st.session_state.username = user["username"]
                    st.session_state.name = user["name"]
                    st.session_state.role = user["role"]
                    st.success("Login successful.")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        if st.button("New user? Create account", use_container_width=True):
            st.session_state.page = "signup"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# =========================
# ROLE PANELS
# =========================
def render_developer_features(issues):
    total, high, medium, low = metrics_from_issues(issues)

    st.markdown('<div class="section-title">Developer Workspace</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    for col, label, val, color in [
        (c1, "Total Issues", total, "#00ff41"),
        (c2, "High", high, "#ff6767"),
        (c3, "Medium", medium, "#ffb347"),
        (c4, "Low", low, "#00ff41")
    ]:
        with col:
            st.markdown(
                f'<div class="metric"><div>{label}</div><div class="metric-num" style="color:{color}">{val}</div></div>',
                unsafe_allow_html=True
            )

    st.markdown('<div class="section-title">AI Fix Recommendations</div>', unsafe_allow_html=True)
    for idx, issue in enumerate(issues):
        sev = issue.get("severity", "LOW").lower()
        st.markdown('<div class="issue-card">', unsafe_allow_html=True)
        st.markdown(
            f"**{issue.get('issue')}**  \n`{issue.get('file')}` · Line {issue.get('line')}  \n"
            f'<span class="badge {sev}">{issue.get("severity")}</span>',
            unsafe_allow_html=True
        )
        col1, col2 = st.columns(2)
        with col1:
            st.caption("Vulnerable code")
            st.code(issue.get("code", ""), language="python")
        with col2:
            st.caption("AI mentor guidance")
            st.write(issue.get("ai_feedback", "No feedback available."))
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Remediation Checklist</div>', unsafe_allow_html=True)
    steps = [
        "Read each vulnerability carefully",
        "Open the impacted file",
        "Apply the secure fix",
        "Run Bandit locally",
        "Commit with a clean message",
        "Push and rescan"
    ]
    done = 0
    for step in steps:
        checked = st.checkbox(step, key=f"dev_{step}")
        if checked:
            done += 1
    st.progress(done / len(steps))
    st.caption(f"{done}/{len(steps)} steps completed.")

def render_security_features(issues):
    st.markdown('<div class="section-title">Security Team Controls</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass">', unsafe_allow_html=True)

    triage_df = pd.DataFrame([
        {
            "Issue": i.get("issue"),
            "File": i.get("file"),
            "Severity": i.get("severity"),
            "Assigned To": "Unassigned",
            "Status": "Open"
        }
        for i in issues
    ])
    st.dataframe(triage_df, use_container_width=True)

    selected = st.selectbox(
        "Select issue for triage",
        options=[f"{i.get('issue')} — {i.get('file')}" for i in issues]
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        st.selectbox("Override severity", ["HIGH", "MEDIUM", "LOW"], key="override_severity")
    with col2:
        st.selectbox("Assign reviewer", ["Unassigned", "Security Lead", "AppSec Analyst"], key="assign_reviewer")
    with col3:
        st.selectbox("Mark status", ["Open", "In Review", "False Positive", "Resolved"], key="mark_status")

    st.button("Save triage update")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Team Analytics</div>', unsafe_allow_html=True)
    sev_counts = pd.DataFrame({
        "Severity": ["HIGH", "MEDIUM", "LOW"],
        "Count": [
            len([i for i in issues if i.get("severity") == "HIGH"]),
            len([i for i in issues if i.get("severity") == "MEDIUM"]),
            len([i for i in issues if i.get("severity") == "LOW"])
        ]
    })
    fig = px.bar(sev_counts, x="Severity", y="Count", color="Severity",
                 color_discrete_map={"HIGH": "#ff6767", "MEDIUM": "#ffb347", "LOW": "#00ff41"})
    fig.update_layout(
        paper_bgcolor="#071107",
        plot_bgcolor="#071107",
        font=dict(color="#e6e6e6")
    )
    st.plotly_chart(fig, use_container_width=True)

def render_admin_features():
    st.markdown('<div class="section-title">Admin Controls</div>', unsafe_allow_html=True)
    users = load_users()
    st.markdown('<div class="glass">', unsafe_allow_html=True)

    if users:
        df = pd.DataFrame([
            {
                "Name": u["name"],
                "Username": u["username"],
                "Role": u["role"],
                "Created": u["created_at"]
            } for u in users
        ])
        st.dataframe(df, use_container_width=True)

        usernames = [u["username"] for u in users]
        selected_user = st.selectbox("Select user", usernames)
        new_role = st.selectbox("Change role to", ["developer", "security_team", "admin"])

        if st.button("Update user role"):
            for u in users:
                if u["username"] == selected_user:
                    u["role"] = new_role
                    break
            save_users(users)
            st.success("User role updated.")
            st.rerun()
    else:
        st.info("No users found.")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">System Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.toggle("Enable live scan on push", value=True)
    st.toggle("Enable secret scanning", value=True)
    st.toggle("Enable AI mentor", value=True)
    st.selectbox("Default branch", ["main", "dev", "staging"])
    st.selectbox("Risk threshold to block pipeline", ["HIGH", "MEDIUM", "LOW"])
    st.button("Save system settings")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Audit Log</div>', unsafe_allow_html=True)
    log_df = pd.DataFrame([
        {"Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Event": "Admin viewed dashboard", "Actor": st.session_state.username},
        {"Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Event": "Role management opened", "Actor": st.session_state.username},
    ])
    st.dataframe(log_df, use_container_width=True)

# =========================
# APP SHELL
# =========================
def logout():
    for key in ["authenticated", "username", "name", "role"]:
        st.session_state[key] = None if key != "authenticated" else False
    st.session_state.page = "signin"
    st.rerun()

def show_app():
    issues = get_active_issues()
    total, high, medium, low = metrics_from_issues(issues)

    with st.sidebar:
        st.markdown('<div class="brand">🛡️ VexilGuard</div>', unsafe_allow_html=True)
        st.markdown(f"**User:** {st.session_state.name}")
        st.markdown(f"**Username:** `{st.session_state.username}`")
        st.markdown(f'<span class="role-chip">{st.session_state.role}</span>', unsafe_allow_html=True)
        st.divider()

        if st.button("⟳ LIVE SCAN", use_container_width=True):
            run_live_scan()
            st.success("Scan completed.")
            st.rerun()

        st.download_button(
            "Download issues CSV",
            data=pd.DataFrame(issues).to_csv(index=False),
            file_name="vexilguard_issues.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.divider()
        st.write("### Scan Metadata")
        st.caption(f"Last scan: {st.session_state.scan_time or 'Not run in this session'}")
        st.caption("SAST Engine: Bandit")
        st.caption("Secret Scanner: Gitleaks")
        st.caption("AI Engine: Groq LLaMA")
        st.caption("Trigger: Git push / manual scan")

        st.divider()
        if st.button("Logout", use_container_width=True):
            logout()

    st.markdown(
        f"""
        <div class="topbar">
            <div>
                <div class="brand">VexilGuard</div>
                <div class="muted">Role-based DevSecOps dashboard with secure authentication and live scan controls.</div>
            </div>
            <div class="role-chip">{st.session_state.role}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <div class="hero">
        <div style="font-family:'Space Grotesk',sans-serif; font-size:3.5rem; font-weight:800; color:#ffffff; letter-spacing:-2px; line-height:1.1; margin-bottom:0.5rem;">
            Shift Security <span style="color:#00ff41;">Left.</span>
        </div>
        <div style="color:#666; font-size:1rem; margin-bottom:1.2rem;">
            Scan code, review issues, teach remediation, and manage security operations from a single dashboard.
        </div>
        {'<div class="status-blocked">🚫 Pipeline blocked — ' + str(high) + ' high-severity issue(s) found. Fix these and you\'re good to go!</div>' if high > 0 else '<div class="status-passed">✅ Pipeline passed — excellent work! No high-severity issues detected.</div>'}
    </div>
    """, unsafe_allow_html=True)

    render_developer_features(issues)

    if st.session_state.role in ["security_team", "admin"]:
        render_security_features(issues)

    if st.session_state.role == "admin":
        render_admin_features()

# =========================
# ROUTER
# =========================
if not st.session_state.authenticated:
    if st.session_state.page == "signup":
        show_signup()
    else:
        show_signin()
else:
    show_app()