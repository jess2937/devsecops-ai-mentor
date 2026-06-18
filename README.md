<div align="center">

<img src="https://img.shields.io/badge/VexilGuard-DevSecOps-00ff41?style=for-the-badge&logo=shield&logoColor=white" />

# 🛡️ VexilGuard

### AI-Powered DevSecOps Security Scanner & Mentor Platform

*Automatically scans every code push for vulnerabilities, secrets, and misconfigurations — then teaches developers exactly how to fix them using AI.*

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-00ff41?style=for-the-badge&logo=streamlit&logoColor=white)](https://devsecops-ai-mentor-5f39ltfybrg79m72bsca2d.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-jess2937-00ff41?style=for-the-badge&logo=github&logoColor=white)](https://github.com/jess2937/devsecops-ai-mentor)
[![Python](https://img.shields.io/badge/Python-3.11-00ff41?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

</div>

---

## 🚀 What is VexilGuard?

VexilGuard is a **free, cloud-native DevSecOps pipeline** that transforms traditional security scanning into an interactive educational experience.

Most security tools just block your code and say *"something is broken"*. VexilGuard goes further — it analyzes every vulnerability using **Groq AI (LLaMA 3.3)** and generates personalized, beginner-friendly fix recommendations with before-and-after code examples.

> **Built for:** Developers who want to write secure code, security teams who need visibility, and organizations who want to shift security left.

---

## ✨ Key Features

| Feature | Description |
|--------|-------------|
| 🔍 **Automated SAST Scanning** | Bandit scans Python code for vulnerabilities on every `git push` |
| 🔐 **Secret Detection** | Gitleaks scans commit history for exposed API keys and passwords |
| 🤖 **AI Mentor** | Groq LLaMA 3.3 generates personalized fix recommendations |
| 🚫 **Quality Gates** | Pipeline automatically blocks merges when critical issues are found |
| 📊 **Security Dashboard** | Beautiful Streamlit dashboard with real-time scan results |
| 👥 **Role-Based Access** | Developer, Security Team, and Admin roles with different views |
| 🔒 **Secure Authentication** | PBKDF2 password hashing with salt for user accounts |
| 📋 **Issue Triage** | Security team can assign, track, and resolve vulnerabilities |
| ⚙️ **Admin Controls** | User management, system settings, and audit logging |
| 📈 **Team Analytics** | Visual charts showing vulnerability distribution |

---

## 🏗️ Architecture

Developer pushes code

│

▼

┌─────────────────┐

│  GitHub Actions  │  ← Triggers on every push

│    Pipeline      │

└────────┬────────┘

│

┌────┴────┐

│         │

▼         ▼

┌───────┐ ┌──────────┐

│Bandit │ │ Gitleaks │

│ SAST  │ │ Secrets  │

└───┬───┘ └────┬─────┘

│           │

└─────┬─────┘

│

▼

┌───────────────┐

│  results.json │

└───────┬───────┘

│

▼

┌───────────────┐

│   Groq AI     │  ← Generates fix recommendations

│  LLaMA 3.3    │

└───────┬───────┘

│

▼

┌───────────────┐

│  ai_report    │

│    .json      │

└───────┬───────┘

│

▼

┌───────────────┐

│   Streamlit   │  ← VexilGuard Dashboard

│   Dashboard   │

└───────────────┘

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **CI/CD** | GitHub Actions |
| **SAST Engine** | Bandit 1.8 |
| **Secret Scanner** | Gitleaks |
| **AI Engine** | Groq API (LLaMA 3.3 70B) |
| **Dashboard** | Python + Streamlit |
| **Data Viz** | Plotly |
| **Auth** | PBKDF2 + Salt (custom implementation) |
| **Deployment** | Streamlit Cloud (free tier) |

---

## 🔐 Security Pipeline Workflow

Developer pushes code to GitHub
GitHub Actions triggers the security pipeline
Bandit scans src/ for Python vulnerabilities
Gitleaks scans commit history for exposed secrets
Results saved to reports/bandit_report.json
Groq AI analyzes each finding and generates fix recommendations
Enriched report saved to reports/ai_report.json
Pipeline BLOCKS the merge if HIGH severity issues found
VexilGuard dashboard displays results with AI guidance

---

## 📊 Dashboard Roles

### 👨‍💻 Developer
- View all vulnerabilities with severity ratings
- Read AI-generated fix recommendations
- Side-by-side vulnerable vs secure code comparison
- Interactive remediation checklist with progress tracking

### 🔒 Security Team
- Full developer view
- Issue triage — assign reviewers, override severity, mark status
- Team analytics with severity distribution charts
- Live table updates on triage changes

### ⚙️ Admin
- Full security team view
- User management — create, view, update roles
- System settings — toggle scanning features, set risk thresholds
- Audit log — track all admin actions

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Git
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Local Setup

```bash
# Clone the repository
git clone https://github.com/jess2937/devsecops-ai-mentor.git
cd devsecops-ai-mentor

# Install dependencies
pip install -r requirements.txt

# Install Bandit
pip install bandit

# Set your Groq API key
export GROQ_API_KEY=your_key_here   # Linux/Mac
set GROQ_API_KEY=your_key_here      # Windows

# Run a local scan
bandit -r src/ -f json -o reports/bandit_report.json
python src/ai_mentor.py

# Launch the dashboard
streamlit run src/dashboard.py
```

### GitHub Actions Setup

1. Fork this repository
2. Go to **Settings → Secrets → Actions**
3. Add secret: `GROQ_API_KEY` = your Groq API key
4. Push any code change to trigger the pipeline

---

## 📁 Project Structure

devsecops-ai-mentor/

├── .github/

│   └── workflows/

│       └── security.yml          # GitHub Actions pipeline

├── src/

│   ├── app.py                    # Intentionally vulnerable test file

│   ├── ai_mentor.py              # Groq AI analysis script

│   ├── check_severity.py         # Pipeline quality gate

│   └── dashboard.py              # VexilGuard Streamlit dashboard

├── reports/

│   ├── bandit_report.json        # Bandit scan output

│   └── ai_report.json            # AI-enriched vulnerability report

├── requirements.txt              # Python dependencies

└── README.md                     # You are here!

---

## 🔒 Vulnerable Test Cases

The `src/app.py` file contains **intentional vulnerabilities** for testing:

| Vulnerability | Severity | Line |
|--------------|----------|------|
| Weak MD5 hashing | HIGH | 6 |
| Use of `exec()` | MEDIUM | 13 |
| SQL Injection | MEDIUM | 17 |
| Hardcoded API Key | HIGH | 10 |

> ⚠️ These vulnerabilities are intentional for demonstration purposes only.

---

## 📈 Pipeline Results

The pipeline correctly:
- ✅ Detects all 3+ vulnerabilities in the test file
- ✅ Blocks the merge due to HIGH severity issues
- ✅ Generates AI fix recommendations for each issue
- ✅ Saves enriched report as a downloadable artifact

---

## 🎯 What I Learned

Building VexilGuard taught me:
- How to build real CI/CD pipelines with GitHub Actions
- How SAST tools like Bandit analyze Python code
- How to integrate AI APIs (Groq) into automated workflows
- How to implement secure authentication (PBKDF2 + salt)
- How to build role-based access control systems
- How to design and deploy production-ready Streamlit dashboards

---

## 👩‍💻 About the Developer

**Jesinda Rachel** — 3rd year CSE student at Sathyabama Institute of Science and Technology, Chennai. Pursuing a career in DevSecOps.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jesinda-rachel-5802b9311)
[![GitHub](https://img.shields.io/badge/GitHub-jess2937-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/jess2937)

---

<div align="center">

**⭐ If you found this project useful, please star the repository!**

*Built with 💚 using GitHub Actions · Bandit · Gitleaks · Groq AI · Streamlit*

</div>