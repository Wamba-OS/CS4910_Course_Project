#!/usr/bin/env python3
# src/main.py
import sys
from pathlib import Path
from report_generator import load_scanner_results
from ai_analyzer import SecurityAnalyzer
from terminal_display import TerminalDisplay
from pdf_generator import PDFReportGenerator
from run_scanners import run_all_scanners

def main():
    # Initialize components
    display = TerminalDisplay()
    analyzer = SecurityAnalyzer()
    pdf_gen = PDFReportGenerator()

    # Display header
    display.display_header()

    # Step 0: Get target from user or command line
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        display.console.print("[yellow]No target specified. Please provide a target to scan.[/yellow]")
        target = display.console.input("[bold cyan]Enter target (IP/domain/URL): [/bold cyan]")
        if not target:
            display.console.print("[red]No target provided. Exiting.[/red]")
            sys.exit(1)

    # Step 1: Run all security scanners
    display.display_loading(f"Running security scanners against {target}")
    try:
        scan_results = run_all_scanners(target, output_dir='scanner_results')
        if len(scan_results['reports']) == 0:
            display.console.print("[red]All scans failed! Cannot proceed without scan data.[/red]")
            sys.exit(1)
        display.display_success(f"Completed {len(scan_results['reports'])} scans successfully")
    except Exception as e:
        display.console.print(f"[red]Error running scanners: {e}[/red]")
        sys.exit(1)

    # Step 2: Load scanner results
    display.display_loading("Loading scanner results")
    try:
        scanner_results = load_scanner_results('scanner_results')
        display.display_success(f"Loaded {len(scanner_results)} scanner output files")
    except Exception as e:
        display.console.print(f"[red]Error loading scanner results: {e}[/red]")
        sys.exit(1)

    # Step 3: Analyze with Claude AI
    display.display_loading("Analyzing vulnerabilities with Claude AI")
    try:
        ai_report = analyzer.analyze_scan_results(scanner_results)
        display.display_success("AI analysis complete")
    except Exception as e:
        display.console.print(f"[red]Error during AI analysis: {e}[/red]")
        sys.exit(1)

    # Step 4: Display report in terminal
    display.display_report(ai_report)

    # Step 5: Save markdown report
    display.display_loading("Saving markdown report")
    # Get the absolute path relative to the script location
    script_dir = Path(__file__).parent.parent  # Go up to project root
    reports_dir = script_dir / 'reports'
    reports_dir.mkdir(exist_ok=True)
    report_file = reports_dir / 'security_report.md'
    with open(report_file, 'w') as f:
        f.write(ai_report)
    display.display_success(f"Markdown report saved to {report_file}")

    # Step 6: Generate PDF
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
