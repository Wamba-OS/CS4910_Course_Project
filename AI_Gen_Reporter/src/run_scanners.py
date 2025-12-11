#!/usr/bin/env python3
"""
Run Security Scanners
This script executes all security scanning tools and generates markdown reports.
"""

import sys
from pathlib import Path

# Add the parent directory to the path to import from src/scanners.py
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.scanners import (
    nmap_scan,
    sqlmap_scan,
    dirb_scan,
    nikto_scan,
    masscan_scan,
    whois_lookup,
    dns_enum
)


def run_all_scanners(target: str, output_dir: str = "scanner_results"):
    """
    Run all security scanners against the target and generate markdown reports.

    Args:
        target: Target domain/IP to scan
        output_dir: Directory to store all markdown reports (default: scanner_results)

    Returns:
        Dictionary with scan results and paths to generated reports
    """
    # Ensure output directory is relative to AI_Gen_Reporter directory
    script_dir = Path(__file__).parent.parent
    results_dir = script_dir / output_dir
    results_dir.mkdir(parents=True, exist_ok=True)

    results = {
        'target': target,
        'output_dir': str(results_dir),
        'reports': {},
        'errors': []
    }

    print(f"\n{'='*60}")
    print(f"Starting Security Scans for Target: {target}")
    print(f"Output Directory: {results_dir}")
    print(f"{'='*60}\n")

    # 1. WHOIS Lookup (Fast, good starting point)
    print("[1/7] Running WHOIS lookup...")
    try:
        report_path = whois_lookup(target, str(results_dir))
        results['reports']['whois'] = report_path
        print(f"✓ WHOIS report saved to: {report_path}")
    except Exception as e:
        error_msg = f"WHOIS lookup failed: {e}"
        results['errors'].append(error_msg)
        print(f"✗ {error_msg}")

    # 2. DNS Enumeration (Fast, important reconnaissance)
    print("\n[2/7] Running DNS enumeration...")
    try:
        report_path = dns_enum(target, str(results_dir))
        results['reports']['dns_enum'] = report_path
        print(f"✓ DNS enumeration report saved to: {report_path}")
    except Exception as e:
        error_msg = f"DNS enumeration failed: {e}"
        results['errors'].append(error_msg)
        print(f"✗ {error_msg}")

    # 3. Nmap Scan (Port scanning)
    print("\n[3/7] Running Nmap port scan...")
    try:
        # Using -sT (TCP connect) instead of -sS (requires root)
        report_path = nmap_scan(
            target,
            str(results_dir),
            scan_type="-sT",
            additional_args=["-p", "1-1000"]  # Scan first 1000 ports
        )
        results['reports']['nmap'] = report_path
        print(f"✓ Nmap report saved to: {report_path}")
    except Exception as e:
        error_msg = f"Nmap scan failed: {e}"
        results['errors'].append(error_msg)
        print(f"✗ {error_msg}")

    # 4. Nikto Web Server Scan (if target is a web server)
    print("\n[4/7] Running Nikto web vulnerability scan...")
    try:
        # Add http:// prefix if not present
        web_target = target if target.startswith(('http://', 'https://')) else f"http://{target}"
        report_path = nikto_scan(web_target, str(results_dir))
        results['reports']['nikto'] = report_path
        print(f"✓ Nikto report saved to: {report_path}")
    except Exception as e:
        error_msg = f"Nikto scan failed: {e}"
        results['errors'].append(error_msg)
        print(f"✗ {error_msg}")

    # 5. Dirb Directory Brute Force (if target is a web server)
    print("\n[5/7] Running Dirb directory scan...")
    try:
        web_target = target if target.startswith(('http://', 'https://')) else f"http://{target}"
        report_path = dirb_scan(web_target, str(results_dir))
        results['reports']['dirb'] = report_path
        print(f"✓ Dirb report saved to: {report_path}")
    except Exception as e:
        error_msg = f"Dirb scan failed: {e}"
        results['errors'].append(error_msg)
        print(f"✗ {error_msg}")

    # 6. SQLMap (if target has a testable URL parameter)
    print("\n[6/7] Running SQLMap SQL injection scan...")
    try:
        # You may need to customize this URL with actual parameters
        web_target = target if target.startswith(('http://', 'https://')) else f"http://{target}"
        report_path = sqlmap_scan(
            target,
            str(results_dir),
            target_url=web_target,
            additional_args=["--batch", "--risk=1", "--level=1"]
        )
        results['reports']['sqlmap'] = report_path
        print(f"✓ SQLMap report saved to: {report_path}")
    except Exception as e:
        error_msg = f"SQLMap scan failed: {e}"
        results['errors'].append(error_msg)
        print(f"✗ {error_msg}")

    # 7. Masscan (Fast port scanner - requires root, may fail)
    print("\n[7/7] Running Masscan fast port scan...")
    try:
        report_path = masscan_scan(
            target,
            str(results_dir),
            port_range="80,443,8080,8443",
            rate=100
        )
        results['reports']['masscan'] = report_path
        print(f"✓ Masscan report saved to: {report_path}")
    except Exception as e:
        error_msg = f"Masscan scan failed: {e}"
        results['errors'].append(error_msg)
        print(f"✗ {error_msg}")

    # Summary
    print(f"\n{'='*60}")
    print(f"Scan Summary")
    print(f"{'='*60}")
    print(f"Successful scans: {len(results['reports'])}/{7}")
    print(f"Failed scans: {len(results['errors'])}/{7}")
    if results['errors']:
        print(f"\nErrors:")
        for error in results['errors']:
            print(f"  - {error}")
    print(f"\nAll reports saved to: {results_dir}")
    print(f"{'='*60}\n")

    return results


def main():
    """Main entry point for running scanners."""
    if len(sys.argv) < 2:
        print("Usage: python run_scanners.py <target>")
        print("Example: python run_scanners.py scanme.nmap.org")
        print("Example: python run_scanners.py http://testphp.vulnweb.com")
        sys.exit(1)

    target = sys.argv[1]
    results = run_all_scanners(target)

    # Exit with error code if all scans failed
    if len(results['reports']) == 0:
        print("[ERROR] All scans failed!")
        sys.exit(1)

    print("[SUCCESS] Scanner execution complete!")


if __name__ == "__main__":
    main()
