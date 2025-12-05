# src/ai_analyzer.py
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

class SecurityAnalyzer:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.getenv('ANTHROPIC_API_KEY')
        )

    def analyze_scan_results(self, scanner_results):
        """Send scanner results to Claude for analysis"""

        # Combine all scanner outputs
        combined_results = "\n\n".join([
            f"# {tool_name.upper()} Results\n{content}"
            for tool_name, content in scanner_results.items()
        ])

        prompt = f"""You are an expert penetration tester analyzing security scan results.

SCAN RESULTS:
{combined_results}

Please analyze these results and create a comprehensive security assessment report with:

1. EXECUTIVE SUMMARY
   - Brief overview of the security posture
   - Total number of vulnerabilities found
   - Risk rating (Critical/High/Medium/Low)

2. VULNERABILITY SUMMARY
   - List all vulnerabilities found
   - Categorize by severity (Critical, High, Medium, Low)
   - Include CVE numbers if applicable

3. DETAILED FINDINGS
   For each vulnerability:
   - Description of the issue
   - Affected component/service
   - Severity rating and justification
   - Proof of concept or evidence
   - Business impact

4. REMEDIATION RECOMMENDATIONS
   For each vulnerability:
   - Specific corrective actions
   - Priority order
   - Estimated effort (Low/Medium/High)
   - Prevention strategies

5. CONCLUSION
   - Overall security posture assessment
   - Priority vulnerabilities to address immediately
   - Long-term security recommendations

Format the report professionally with clear sections and markdown formatting."""

        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )

        return message.content[0].text
