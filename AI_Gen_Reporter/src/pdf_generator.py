# src/pdf_generator.py
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from pathlib import Path
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
        # Get the absolute path relative to the script location
        script_dir = Path(__file__).parent.parent  # Go up to project root

        # If output_path is relative, make it relative to project root
        if not Path(output_path).is_absolute():
            output_path = script_dir / output_path

        # Ensure the directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        doc = SimpleDocTemplate(
            str(output_path),
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
