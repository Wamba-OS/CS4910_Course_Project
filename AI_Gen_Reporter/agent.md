# Penetration Testing Report Generator - Part 2

## Overview
This agent takes scan results from pentesting tools (provided by teammate as .md files) and generates professional security reports using Claude AI.

## Project Structure
```
pentest-reporter/
├── agent.md                    # This file
├── scanner_results/            # Input: Tool outputs from Part 1
│   ├── nmap_results.md
│   ├── nikto_results.md
│   ├── sqlmap_results.md
│   └── combined_scan.md
├── reports/                    # Output: Generated reports
│   ├── security_report.md
│   └── security_report.pdf
├── src/
│   ├── report_generator.py    # Main script
│   ├── ai_analyzer.py         # Claude API integration
│   ├── pdf_generator.py       # PDF creation
│   └── terminal_display.py    # Terminal UI
├── requirements.txt
└── README.md
```

## Requirements
```txt
anthropic>=0.20.0
reportlab>=4.0.0
markdown>=3.5.0
rich>=13.7.0
python-dotenv>=1.0.0
```

## Implementation Plan

### Step 1: Read Scanner Output Files
Create a function to read all .md files from Part 1's output.
```python
# src/report_generator.py
import os
from pathlib import Path

def load_scanner_results(results_dir='scanner_results'):
    """Load all scanner result files"""
    results = {}
    results_path = Path(results_dir)
    
    for md_file in results_path.glob('*.md'):
        tool_name = md_file.stem
        with open(md_file, 'r') as f:
            results[tool_name] = f.read()
    
    return results
```

### Step 2: Send to Claude AI for Analysis
Use Claude to analyze vulnerabilities and generate report.
```python
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
```

### Step 3: Display in Terminal
Create a clean terminal interface to show the report.
```python
# src/terminal_display.py
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich import box

class TerminalDisplay:
    def __init__(self):
        self.console = Console()
    
    def display_header(self):
        """Display application header"""
        header = """
╔═══════════════════════════════════════════════════════════╗
║     PENETRATION TESTING REPORT GENERATOR                  ║
║     AI-Powered Security Assessment Tool                   ║
╚═══════════════════════════════════════════════════════════╝
        """
        self.console.print(header, style="bold cyan")
    
    def display_loading(self, message):
        """Display loading message"""
        self.console.print(f"\n[yellow]⚙️  {message}...[/yellow]")
    
    def display_success(self, message):
        """Display success message"""
        self.console.print(f"[green]✓ {message}[/green]")
    
    def display_report(self, report_content):
        """Display the AI-generated report in terminal"""
        self.console.print("\n")
        self.console.print(Panel.fit(
            "SECURITY ASSESSMENT REPORT",
            style="bold white on blue"
        ))
        self.console.print("\n")
        
        # Render markdown in terminal
        md = Markdown(report_content)
        self.console.print(md)
    
    def display_summary_table(self, vulnerabilities):
        """Display vulnerability summary table"""
        table = Table(title="Vulnerability Summary", box=box.ROUNDED)
        
        table.add_column("Severity", style="bold")
        table.add_column("Count", justify="right")
        table.add_column("Status", style="italic")
        
        severity_colors = {
            "Critical": "red",
            "High": "orange1",
            "Medium": "yellow",
            "Low": "green"
        }
        
        for severity, count in vulnerabilities.items():
            color = severity_colors.get(severity, "white")
            table.add_row(
                f"[{color}]{severity}[/{color}]",
                str(count),
                "⚠️  Requires Action" if severity in ["Critical", "High"] else "📋 Review"
            )
        
        self.console.print(table)
```

### Step 4: Generate PDF Report
Create a PDF version of the report.
```python
# src/pdf_generator.py
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import markdown
from io import StringIO

class PDFReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom styles for the report"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor='#1a237e',
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor='#283593',
            spaceAfter=12,
            spaceBefore=12
        ))
    
    def generate_pdf(self, report_content, output_path='reports/security_report.pdf'):
        """Generate PDF from markdown report"""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        story = []
        
        # Title page
        story.append(Spacer(1, 2*inch))
        title = Paragraph(
            "PENETRATION TESTING REPORT",
            self.styles['CustomTitle']
        )
        story.append(title)
        story.append(Spacer(1, 0.5*inch))
        
        subtitle = Paragraph(
            f"Generated: {datetime.now().strftime('%B %d, %Y')}",
            self.styles['Normal']
        )
        story.append(subtitle)
        story.append(PageBreak())
        
        # Convert markdown to paragraphs
        lines = report_content.split('\n')
        for line in lines:
            if line.startswith('# '):
                story.append(Paragraph(line[2:], self.styles['CustomTitle']))
                story.append(Spacer(1, 12))
            elif line.startswith('## '):
                story.append(Paragraph(line[3:], self.styles['SectionHeading']))
                story.append(Spacer(1, 12))
            elif line.strip():
                story.append(Paragraph(line, self.styles['Normal']))
                story.append(Spacer(1, 6))
        
        doc.build(story)
        return output_path
```

