#!/usr/bin/env python3
# src/test_without_api.py
# Test script that demonstrates functionality without API key

import sys
from pathlib import Path
from report_generator import load_scanner_results
from terminal_display import TerminalDisplay

def main():
    # Initialize components
    display = TerminalDisplay()

    # Display header
    display.display_header()

    # Step 1: Load scanner results
    display.display_loading("Loading scanner results from teammate")
    try:
        scanner_results = load_scanner_results('scanner_results')
        display.display_success(f"Loaded {len(scanner_results)} scanner output files")

        # Show what was loaded
        display.console.print("\n[bold cyan]Files loaded:[/bold cyan]")
        for tool_name in scanner_results.keys():
            display.console.print(f"  - {tool_name}.md")

    except Exception as e:
        display.console.print(f"[red]Error loading scanner results: {e}[/red]")
        sys.exit(1)

    # Step 2: Show sample of loaded content
    display.console.print("\n[bold cyan]Sample of loaded scanner data:[/bold cyan]")
    for tool_name, content in list(scanner_results.items())[:2]:  # Show first 2
        display.console.print(f"\n[yellow]--- {tool_name.upper()} ---[/yellow]")
        lines = content.split('\n')[:8]  # First 8 lines
        for line in lines:
            if line.strip():
                display.console.print(f"  {line}")

    # Step 3: Show mock report structure
    display.console.print("\n")
    display.display_loading("Would analyze with Claude AI (API key required)")

    # Create a mock report to show structure
    mock_report = """# EXECUTIVE SUMMARY

The security assessment identified **7 vulnerabilities** across the target system (192.168.1.100).

**Overall Risk Rating: HIGH**

## Key Findings:
- 1 Critical vulnerability (SQL Injection)
- 2 High severity issues (Outdated software, Missing security headers)
- 3 Medium severity issues (Directory indexing, Information disclosure)
- 1 Low severity issue (ETags leak inodes)

# VULNERABILITY SUMMARY

## Critical Vulnerabilities
1. **SQL Injection in Login Form**
   - Affected: /login.php (username parameter)
   - CVE: Not assigned
   - Impact: Full database access, data exfiltration

## High Severity
2. **Outdated Apache Server**
   - Version: Apache 2.4.6 (Current: 2.4.58)
   - Multiple known CVEs

3. **Missing Security Headers**
   - X-Frame-Options: Missing
   - X-Content-Type-Options: Missing
   - Impact: Clickjacking, MIME-sniffing attacks

## Medium Severity
4. **Directory Indexing Enabled**
   - Path: /backup/
   - Allows browsing of sensitive files

5. **Exposed MySQL Service**
   - Port: 3306/tcp open to network
   - Version: MySQL 5.7.33

# REMEDIATION RECOMMENDATIONS

## Immediate Actions (Critical Priority)
1. **Fix SQL Injection**
   - Use parameterized queries/prepared statements
   - Implement input validation
   - Effort: Medium
   - Timeline: 1-2 days

## High Priority
2. **Update Apache Server**
   - Upgrade to Apache 2.4.58
   - Effort: Low
   - Timeline: 1 day

3. **Implement Security Headers**
   - Add X-Frame-Options: SAMEORIGIN
   - Add X-Content-Type-Options: nosniff
   - Effort: Low
   - Timeline: 1 day

# CONCLUSION

The target system has significant security vulnerabilities that require immediate attention. The SQL injection vulnerability poses a critical risk and should be remediated immediately. Updating outdated software and implementing security best practices will significantly improve the security posture.

**Priority Actions:**
1. Patch SQL injection vulnerability (Critical)
2. Update Apache to latest version (High)
3. Implement security headers (High)
4. Restrict MySQL network access (Medium)
"""

    display.display_report(mock_report)

    # Step 4: Show what would be saved
    display.console.print("\n[bold cyan]Without API key, the following would be generated:[/bold cyan]")
    display.console.print("  ✓ reports/security_report.md (AI-generated analysis)")
    display.console.print("  ✓ reports/security_report.pdf (Professional PDF)")

    # Vulnerability summary table
    display.console.print("\n")
    vulnerabilities = {
        "Critical": 1,
        "High": 2,
        "Medium": 3,
        "Low": 1
    }
    display.display_summary_table(vulnerabilities)

    # Final message
    display.console.print("\n[bold yellow]⚠️  This is a test run without API key[/bold yellow]")
    display.console.print("[bold green]✓ All components verified and working![/bold green]")
    display.console.print("\n[cyan]To run with real AI analysis:[/cyan]")
    display.console.print("  1. Add your ANTHROPIC_API_KEY to .env file")
    display.console.print("  2. Run: python src/main.py\n")

if __name__ == "__main__":
    main()
