"""
Scanner Functions Module

This module provides Python functions to execute various network and security
scanning tools, with automatic markdown report generation.

Each function executes a scanning tool and generates a markdown report containing:
- Scan parameters and configuration
- Tool output and results
- Timestamp and execution details
- Raw output and processed data

Usage:
    from src.scanners import nmap_scan, sqlmap_scan, dirb_scan

    nmap_scan("192.168.1.0/24", "/path/to/results")
    sqlmap_scan("http://target.com", "/path/to/results", target_url="/api/user")
    dirb_scan("http://target.com", "/path/to/results")
"""

import subprocess
import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


def _ensure_output_dir(destination_dir: str) -> Path:
    """
    Ensure the output directory exists.

    Args:
        destination_dir: Path to the output directory

    Returns:
        Path object of the output directory
    """
    output_path = Path(destination_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def _write_markdown_report(filename: str, destination_dir: str, content: str) -> str:
    """
    Write a markdown report to file.

    Args:
        filename: Name of the markdown file (without extension)
        destination_dir: Output directory path
        content: Markdown content to write

    Returns:
        Path to the created file
    """
    output_path = _ensure_output_dir(destination_dir)
    report_path = output_path / f"{filename}.md"

    with open(report_path, 'w') as f:
        f.write(content)

    return str(report_path)


def _execute_command(command: List[str], timeout: int = 300) -> Dict[str, Any]:
    """
    Execute a system command and capture output.

    Args:
        command: List of command arguments
        timeout: Maximum execution time in seconds (default: 300)

    Returns:
        Dictionary with stdout, stderr, and return code
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode,
            'success': result.returncode == 0
        }
    except subprocess.TimeoutExpired:
        return {
            'stdout': '',
            'stderr': f'Command timed out after {timeout} seconds',
            'returncode': -1,
            'success': False
        }
    except Exception as e:
        return {
            'stdout': '',
            'stderr': str(e),
            'returncode': -1,
            'success': False
        }


def nmap_scan(target: str, destination_dir: str,
              scan_type: str = "-sS", additional_args: Optional[List[str]] = None) -> str:
    """
    Execute an nmap network scan and generate a markdown report.

    Nmap is a powerful network mapper that scans for open ports and services.
    Common scan types:
    - -sS: TCP SYN stealth scan (default, requires root)
    - -sT: TCP connect scan
    - -sU: UDP scan
    - -sA: TCP ACK scan (for firewall mapping)
    - -sP: Ping scan

    Args:
        target: Target IP address or CIDR range (e.g., "192.168.1.0/24")
        destination_dir: Directory to store markdown report
        scan_type: Type of scan to perform (default: "-sS")
        additional_args: Additional nmap arguments as list

    Returns:
        Path to generated markdown report

    Example:
        >>> nmap_scan("192.168.1.100", "./results", scan_type="-sT")
        './results/nmap.md'
    """
    timestamp = datetime.datetime.now().isoformat()

    # Build command
    command = ["nmap", scan_type, "-v"]

    if additional_args:
        command.extend(additional_args)

    command.append(target)

    # Execute scan
    result = _execute_command(command, timeout=600)

    # Generate markdown report
    markdown_content = f"""# Nmap Scan Report

**Target:** {target}
**Scan Type:** {scan_type}
**Timestamp:** {timestamp}
**Status:** {'✓ Success' if result['success'] else '✗ Failed'}

## Scan Parameters

- **Target:** {target}
- **Scan Type:** {scan_type}
- **Additional Arguments:** {', '.join(additional_args) if additional_args else 'None'}
- **Execution Time:** {timestamp}

## Results

### Command Output

\\`\\`\\`
{result['stdout']}
\\`\\`\\`

### Errors (if any)

\\`\\`\\`
{result['stderr'] if result['stderr'] else 'None'}
\\`\\`\\`

### Return Code

{result['returncode']}

## Summary

This scan used nmap to identify open ports and running services on the target network.
Review the output above for details on discovered hosts and open ports.
"""

    return _write_markdown_report("nmap", destination_dir, markdown_content)


def sqlmap_scan(target: str, destination_dir: str,
                target_url: str = "", additional_args: Optional[List[str]] = None) -> str:
    """
    Execute a sqlmap SQL injection vulnerability scan and generate a markdown report.

    SQLMap is an open-source tool that automates the detection and exploitation
    of SQL injection vulnerabilities.

    Args:
        target: Target domain or IP (used for context/identification)
        destination_dir: Directory to store markdown report
        target_url: Full URL to test for SQL injection (e.g., "http://target.com/page?id=1")
        additional_args: Additional sqlmap arguments as list

    Returns:
        Path to generated markdown report

    Example:
        >>> sqlmap_scan("target.com", "./results",
        ...             target_url="http://target.com/user?id=1",
        ...             additional_args=["--batch", "--level=3"])
        './results/sqlmap.md'
    """
    timestamp = datetime.datetime.now().isoformat()

    if not target_url:
        target_url = f"http://{target}"

    # Build command
    command = ["sqlmap", "-u", target_url, "--batch", "-v", "1"]

    if additional_args:
        command.extend(additional_args)

    # Execute scan
    result = _execute_command(command, timeout=600)

    # Generate markdown report
    markdown_content = f"""# SQLMap SQL Injection Scan Report

**Target:** {target}
**Target URL:** {target_url}
**Timestamp:** {timestamp}
**Status:** {'✓ Success' if result['success'] else '✗ Failed'}

## Scan Parameters

- **Target Domain:** {target}
- **Target URL:** {target_url}
- **Additional Arguments:** {', '.join(additional_args) if additional_args else 'None'}
- **Execution Time:** {timestamp}

## Results

### Command Output

\\`\\`\\`
{result['stdout']}
\\`\\`\\`

### Errors (if any)

\\`\\`\\`
{result['stderr'] if result['stderr'] else 'None'}
\\`\\`\\`

### Return Code

{result['returncode']}

## Summary

This scan used SQLMap to test for SQL injection vulnerabilities at the target URL.
SQLMap attempts to identify injection points and may provide database information
if vulnerabilities are discovered.

⚠️ **Important:** Ensure you have explicit permission before testing for SQL injection.
"""

    return _write_markdown_report("sqlmap", destination_dir, markdown_content)


def dirb_scan(target: str, destination_dir: str,
              wordlist: str = "/usr/share/dirb/wordlists/common.txt",
              additional_args: Optional[List[str]] = None) -> str:
    """
    Execute a dirb directory brute-force scan and generate a markdown report.

    Dirb is a web content scanner that uses dictionary-based directory enumeration
    to find hidden directories and files on web servers.

    Args:
        target: Target URL (e.g., "http://target.com")
        destination_dir: Directory to store markdown report
        wordlist: Path to wordlist file (default: common.txt from dirb)
        additional_args: Additional dirb arguments as list

    Returns:
        Path to generated markdown report

    Example:
        >>> dirb_scan("http://target.com", "./results",
        ...           additional_args=["-r", "-z"])
        './results/dirb.md'
    """
    timestamp = datetime.datetime.now().isoformat()

    # Build command
    command = ["dirb", target, wordlist, "-o", "/tmp/dirb_output.txt"]

    if additional_args:
        command.extend(additional_args)

    # Execute scan
    result = _execute_command(command, timeout=600)

    # Try to read the output file
    dirb_output = ""
    try:
        with open("/tmp/dirb_output.txt", 'r') as f:
            dirb_output = f.read()
        os.remove("/tmp/dirb_output.txt")
    except:
        pass

    # Generate markdown report
    markdown_content = f"""# Dirb Directory Brute-Force Scan Report

**Target:** {target}
**Wordlist:** {wordlist}
**Timestamp:** {timestamp}
**Status:** {'✓ Success' if result['success'] else '✗ Failed'}

## Scan Parameters

- **Target URL:** {target}
- **Wordlist:** {wordlist}
- **Additional Arguments:** {', '.join(additional_args) if additional_args else 'None'}
- **Execution Time:** {timestamp}

## Results

### Command Output

\\`\\`\\`
{result['stdout']}
\\`\\`\\`

### Detailed Output

\\`\\`\\`
{dirb_output if dirb_output else result['stderr']}
\\`\\`\\`

### Return Code

{result['returncode']}

## Summary

This scan used dirb to enumerate hidden directories and files on the target web server.
Results show HTTP status codes for discovered paths. Status codes indicate:
- 200: OK (found)
- 301/302: Redirect
- 403: Forbidden
- 404: Not Found

⚠️ **Note:** Dirb performs many requests and may trigger IDS/IPS systems or rate limiting.
"""

    return _write_markdown_report("dirb", destination_dir, markdown_content)


def nikto_scan(target: str, destination_dir: str,
               additional_args: Optional[List[str]] = None) -> str:
    """
    Execute a nikto web server vulnerability scan and generate a markdown report.

    Nikto is an open-source web server vulnerability scanner that performs
    comprehensive tests against web servers for dangerous files and programs.

    Args:
        target: Target URL (e.g., "http://target.com")
        destination_dir: Directory to store markdown report
        additional_args: Additional nikto arguments as list

    Returns:
        Path to generated markdown report

    Example:
        >>> nikto_scan("http://target.com", "./results", additional_args=["-o", "full"])
        './results/nikto.md'
    """
    timestamp = datetime.datetime.now().isoformat()

    # Build command
    command = ["nikto", "-h", target, "-noSSL", "-nointeractive", "-o", "/tmp/nikto_output.txt"]

    if additional_args:
        command.extend(additional_args)

    # Execute scan
    result = _execute_command(command, timeout=600)

    # Try to read the output file
    nikto_output = ""
    try:
        with open("/tmp/nikto_output.txt", 'r') as f:
            nikto_output = f.read()
        os.remove("/tmp/nikto_output.txt")
    except:
        pass

    # Generate markdown report
    markdown_content = f"""# Nikto Web Server Vulnerability Scan Report

**Target:** {target}
**Timestamp:** {timestamp}
**Status:** {'✓ Success' if result['success'] else '✗ Failed'}

## Scan Parameters

- **Target URL:** {target}
- **Additional Arguments:** {', '.join(additional_args) if additional_args else 'None'}
- **Execution Time:** {timestamp}

## Results

### Command Output

\\`\\`\\`
{result['stdout']}
\\`\\`\\`

### Detailed Findings

\\`\\`\\`
{nikto_output if nikto_output else result['stderr']}
\\`\\`\\`

### Return Code

{result['returncode']}

## Summary

This scan used nikto to identify web server vulnerabilities, misconfigurations,
dangerous files, and outdated server software. Findings are typically categorized
by severity and include information about:

- Outdated software versions
- Default credentials
- Dangerous files and directories
- Missing security headers
- Information disclosure vulnerabilities

Review the findings above and prioritize remediation based on severity.
"""

    return _write_markdown_report("nikto", destination_dir, markdown_content)


def masscan_scan(target: str, destination_dir: str,
                 port_range: str = "1-65535", rate: int = 1000,
                 additional_args: Optional[List[str]] = None) -> str:
    """
    Execute a masscan fast port scan and generate a markdown report.

    Masscan is one of the fastest network port scanners, capable of scanning
    the entire internet in under 6 minutes. It performs banner grabbing and
    supports various output formats.

    Args:
        target: Target IP address or CIDR range
        destination_dir: Directory to store markdown report
        port_range: Port range to scan (default: "1-65535")
        rate: Packets per second to send (default: 1000)
        additional_args: Additional masscan arguments as list

    Returns:
        Path to generated markdown report

    Example:
        >>> masscan_scan("192.168.1.0/24", "./results", port_range="80,443,8080")
        './results/masscan.md'
    """
    timestamp = datetime.datetime.now().isoformat()

    # Build command
    command = ["masscan", target, "-p", port_range, "--rate", str(rate),
               "-oJ", "/tmp/masscan_output.json"]

    if additional_args:
        command.extend(additional_args)

    # Execute scan
    result = _execute_command(command, timeout=900)

    # Try to read the JSON output file
    masscan_results = ""
    try:
        with open("/tmp/masscan_output.json", 'r') as f:
            masscan_results = f.read()
        os.remove("/tmp/masscan_output.json")
    except:
        pass

    # Generate markdown report
    markdown_content = f"""# Masscan Fast Port Scan Report

**Target:** {target}
**Port Range:** {port_range}
**Rate:** {rate} packets/second
**Timestamp:** {timestamp}
**Status:** {'✓ Success' if result['success'] else '✗ Failed'}

## Scan Parameters

- **Target:** {target}
- **Port Range:** {port_range}
- **Packet Rate:** {rate} packets/second
- **Additional Arguments:** {', '.join(additional_args) if additional_args else 'None'}
- **Execution Time:** {timestamp}

## Results

### Command Output

\\`\\`\\`
{result['stdout']}
\\`\\`\\`

### Scan Results (JSON format)

\\`\\`\\`json
{masscan_results if masscan_results else result['stderr']}
\\`\\`\\`

### Return Code

{result['returncode']}

## Summary

This scan used masscan to rapidly identify open ports on the target network.
Masscan is significantly faster than traditional port scanners and is effective
for large-scale network reconnaissance.

**Note:** Higher rate values may result in lost packets or dropped responses.
Adjust the rate parameter based on network conditions and target responsiveness.
"""

    return _write_markdown_report("masscan", destination_dir, markdown_content)


def whois_lookup(target: str, destination_dir: str) -> str:
    """
    Perform a WHOIS lookup and generate a markdown report.

    WHOIS lookups retrieve registration information about domain names and IP addresses,
    including registrant contact details, nameservers, and registration dates.

    Args:
        target: Domain name or IP address to look up
        destination_dir: Directory to store markdown report

    Returns:
        Path to generated markdown report

    Example:
        >>> whois_lookup("example.com", "./results")
        './results/whois.md'
    """
    timestamp = datetime.datetime.now().isoformat()

    # Build command
    command = ["whois", target]

    # Execute lookup
    result = _execute_command(command, timeout=30)

    # Generate markdown report
    markdown_content = f"""# WHOIS Lookup Report

**Target:** {target}
**Timestamp:** {timestamp}
**Status:** {'✓ Success' if result['success'] else '✗ Failed'}

## Lookup Parameters

- **Target Domain/IP:** {target}
- **Execution Time:** {timestamp}

## Results

### WHOIS Data

\\`\\`\\`
{result['stdout']}
\\`\\`\\`

### Errors (if any)

\\`\\`\\`
{result['stderr'] if result['stderr'] else 'None'}
\\`\\`\\`

### Return Code

{result['returncode']}

## Summary

This lookup retrieved WHOIS registration information for the target. WHOIS data includes:

- **Registrant Information:** Domain owner or organization details
- **Administrative Contact:** Domain administrator information
- **Technical Contact:** Technical point of contact
- **Nameservers:** DNS servers for the domain
- **Registration Date:** When the domain was registered
- **Expiration Date:** When the domain registration expires
- **Registrar:** Organization that registered the domain

This information is useful for identifying domain ownership and can assist in
social engineering assessments or supply chain analysis.
"""

    return _write_markdown_report("whois", destination_dir, markdown_content)


def dns_enum(target: str, destination_dir: str,
             additional_args: Optional[List[str]] = None) -> str:
    """
    Perform DNS enumeration and record lookups and generate a markdown report.

    DNS enumeration retrieves DNS records (A, AAAA, MX, NS, TXT, CNAME, SOA)
    which can reveal server infrastructure, mail servers, and domain configuration.

    Args:
        target: Domain name to enumerate
        destination_dir: Directory to store markdown report
        additional_args: Additional dig arguments as list

    Returns:
        Path to generated markdown report

    Example:
        >>> dns_enum("example.com", "./results")
        './results/dns_enum.md'
    """
    timestamp = datetime.datetime.now().isoformat()

    # Execute multiple DNS queries
    record_types = ["A", "AAAA", "MX", "NS", "TXT", "SOA", "CNAME"]
    dns_results = {}

    for record_type in record_types:
        command = ["dig", target, record_type, "+short"]
        result = _execute_command(command, timeout=10)
        dns_results[record_type] = result['stdout']

    # Also perform AXFR (zone transfer) attempt
    command = ["dig", target, "AXFR"]
    axfr_result = _execute_command(command, timeout=10)

    # Generate markdown report
    markdown_content = f"""# DNS Enumeration Report

**Target Domain:** {target}
**Timestamp:** {timestamp}
**Status:** ✓ Completed

## Lookup Parameters

- **Target Domain:** {target}
- **Execution Time:** {timestamp}

## DNS Records

### A Records (IPv4 Addresses)

\\`\\`\\`
{dns_results['A'] if dns_results['A'] else 'No records found'}
\\`\\`\\`

### AAAA Records (IPv6 Addresses)

\\`\\`\\`
{dns_results['AAAA'] if dns_results['AAAA'] else 'No records found'}
\\`\\`\\`

### MX Records (Mail Servers)

\\`\\`\\`
{dns_results['MX'] if dns_results['MX'] else 'No records found'}
\\`\\`\\`

### NS Records (Nameservers)

\\`\\`\\`
{dns_results['NS'] if dns_results['NS'] else 'No records found'}
\\`\\`\\`

### TXT Records

\\`\\`\\`
{dns_results['TXT'] if dns_results['TXT'] else 'No records found'}
\\`\\`\\`

### SOA Records

\\`\\`\\`
{dns_results['SOA'] if dns_results['SOA'] else 'No records found'}
\\`\\`\\`

### CNAME Records

\\`\\`\\`
{dns_results['CNAME'] if dns_results['CNAME'] else 'No records found'}
\\`\\`\\`

## Zone Transfer Attempt (AXFR)

\\`\\`\\`
{axfr_result['stdout'] if axfr_result['stdout'] else 'Zone transfer not permitted (expected)'}
\\`\\`\\`

## Summary

This enumeration retrieved DNS records for the target domain. DNS records reveal:

- **A/AAAA Records:** Server IP addresses
- **MX Records:** Email server infrastructure
- **NS Records:** Authoritative nameservers
- **TXT Records:** Domain verification, SPF, DKIM, DMARC policies
- **SOA Records:** Zone authority and refresh parameters

Zone transfers (AXFR) should be restricted and typically indicate a misconfiguration
if they succeed.
"""

    return _write_markdown_report("dns_enum", destination_dir, markdown_content)