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
