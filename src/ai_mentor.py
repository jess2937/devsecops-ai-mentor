import json
import os
import time
from groq import Groq

# Configure Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def load_bandit_report():
    report_path = "reports/bandit_report.json"
    if not os.path.exists(report_path):
        print("⚠️ No Bandit report found.")
        return []
    with open(report_path, "r") as f:
        data = json.load(f)
    return data.get("results", [])

def get_ai_fix(issue):
    prompt = f"""
You are a senior security engineer and coding mentor.

A security scanner found this vulnerability:
- Issue: {issue.get('issue_text')}
- Severity: {issue.get('issue_severity')}
- File: {issue.get('filename')}
- Line: {issue.get('line_number')}
- Code: {issue.get('code')}

Please provide:
1. A 2-sentence explanation of why this is dangerous
2. A secure "After" code fix (3-5 lines max)
3. One key lesson to remember

Keep it beginner-friendly and practical.
"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content

def analyze_vulnerabilities():
    issues = load_bandit_report()
    
    if not issues:
        print("✅ No vulnerabilities to analyze!")
        return
    
    results = []
    
    for i, issue in enumerate(issues):
        print(f"\n🔍 Analyzing: {issue.get('issue_text')}")
        
        if i > 0:
            time.sleep(2)
        
        try:
            ai_feedback = get_ai_fix(issue)
        except Exception as e:
            print(f"⚠️ AI analysis failed: {e}")
            ai_feedback = "AI analysis unavailable for this issue."
        
        result = {
            "issue": issue.get("issue_text"),
            "severity": issue.get("issue_severity"),
            "file": issue.get("filename"),
            "line": issue.get("line_number"),
            "code": issue.get("code"),
            "ai_feedback": ai_feedback
        }
        results.append(result)
        print(f"✅ AI feedback generated for issue at line {issue.get('line_number')}")
    
    with open("reports/ai_report.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n🎯 AI analysis complete! {len(results)} vulnerabilities analyzed.")
    print("📄 Report saved to reports/ai_report.json")

if __name__ == "__main__":
    analyze_vulnerabilities()