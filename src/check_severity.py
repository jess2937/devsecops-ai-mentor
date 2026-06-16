import json
import sys
import os

def check_bandit_results():
    report_path = "reports/bandit_report.json"
    
    if not os.path.exists(report_path):
        print("⚠️ No Bandit report found.")
        return 0
    
    with open(report_path, "r") as f:
        data = json.load(f)
    
    critical_count = 0
    high_count = 0
    
    for issue in data.get("results", []):
        severity = issue.get("issue_severity", "").upper()
        if severity == "HIGH":
            high_count += 1
        elif severity == "CRITICAL":
            critical_count += 1
    
    print(f"🔍 Critical issues: {critical_count}")
    print(f"🔍 High issues: {high_count}")
    
    return critical_count + high_count

def check_gitleaks_results():
    report_path = "reports/gitleaks_report.json"
    
    if not os.path.exists(report_path):
        print("⚠️ No Gitleaks report found.")
        return 0
    
    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return 0
    
    secret_count = len(data) if isinstance(data, list) else 0
    print(f"🔐 Secrets found: {secret_count}")
    return secret_count

if __name__ == "__main__":
    print("🚀 Running security checks...")
    
    bandit_issues = check_bandit_results()
    secret_issues = check_gitleaks_results()
    
    total = bandit_issues + secret_issues
    
    if total > 0:
        print(f"❌ Pipeline BLOCKED — {total} critical issue(s) found!")
        sys.exit(1)
    else:
        print("✅ Pipeline PASSED — No critical issues found!")
        sys.exit(0)