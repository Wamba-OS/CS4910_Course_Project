# Penetration Testing Report Generator

AI-Powered Security Assessment Tool that transforms raw penetration testing scan results into professional security reports using Claude AI.

## Overview

This tool takes scan results from penetration testing tools (Nmap, Nikto, SQLMap, etc.) and generates comprehensive security assessment reports with:
- Executive summaries
- Vulnerability analysis
- Risk assessments
- Remediation recommendations
- Professional PDF reports

## Project Structure

```
AI_Gen_Reporter/
├── agent.md                    # Implementation guide
├── scanner_results/            # Input: Tool outputs from scanners
│   ├── nmap_results.md
│   ├── nikto_results.md
│   └── sqlmap_results.md
├── reports/                    # Output: Generated reports
│   ├── security_report.md
│   └── security_report.pdf
├── src/
│   ├── report_generator.py    # Scanner result loader
│   ├── ai_analyzer.py         # Claude API integration
│   ├── pdf_generator.py       # PDF creation
│   ├── terminal_display.py    # Terminal UI
│   └── main.py                # Main application
├── requirements.txt
├── .env                       # API key configuration
└── README.md
```

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Edit the `.env` file and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

### 3. Prepare Scanner Results

Place your scanner output files (as .md files) in the `scanner_results/` directory.

## Usage

### Running the Report Generator

```bash
cd AI_Gen_Reporter
python src/main.py
```

### Expected Output

The application will:
1. Load all .md files from `scanner_results/`
2. Send them to Claude AI for analysis
3. Display a formatted report in the terminal
4. Save a markdown report to `reports/security_report.md`
5. Generate a PDF report at `reports/security_report.pdf`

## Sample Terminal Output

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

[AI-generated report content displayed here]

✓ Markdown report saved to reports/security_report.md
✓ PDF report saved to reports/security_report.pdf

✓ Report generation complete!
```

## Features

- **AI-Powered Analysis**: Uses Claude Sonnet to analyze vulnerabilities and provide expert insights
- **Professional Formatting**: Clean terminal display with Rich library
- **Multiple Output Formats**: Generates both Markdown and PDF reports
- **Comprehensive Reports**: Includes executive summaries, detailed findings, and remediation guidance
- **Easy Integration**: Works with any scanner tool that outputs to .md files

## Testing

Sample scanner results are included in `scanner_results/` for testing purposes. Run the application to see how it processes and analyzes the sample data.

## Requirements

- Python 3.8+
- Anthropic API key
- Dependencies listed in requirements.txt

## License

Educational project for CS4910 Penetration Testing course.
