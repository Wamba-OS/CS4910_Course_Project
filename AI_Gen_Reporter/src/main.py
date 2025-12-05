#!/usr/bin/env python3
# src/main.py
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
    # Get the absolute path relative to the script location
    script_dir = Path(__file__).parent.parent  # Go up to project root
    reports_dir = script_dir / 'reports'
    reports_dir.mkdir(exist_ok=True)
    report_file = reports_dir / 'security_report.md'
    with open(report_file, 'w') as f:
        f.write(ai_report)
    display.display_success(f"Markdown report saved to {report_file}")

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
