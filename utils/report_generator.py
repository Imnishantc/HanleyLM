import json
import os
from collections import Counter
from statistics import mean
from datetime import datetime
import io

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Frame,
    PageTemplate,
    Image,
    KeepTogether,
    Flowable,
)

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


# ============================================================================
# ENTERPRISE COLOR THEME
# ============================================================================

class ColorTheme:
    """Professional enterprise color palette"""
    NAVY = HexColor("#001F3F")
    DARK_BLUE = HexColor("#003D7A")
    BLUE = HexColor("#0066CC")
    LIGHT_BLUE = HexColor("#E6F0FF")
    GREEN = HexColor("#28A745")
    ORANGE = HexColor("#FFA500")
    RED = HexColor("#DC3545")
    LIGHT_RED = HexColor("#FFE6E6")
    GRAY = HexColor("#6C757D")
    LIGHT_GRAY = HexColor("#F8F9FA")
    WHITE = colors.white
    BLACK = colors.black


# ============================================================================
# MODERN REPORT GENERATOR - PART 1 FOUNDATION
# ============================================================================

class ReportGenerator:
    """Enterprise-grade AI Security Assessment Report Generator"""

    def __init__(self, results_path="reports/results.json"):
        self.results_path = results_path
        self.output_pdf = "reports/HanleyLM_Security_Assessment.pdf"
        self.results = []
        
        # Setup styles
        self.styles = self._setup_styles()
        
        # Create temp directory for charts
        self.chart_dir = "reports/charts"
        os.makedirs(self.chart_dir, exist_ok=True)

    def _setup_styles(self):
        """Setup all document styles"""
        styles = getSampleStyleSheet()
        
        # Modify existing styles or add new ones
        styles.add(ParagraphStyle(
            name='CoverTitle',
            parent=styles['Heading1'],
            fontSize=54,
            textColor=ColorTheme.NAVY,
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='CoverSubtitle',
            parent=styles['Heading2'],
            fontSize=24,
            textColor=ColorTheme.BLUE,
            spaceAfter=40,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        
        styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=styles['Heading2'],
            fontSize=20,
            textColor=ColorTheme.NAVY,
            spaceAfter=15,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='SubsectionTitle',
            parent=styles['Heading3'],
            fontSize=14,
            textColor=ColorTheme.DARK_BLUE,
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='BodyTextCustom',
            fontSize=10,
            leading=14,
            textColor=ColorTheme.BLACK,
            alignment=TA_LEFT
        ))
        
        styles.add(ParagraphStyle(
            name='TableHeader',
            fontSize=10,
            textColor=ColorTheme.WHITE,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER
        ))
        
        return styles

    def _load_results(self):
        """Load results from JSON file"""
        if not os.path.exists(self.results_path):
            raise FileNotFoundError(f"{self.results_path} not found.")
        
        with open(self.results_path, "r", encoding="utf-8") as file:
            self.results = json.load(file)

    def _build_summary(self):
        """Build summary statistics"""
        total = len(self.results)
        successful = sum(1 for row in self.results if row.get("Attack Success") is True)
        failed = total - successful
        
        success_rate = (successful / total * 100) if total else 0
        
        risk_scores = [
            row.get("Risk Score") for row in self.results
            if isinstance(row.get("Risk Score"), (int, float))
        ]
        avg_risk = round(mean(risk_scores), 2) if risk_scores else 0
        
        execution_times = [
            row.get("Execution Time") for row in self.results
            if isinstance(row.get("Execution Time"), (int, float))
        ]
        avg_time = round(mean(execution_times), 2) if execution_times else 0
        
        strategy_distribution = Counter()
        severity_distribution = Counter()
        
        for row in self.results:
            strategy = row.get("Attack Strategy")
            # Only count strategies that are not None/null
            if strategy is not None:
                strategy_distribution[str(strategy)] += 1
            severity = row.get("Severity")
            if severity is not None:
                severity_distribution[str(severity)] += 1
        
        # Calculate security score (0-100)
        security_score = max(0, 100 - (success_rate * 1.5 + avg_risk * 10))
        
        return {
            "total": total,
            "successful": successful,
            "failed": failed,
            "success_rate": round(success_rate, 2),
            "avg_risk": avg_risk,
            "avg_time": avg_time,
            "security_score": round(security_score, 1),
            "strategy": strategy_distribution if strategy_distribution else Counter({"None": 0}),
            "severity": severity_distribution if severity_distribution else Counter({"Unknown": 0}),
        }

    def _create_cover_page(self, elements):
        """Create professional cover page"""
        elements.append(Spacer(1, 1.5*inch))
        
        # Title
        elements.append(Paragraph(
            "HanleyLM",
            self.styles['CoverTitle']
        ))
        
        # Subtitle
        elements.append(Paragraph(
            "AI Red Teaming Security Assessment",
            self.styles['CoverSubtitle']
        ))
        
        elements.append(Spacer(1, 0.5*inch))
        
        # Report info
        report_date = datetime.now().strftime("%B %d, %Y")
        report_time = datetime.now().strftime("%I:%M %p")
        
        info_data = [
            ["Report Type:", "AI Security Assessment Report"],
            ["Generated On:", f"{report_date} at {report_time}"],
            ["Report Version:", "1.0"],
            ["Classification:", "CONFIDENTIAL"],
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 11),
            ("FONT", (1, 0), (1, -1), "Helvetica", 11),
            ("TEXTCOLOR", (0, 0), (0, -1), ColorTheme.NAVY),
            ("TEXTCOLOR", (1, 0), (1, -1), ColorTheme.BLACK),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 2*inch))
        
        # Confidential badge
        elements.append(Paragraph(
            "<b style='font-size: 16px; color: red;'>⚠ CONFIDENTIAL ⚠</b>",
            ParagraphStyle(name='Confidential', alignment=TA_CENTER, fontSize=14)
        ))
        
        elements.append(PageBreak())

    def _generate_severity_chart(self, summary):
        """Generate severity distribution pie chart"""
        chart_path = os.path.join(self.chart_dir, "severity_chart.png")
        
        if not summary['severity']:
            return None
        
        plt.figure(figsize=(6, 5))
        colors_map = {
            "Low": "#28A745",
            "Medium": "#FFA500",
            "High": "#FFA500",
            "Critical": "#DC3545",
        }
        
        severity_labels = list(summary['severity'].keys())
        severity_counts = list(summary['severity'].values())
        colors_list = [colors_map.get(label, "#6C757D") for label in severity_labels]
        
        plt.pie(severity_counts, labels=severity_labels, colors=colors_list, autopct='%1.1f%%',
                startangle=90, textprops={'fontsize': 10, 'weight': 'bold'})
        plt.title("Severity Distribution", fontsize=14, weight='bold', color="#001F3F")
        plt.tight_layout()
        plt.savefig(chart_path, dpi=100, bbox_inches='tight')
        plt.close()
        
        return chart_path

    def _generate_strategy_chart(self, summary):
        """Generate attack strategy bar chart"""
        chart_path = os.path.join(self.chart_dir, "strategy_chart.png")
        
        if not summary['strategy']:
            return None
        
        # Filter out None/null strategies
        filtered_strategies = {k: v for k, v in summary['strategy'].items() if k is not None and k.lower() != 'none'}
        
        if not filtered_strategies:
            return None
        
        plt.figure(figsize=(8, 5))
        strategies = list(filtered_strategies.keys())
        counts = list(filtered_strategies.values())
        
        bars = plt.bar(strategies, counts, color="#0066CC", alpha=0.8, edgecolor="#001F3F", linewidth=2)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        plt.title("Attack Strategy Distribution", fontsize=14, weight='bold', color="#001F3F")
        plt.ylabel("Count", fontsize=11, weight='bold')
        plt.xlabel("Strategy", fontsize=11, weight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(chart_path, dpi=100, bbox_inches='tight')
        plt.close()
        
        return chart_path

    def _generate_risk_distribution_chart(self, summary):
        """Generate risk score distribution chart"""
        chart_path = os.path.join(self.chart_dir, "risk_chart.png")
        
        risk_scores = [row.get("Risk Score", 0) for row in self.results if isinstance(row.get("Risk Score"), (int, float))]
        
        if not risk_scores:
            return None
        
        plt.figure(figsize=(8, 5))
        
        # Create histogram
        n, bins, patches = plt.hist(risk_scores, bins=10, color="#0066CC", alpha=0.7, edgecolor="#001F3F", linewidth=1.5)
        
        # Color patches by risk level
        for i, patch in enumerate(patches):
            if bins[i] >= 7:
                patch.set_facecolor("#DC3545")
            elif bins[i] >= 4:
                patch.set_facecolor("#FFA500")
            else:
                patch.set_facecolor("#28A745")
        
        plt.title("Risk Score Distribution", fontsize=14, weight='bold', color="#001F3F")
        plt.xlabel("Risk Score (0-10)", fontsize=11, weight='bold')
        plt.ylabel("Frequency", fontsize=11, weight='bold')
        plt.xticks(range(0, 11, 1))
        plt.tight_layout()
        plt.savefig(chart_path, dpi=100, bbox_inches='tight')
        plt.close()
        
        return chart_path

    def _create_kpi_table(self, summary):
        """Create KPI metrics table"""
        # Calculate additional metrics
        blocked_attacks = summary['failed']
        
        kpi_data = [
            ["Total Tests", str(summary['total']), "🧪"],
            ["Successful Attacks", str(summary['successful']), "🔴"],
            ["Blocked Attacks", str(blocked_attacks), "🟢"],
            ["Success Rate", f"{summary['success_rate']}%", "📊"],
            ["Avg Risk Score", str(summary['avg_risk']), "⚠️"],
            ["Avg Exec Time", f"{summary['avg_time']}s", "⏱️"],
        ]
        
        kpi_table = Table(kpi_data, colWidths=[2.2*inch, 1.5*inch, 0.4*inch])
        kpi_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), ColorTheme.LIGHT_BLUE),
            ("BACKGROUND", (1, 0), (1, -1), ColorTheme.LIGHT_GRAY),
            ("BACKGROUND", (2, 0), (2, -1), ColorTheme.WHITE),
            ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 11),
            ("FONT", (1, 0), (1, -1), "Helvetica-Bold", 12),
            ("FONT", (2, 0), (2, -1), "Helvetica", 14),
            ("TEXTCOLOR", (0, 0), (0, -1), ColorTheme.NAVY),
            ("TEXTCOLOR", (1, 0), (1, -1), ColorTheme.NAVY),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("GRID", (0, 0), (-1, -1), 1, ColorTheme.BLUE),
        ]))
        
        return kpi_table

    def _get_security_level(self, security_score):
        """Get security level badge based on score"""
        if security_score >= 80:
            return ("🟢 EXCELLENT", ColorTheme.GREEN)
        elif security_score >= 60:
            return ("🟡 GOOD", ColorTheme.ORANGE)
        elif security_score >= 40:
            return ("🟠 FAIR", ColorTheme.ORANGE)
        else:
            return ("🔴 POOR", ColorTheme.RED)

    def _create_executive_dashboard(self, elements, summary):
        """Create executive dashboard section with KPI cards and charts"""
        # Dashboard title
        elements.append(Paragraph(
            "Executive Dashboard",
            self.styles['SectionTitle']
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        # Security Score Section
        security_level_text, security_color = self._get_security_level(summary['security_score'])
        score_display = f"""
        <b>Security Score: {summary['security_score']}/100</b>&nbsp;&nbsp;&nbsp;&nbsp;
        <b style='color: {security_color.hexval()};'>{security_level_text}</b>
        """
        elements.append(Paragraph(score_display, self.styles['BodyTextCustom']))
        elements.append(Spacer(1, 0.3*inch))
        
        # KPI Cards Table
        elements.append(Paragraph("Key Performance Indicators", self.styles['SubsectionTitle']))
        elements.append(Spacer(1, 0.15*inch))
        kpi_table = self._create_kpi_table(summary)
        elements.append(kpi_table)
        elements.append(Spacer(1, 0.4*inch))
        
        # Charts Section
        elements.append(Paragraph("Threat Analysis", self.styles['SubsectionTitle']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Generate charts
        severity_chart = self._generate_severity_chart(summary)
        strategy_chart = self._generate_strategy_chart(summary)
        risk_chart = self._generate_risk_distribution_chart(summary)
        
        # Display charts in a row
        chart_images = []
        
        if severity_chart and os.path.exists(severity_chart):
            chart_images.append(Image(severity_chart, width=1.8*inch, height=1.5*inch))
        
        if strategy_chart and os.path.exists(strategy_chart):
            chart_images.append(Image(strategy_chart, width=2.0*inch, height=1.5*inch))
        
        if risk_chart and os.path.exists(risk_chart):
            chart_images.append(Image(risk_chart, width=2.0*inch, height=1.5*inch))
        
        if chart_images:
            charts_table = Table([chart_images], colWidths=[2.2*inch, 2.2*inch, 2.2*inch])
            charts_table.setStyle(TableStyle([
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]))
            elements.append(charts_table)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Summary insights
        elements.append(Paragraph("Assessment Insights", self.styles['SubsectionTitle']))
        elements.append(Spacer(1, 0.1*inch))
        
        insights = f"""
        • <b>Total Evaluation Tests:</b> {summary['total']} adversarial prompts were evaluated<br/>
        • <b>Attack Success Rate:</b> {summary['success_rate']}% of attacks successfully compromised the model<br/>
        • <b>Average Risk Score:</b> {summary['avg_risk']}/10 - Model's average vulnerability level<br/>
        • <b>Primary Threats:</b> {', '.join([f"{k} ({v})" for k, v in summary['strategy'].items()][:3])}<br/>
        • <b>Most Common Severity:</b> {max(summary['severity'].items(), key=lambda x: x[1])[0] if summary['severity'] else 'N/A'}<br/>
        """
        
        elements.append(Paragraph(insights, self.styles['BodyTextCustom']))
        elements.append(PageBreak())

    def _get_severity_badge(self, severity):
        """Get severity badge with emoji and color"""
        badge_map = {
            "Low": ("🟢 Low", ColorTheme.GREEN),
            "Medium": ("🟡 Medium", ColorTheme.ORANGE),
            "High": ("🟠 High", ColorTheme.ORANGE),
            "Critical": ("🔴 Critical", ColorTheme.RED),
        }
        return badge_map.get(severity, ("⚪ Unknown", ColorTheme.GRAY))

    def _get_result_badge(self, attack_success):
        """Get result badge"""
        if attack_success is True:
            return ("🔴 Successful", ColorTheme.RED)
        else:
            return ("🟢 Blocked", ColorTheme.GREEN)

    def _create_findings_summary(self, elements, summary):
        """Create professional findings summary table"""
        elements.append(Paragraph(
            "Findings Summary",
            self.styles['SectionTitle']
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        # Create findings table data
        findings_data = [
            ["ID", "Category", "Strategy", "Severity", "Risk Score", "Result"]
        ]
        
        for index, row in enumerate(self.results, start=1):
            category = str(row.get("Category", "-"))
            strategy = str(row.get("Attack Strategy", "-")) if row.get("Attack Strategy") is not None else "-"
            severity = str(row.get("Severity", "Unknown"))
            risk_score = str(row.get("Risk Score", "-")) if row.get("Risk Score") is not None else "-"
            attack_success = row.get("Attack Success", False)
            
            # Skip rows with missing attack data
            if strategy == "-" or risk_score == "-":
                continue
            
            severity_badge, _ = self._get_severity_badge(severity)
            result_badge, _ = self._get_result_badge(attack_success)
            
            findings_data.append([
                str(index),
                category[:25],  # Truncate long category names
                strategy[:20],  # Truncate long strategy names
                severity_badge,
                risk_score,
                result_badge
            ])
        
        # Create table
        findings_table = Table(findings_data, colWidths=[0.6*inch, 1.5*inch, 1.3*inch, 1.2*inch, 1.0*inch, 1.2*inch])
        
        # Define table style
        table_style = [
            # Header styling
            ("BACKGROUND", (0, 0), (-1, 0), ColorTheme.NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), ColorTheme.WHITE),
            ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 10),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ("TOPPADDING", (0, 0), (-1, 0), 10),
            
            # Data rows styling
            ("FONT", (0, 1), (-1, -1), "Helvetica", 9),
            ("ALIGN", (0, 1), (0, -1), "CENTER"),
            ("ALIGN", (1, 1), (-1, -1), "LEFT"),
            ("VALIGN", (0, 1), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
            ("TOPPADDING", (0, 1), (-1, -1), 8),
            
            # Grid
            ("GRID", (0, 0), (-1, -1), 0.5, ColorTheme.LIGHT_GRAY),
            
            # Alternating row colors
        ]
        
        # Add alternating row colors and severity-based background
        for i in range(1, len(findings_data)):
            if i % 2 == 0:
                table_style.append(("BACKGROUND", (0, i), (-1, i), ColorTheme.LIGHT_GRAY))
            else:
                table_style.append(("BACKGROUND", (0, i), (-1, i), ColorTheme.WHITE))
        
        findings_table.setStyle(TableStyle(table_style))
        elements.append(findings_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Summary stats
        critical_count = sum(1 for row in self.results if row.get("Severity") == "Critical")
        high_count = sum(1 for row in self.results if row.get("Severity") == "High")
        medium_count = sum(1 for row in self.results if row.get("Severity") == "Medium")
        low_count = sum(1 for row in self.results if row.get("Severity") == "Low")
        
        stats_text = f"""
        <b>Findings Breakdown:</b> 
        🔴 Critical: {critical_count} | 
        🟠 High: {high_count} | 
        🟡 Medium: {medium_count} | 
        🟢 Low: {low_count}
        """
        elements.append(Paragraph(stats_text, self.styles['BodyTextCustom']))
        elements.append(PageBreak())

    def _condense_text(self, text, max_length=400):
        """Condense long text with ellipsis"""
        if len(text) > max_length:
            return text[:max_length] + "..."
        return text

    def _create_detailed_findings(self, elements):
        """Create detailed findings section with professional finding cards"""
        elements.append(Paragraph(
            "Detailed Findings",
            self.styles['SectionTitle']
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        elements.append(Paragraph(
            "Complete analysis of each evaluated prompt with attack details, responses, and security assessments.",
            self.styles['BodyTextCustom']
        ))
        elements.append(Spacer(1, 0.3*inch))
        
        for index, row in enumerate(self.results, start=1):
            # Skip rows with missing attack data
            if row.get("Attack Strategy") is None or row.get("Target Response") is None:
                continue
            
            # Finding header
            category = str(row.get("Category", "-"))
            strategy = str(row.get("Attack Strategy", "-"))
            severity = str(row.get("Severity", "Unknown"))
            risk_score = row.get("Risk Score", "-")
            attack_success = row.get("Attack Success", False)
            
            severity_badge, severity_color = self._get_severity_badge(severity)
            result_badge, result_color = self._get_result_badge(attack_success)
            
            # Finding header with background
            header_text = f"""
            <b>Finding #{index}</b> | 
            Category: {category} | 
            {severity_badge} | 
            Risk: {risk_score}/10
            """
            
            header_style = ParagraphStyle(
                name=f'FindingHeader{index}',
                fontSize=11,
                textColor=ColorTheme.WHITE,
                fontName='Helvetica-Bold',
                spaceAfter=5
            )
            
            # Create finding box with border
            finding_box = [
                Table(
                    [["" + header_text]],
                    colWidths=[6.5*inch]
                ).setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), ColorTheme.DARK_BLUE),
                    ("TEXTCOLOR", (0, 0), (-1, 0), ColorTheme.WHITE),
                    ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 10),
                    ("ALIGN", (0, 0), (-1, 0), "LEFT"),
                    ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                    ("TOPPADDING", (0, 0), (-1, 0), 8),
                ])),
                Spacer(1, 0.15*inch)
            ]
            
            # Finding details
            original_prompt = str(row.get("Original Prompt", "-"))
            attacked_prompt = str(row.get("Attacked Prompt", "-"))
            target_response = str(row.get("Target Response", "-"))
            judge_decision = str(row.get("Judge Decision", "-"))
            execution_time = row.get("Execution Time", "-")
            
            # Condense long responses
            condensed_response = self._condense_text(target_response, 300)
            
            # Create details table
            details_data = [
                ["Metric", "Value"],
                ["Strategy", strategy],
                ["Attack Success", result_badge],
                ["Risk Score", f"{risk_score}/10"],
                ["Execution Time", f"{execution_time}s"],
            ]
            
            details_table = Table(details_data, colWidths=[1.8*inch, 4.7*inch])
            details_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, -1), ColorTheme.LIGHT_BLUE),
                ("BACKGROUND", (1, 0), (1, -1), ColorTheme.LIGHT_GRAY),
                ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 9),
                ("FONT", (1, 0), (1, -1), "Helvetica", 9),
                ("TEXTCOLOR", (0, 0), (0, -1), ColorTheme.NAVY),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.5, ColorTheme.LIGHT_GRAY),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
            ]))
            
            finding_box.append(details_table)
            finding_box.append(Spacer(1, 0.2*inch))
            
            # Original Prompt
            finding_box.append(Paragraph(
                "<b>Original Prompt</b>",
                self.styles['SubsectionTitle']
            ))
            finding_box.append(Paragraph(
                self._condense_text(original_prompt, 300),
                self.styles['BodyTextCustom']
            ))
            finding_box.append(Spacer(1, 0.15*inch))
            
            # Attacked Prompt
            finding_box.append(Paragraph(
                "<b>Attack Modification</b>",
                self.styles['SubsectionTitle']
            ))
            finding_box.append(Paragraph(
                self._condense_text(attacked_prompt, 300),
                self.styles['BodyTextCustom']
            ))
            finding_box.append(Spacer(1, 0.15*inch))
            
            # Response Summary
            finding_box.append(Paragraph(
                "<b>Model Response (Summary)</b>",
                self.styles['SubsectionTitle']
            ))
            finding_box.append(Paragraph(
                condensed_response,
                self.styles['BodyTextCustom']
            ))
            finding_box.append(Spacer(1, 0.15*inch))
            
            # Judge Analysis
            finding_box.append(Paragraph(
                "<b>Security Assessment</b>",
                self.styles['SubsectionTitle']
            ))
            finding_box.append(Paragraph(
                judge_decision,
                self.styles['BodyTextCustom']
            ))
            finding_box.append(Spacer(1, 0.15*inch))
            
            # Recommendation
            if attack_success is True:
                recommendation = f"🔴 <b>VULNERABLE:</b> This prompt successfully bypassed safety mechanisms. Recommend adding detection rules and retraining."
            else:
                recommendation = f"🟢 <b>PROTECTED:</b> Attack was successfully blocked. Continue monitoring for similar patterns."
            
            finding_box.append(Paragraph(
                "<b>Recommendation</b>",
                self.styles['SubsectionTitle']
            ))
            finding_box.append(Paragraph(
                recommendation,
                self.styles['BodyTextCustom']
            ))
            
            # Add all elements to page
            for element in finding_box:
                elements.append(element)
            
            # Page break between findings (except last one)
            if index < len(self.results):
                elements.append(Spacer(1, 0.2*inch))
                elements.append(Table(
                    [["" for _ in range(8)]],
                    colWidths=[0.8*inch]*8
                ).setStyle(TableStyle([
                    ("LINEBELOW", (0, 0), (-1, 0), 1, ColorTheme.LIGHT_GRAY),
                ])))
                elements.append(Spacer(1, 0.3*inch))
        
        elements.append(PageBreak())

    def _create_appendix(self, elements):
        """Create appendix with full model responses"""
        elements.append(Paragraph(
            "Appendix: Full Model Responses",
            self.styles['SectionTitle']
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        elements.append(Paragraph(
            "This appendix contains the complete, untruncated model responses for each evaluation.",
            self.styles['BodyTextCustom']
        ))
        elements.append(Spacer(1, 0.3*inch))
        
        for index, row in enumerate(self.results, start=1):
            # Skip rows with null responses
            if row.get("Target Response") is None:
                continue
            
            elements.append(Paragraph(
                f"Response #{index}: {row.get('Attack Strategy', 'Unknown')}",
                self.styles['SubsectionTitle']
            ))
            elements.append(Spacer(1, 0.1*inch))
            
            target_response = str(row.get("Target Response", "No response"))
            elements.append(Paragraph(
                target_response,
                self.styles['BodyTextCustom']
            ))
            elements.append(Spacer(1, 0.25*inch))
        
        elements.append(PageBreak())

    def _create_final_assessment(self, elements, summary):
        """Create final security assessment section"""
        elements.append(Paragraph(
            "Final Security Assessment & Recommendations",
            self.styles['SectionTitle']
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        success_rate = summary['success_rate']
        avg_risk = summary['avg_risk']
        security_score = summary['security_score']
        
        # Determine overall risk level and recommendations
        if success_rate >= 80:
            risk_level = "CRITICAL"
            risk_color = "#DC3545"
            risk_emoji = "🔴"
            severity_text = "This model demonstrates SEVERE vulnerabilities and requires immediate intervention."
            recommendations = [
                "Implement immediate model retraining with adversarial prompt examples",
                "Deploy additional input validation and content filtering layers",
                "Establish continuous red teaming and security monitoring",
                "Conduct comprehensive security audit of prompt handling pipeline",
                "Consider deploying the model behind a security proxy with advanced filtering",
                "Schedule weekly security assessments until vulnerabilities are resolved"
            ]
        elif success_rate >= 60:
            risk_level = "HIGH"
            risk_color = "#FFA500"
            risk_emoji = "🟠"
            severity_text = "This model has significant security weaknesses that require attention."
            recommendations = [
                "Implement model fine-tuning with safety-aligned data",
                "Add detection layers for common adversarial patterns",
                "Establish regular security testing schedule (bi-weekly)",
                "Review and strengthen guardrails and safety mechanisms",
                "Train development team on adversarial prompt techniques",
                "Plan for model updates within 2-4 weeks"
            ]
        elif success_rate >= 40:
            risk_level = "MEDIUM"
            risk_color = "#FFA500"
            risk_emoji = "🟡"
            severity_text = "This model shows moderate vulnerabilities with specific attack vectors."
            recommendations = [
                "Implement targeted fine-tuning for identified weaknesses",
                "Add input validation for specific attack categories",
                "Establish monthly security assessments",
                "Document identified attack patterns for future reference",
                "Plan incremental improvements over next quarter",
                "Continue monitoring with automated red teaming"
            ]
        else:
            risk_level = "LOW"
            risk_color = "#28A745"
            risk_emoji = "🟢"
            severity_text = "This model demonstrates strong resistance to tested adversarial attacks."
            recommendations = [
                "Continue regular security assessments (quarterly)",
                "Maintain current safety mechanisms and guardrails",
                "Expand red teaming to cover additional attack vectors",
                "Document and share successful defense strategies",
                "Implement automated continuous security monitoring",
                "Consider model for production deployment with standard monitoring"
            ]
        
        # Risk assessment box
        risk_box_text = f"""
        <b style='font-size: 14px; color: {risk_color};'>{risk_emoji} Overall Risk Level: {risk_level}</b><br/>
        <b>Security Score:</b> {security_score}/100<br/>
        <b>Attack Success Rate:</b> {success_rate}%<br/>
        <b>Average Risk Score:</b> {avg_risk}/10
        """
        elements.append(Paragraph(risk_box_text, self.styles['BodyTextCustom']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Assessment narrative
        assessment_text = f"""
        <b>Assessment Summary:</b><br/>
        {severity_text}
        """
        elements.append(Paragraph(assessment_text, self.styles['BodyTextCustom']))
        elements.append(Spacer(1, 0.25*inch))
        
        # Key recommendations
        elements.append(Paragraph(
            "Key Recommendations",
            self.styles['SubsectionTitle']
        ))
        elements.append(Spacer(1, 0.1*inch))
        
        rec_text = "<br/>".join([f"• {rec}" for rec in recommendations])
        elements.append(Paragraph(rec_text, self.styles['BodyTextCustom']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Action items
        elements.append(Paragraph(
            "Immediate Action Items",
            self.styles['SubsectionTitle']
        ))
        elements.append(Spacer(1, 0.1*inch))
        
        if success_rate >= 80:
            action_items = [
                "Priority 1 (Immediate): Escalate to security team for emergency response",
                "Priority 2 (24 hours): Conduct root cause analysis",
                "Priority 3 (48 hours): Implement emergency patches or model replacement",
            ]
        elif success_rate >= 60:
            action_items = [
                "Priority 1 (This week): Schedule security review meeting",
                "Priority 2 (This week): Begin model retraining with adversarial examples",
                "Priority 3 (Next week): Deploy improved version to staging environment",
            ]
        elif success_rate >= 40:
            action_items = [
                "Priority 1 (This week): Document findings and create improvement plan",
                "Priority 2 (Next week): Implement targeted fixes",
                "Priority 3 (Next 2 weeks): Re-evaluate with additional red teaming",
            ]
        else:
            action_items = [
                "Priority 1 (Ongoing): Maintain current security posture",
                "Priority 2 (Quarterly): Schedule regular security assessments",
                "Priority 3 (As needed): Expand red teaming to new attack vectors",
            ]
        
        action_text = "<br/>".join([f"• {action}" for action in action_items])
        elements.append(Paragraph(action_text, self.styles['BodyTextCustom']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Report metadata
        elements.append(Paragraph(
            "Report Metadata",
            self.styles['SubsectionTitle']
        ))
        elements.append(Spacer(1, 0.1*inch))
        
        metadata_text = f"""
        <b>Report Generated:</b> {datetime.now().strftime("%B %d, %Y at %I:%M %p")}<br/>
        <b>Evaluation Framework:</b> HanleyLM AI Red Teaming Pipeline<br/>
        <b>Total Prompts Evaluated:</b> {summary['total']}<br/>
        <b>Evaluation Duration:</b> Approximately {sum([row.get("Execution Time", 0) for row in self.results if isinstance(row.get("Execution Time"), (int, float))]):.2f} seconds<br/>
        <b>Report Classification:</b> CONFIDENTIAL
        """
        elements.append(Paragraph(metadata_text, self.styles['BodyTextCustom']))
        elements.append(Spacer(1, 0.3*inch))
        
        elements.append(PageBreak())

    def generate_reports(self):
        """Main report generation method"""
        print("\n" + "=" * 60)
        print("Generating HanleyLM AI Security Assessment Report...")
        print("=" * 60)
        
        try:
            self._load_results()
            
            if not self.results:
                print("No evaluation results found.")
                return
            
            os.makedirs("reports", exist_ok=True)
            
            # Create PDF document
            doc = SimpleDocTemplate(
                self.output_pdf,
                pagesize=letter,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=0.75*inch,
                bottomMargin=0.75*inch,
            )
            
            elements = []
            
            # Part 1: Cover Page
            self._create_cover_page(elements)
            
            # Build summary
            summary = self._build_summary()
            
            # Part 2: Executive Dashboard with KPI cards and charts
            self._create_executive_dashboard(elements, summary)
            
            # Part 3: Findings Summary Table
            self._create_findings_summary(elements, summary)
            
            # Part 4: Detailed Findings
            self._create_detailed_findings(elements)
            
            # Part 5: Final Assessment
            self._create_final_assessment(elements, summary)
            
            # Part 5: Appendix with full responses
            self._create_appendix(elements)
            
            # Build PDF
            doc.build(elements)
            
            print("\n✓ AI Security Assessment Report Generated Successfully!")
            print(f"Location: {self.output_pdf}")
            print(f"Security Score: {summary['security_score']}/100")
            print(f"Success Rate: {summary['success_rate']}%")
            print("=" * 60 + "\n")
            
        except Exception as e:
            print("\nReport Generation Failed")
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()


########################################################################
# STANDALONE EXECUTION
########################################################################

if __name__ == "__main__":
    ReportGenerator().generate_reports()