### Step 5: Main Application
Tie everything together.
```python
# src/main.py
#!/usr/bin/env python3
import sys
from pathlib import Path
from report_generator import load_scanner_results
from ai_analyzer import SecurityAnalyzer
from terminal_display import TerminalDisplay
from pdf_generator import PDFReportGenerator

def main():
    # Initialize components
    display = TerminalDisplay()
    analyzer = SecurityAnalyzer()
    pdf_gen = PDFReportGenerator()
    
    # Display header
    display.display_header()
    
    # Step 1: Load scanner results
    display.display_loading("Loading scanner results from teammate")
    try:
        scanner_results = load_scanner_results('scanner_results')
        display.display_success(f"Loaded {len(scanner_results)} scanner output files")
    except Exception as e:
        display.console.print(f"[red]Error loading scanner results: {e}[/red]")
        sys.exit(1)
    
    # Step 2: Analyze with Claude AI
    display.display_loading("Analyzing vulnerabilities with Claude AI")
    try:
        ai_report = analyzer.analyze_scan_results(scanner_results)
        display.display_success("AI analysis complete")
    except Exception as e:
        display.console.print(f"[red]Error during AI analysis: {e}[/red]")
        sys.exit(1)
    
    # Step 3: Display report in terminal
    display.display_report(ai_report)
    
    # Step 4: Save markdown report
    display.display_loading("Saving markdown report")
    Path('reports').mkdir(exist_ok=True)
    with open('reports/security_report.md', 'w') as f:
        f.write(ai_report)
    display.display_success("Markdown report saved to reports/security_report.md")
    
    # Step 5: Generate PDF
    display.display_loading("Generating PDF report")
    try:
        pdf_path = pdf_gen.generate_pdf(ai_report)
        display.display_success(f"PDF report saved to {pdf_path}")
    except Exception as e:
        display.console.print(f"[yellow]Warning: PDF generation failed: {e}[/yellow]")
    
    # Final message
    display.console.print("\n[bold green]✓ Report generation complete![/bold green]\n")

if __name__ == "__main__":
    main()
```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Create a `.env` file:
```
ANTHROPIC_API_KEY=your_api_key_here
```

### 3. Prepare Input Directory
```bash
mkdir -p scanner_results
mkdir -p reports
```

### 4. Get Scanner Results from Teammate
Your teammate (Part 1) should place their tool outputs in `scanner_results/`:
- `nmap_results.md`
- `nikto_results.md`
- `sqlmap_results.md`
- Any other scanner outputs

### 5. Run the Report Generator
```bash
python src/main.py
```

## Expected Output

### Terminal Display:
```
╔═══════════════════════════════════════════════════════════╗
║     PENETRATION TESTING REPORT GENERATOR                  ║
║     AI-Powered Security Assessment Tool                   ║
╚═══════════════════════════════════════════════════════════╝

⚙️  Loading scanner results from teammate...
✓ Loaded 3 scanner output files

⚙️  Analyzing vulnerabilities with Claude AI...
✓ AI analysis complete

╔════════════════════════════════════════╗
║   SECURITY ASSESSMENT REPORT           ║
╚════════════════════════════════════════╝

# EXECUTIVE SUMMARY
...

# VULNERABILITY SUMMARY
...

# DETAILED FINDINGS
...

# REMEDIATION RECOMMENDATIONS
...

✓ Markdown report saved to reports/security_report.md
✓ PDF report saved to reports/security_report.pdf

✓ Report generation complete!
```

## Testing Without Teammate's Output

Create sample files in `scanner_results/`:

**nmap_results.md:**
```markdown
# Nmap Scan Results
Target: 192.168.1.100

## Open Ports
- 22/tcp open ssh OpenSSH 7.4
- 80/tcp open http Apache 2.4.6
- 443/tcp open https Apache 2.4.6
- 3306/tcp open mysql MySQL 5.7.33
```

**nikto_results.md:**
```markdown
# Nikto Web Scan Results
Target: http://192.168.1.100

## Vulnerabilities Found
- Server leaks inodes via ETags
- Apache/2.4.6 appears to be outdated
- Missing security headers (X-Frame-Options, X-Content-Type-Options)
- Directory indexing enabled on /backup/
```

Then run: `python src/main.py`

## Demo Video Script

1. **Show terminal** - Run the command
2. **Real-time processing** - Show it loading files and calling Claude
3. **Beautiful terminal output** - Formatted report with colors
4. **Show generated files** - Markdown and PDF in reports/ folder
5. **Open PDF** - Professional-looking report

## For Your Presentation

**Your contribution:**
- AI-powered vulnerability analysis using Claude
- Professional report generation
- Clean terminal interface
- PDF export capability
- Integration with Part 1's scanner outputs

**Key talking points:**
- "Takes raw scanner output and transforms it into actionable intelligence"
- "Uses Claude AI to prioritize vulnerabilities by business impact"
- "Generates professional reports suitable for executive stakeholders"
- "Automates the most time-consuming part of penetration testing"

## Deliverables Checklist

- [ ] Working Python application that processes .md files
- [ ] Claude AI integration for vulnerability analysis
- [ ] Terminal-based report display with rich formatting
- [ ] PDF report generation
- [ ] 3-5 minute demo video
- [ ] PowerPoint slides (your portion: AI analysis, reporting, architecture)
- [ ] IEEE report contribution (methodology, implementation, results)

---

This is your complete implementation guide. Everything is designed to work independently of your teammate's implementation - you just need their .md output files!