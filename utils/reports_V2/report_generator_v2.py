import json
import os

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate

from .models import Finding
from .metrics import MetricsBuilder
from .styles import build_styles

from .sections import (
    create_cover,
    create_executive_summary,
    create_dashboard,
    create_charts,
    create_findings,
)


def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


class ReportGenerator:

    def __init__(self, results_path="reports/results.json"):

        self.results_path = results_path

        self.output_pdf = "reports/HanleyLM_Security_Assessment.pdf"

        os.makedirs(
            os.path.dirname(self.output_pdf),
            exist_ok=True
        )

        self.results = []

        self.findings = []

        self.summary = None

        self.story = []

        self.styles = build_styles()

    # --------------------------------------------------

    def load_results(self):

        if not os.path.exists(self.results_path):

            raise FileNotFoundError(

                f"{self.results_path} not found."

            )

        with open(

            self.results_path,

            "r",

            encoding="utf-8"

        ) as file:

            self.results = json.load(file)

        if not isinstance(self.results, list):

            raise ValueError(

                "results.json should contain a list."

            )

    # --------------------------------------------------

    def build_findings(self):

        self.findings.clear()

        for row in self.results:

            finding = Finding(

                id=row.get("No", 0),

                category=row.get("Category", "-"),

                original_prompt=row.get(
                    "Original Prompt",
                    "-"
                ),

                attack_strategy=row.get(
                    "Attack Strategy",
                    "-"
                ),

                attacked_prompt=row.get(
                    "Attacked Prompt",
                    "-"
                ),

                target_response=row.get(
                    "Target Response",
                    "-"
                ),

                attack_success=row.get(
                    "Attack Success",
                    False
                ),

                risk_score=safe_float(
                    row.get("Risk Score")
                ),

                severity=row.get(
                    "Severity",
                    "Low"
                ),

                judge_decision=row.get(
                    "Judge Decision",
                    "-"
                ),

                execution_time=safe_float(
                    row.get("Execution Time")
                ),

                timestamp=row.get(
                    "Timestamp",
                    "-"
                )

            )

            self.findings.append(finding)

    # --------------------------------------------------
    # Build Summary
    # --------------------------------------------------

    def build_summary(self):

        self.summary = MetricsBuilder(

            self.findings

        ).build()

    # --------------------------------------------------
    # Build Report Story
    # --------------------------------------------------

    def build_story(self):

        self.story.clear()

        if self.summary is None:

            raise RuntimeError(

                "Summary has not been generated."

            )

        # Cover Page
        create_cover(

            self.story,

            self.styles,

            self.summary

        )

        # Executive Summary
        create_executive_summary(

            self.story,

            self.styles,

            self.summary

        )

        # Dashboard
        create_dashboard(

            self.story,

            self.styles,

            self.summary

        )

        # Charts
        create_charts(

            self.story,

            self.styles,

            self.summary

        )

        # Findings
        create_findings(

            self.story,

            self.styles,

            self.findings

        )

    # --------------------------------------------------
    # Export PDF
    # --------------------------------------------------

    def export_pdf(self):

        if not self.story:

            raise RuntimeError(

                "Nothing to export."

            )

        document = SimpleDocTemplate(

            self.output_pdf,

            pagesize=A4,

            rightMargin=30,

            leftMargin=30,

            topMargin=35,

            bottomMargin=35

        )

        document.build(

            self.story

        )
    # --------------------------------------------------
    # Generate Complete Report
    # --------------------------------------------------

    def generate_reports(self):

        print("=" * 60)
        print(" HanleyLM Report Generator V2")
        print("=" * 60)

        try:

            print("[1/5] Loading results...")
            self.load_results()
            print(f"✓ Loaded {len(self.results)} test cases")

            print("[2/5] Building findings...")
            self.build_findings()
            print(f"✓ Created {len(self.findings)} findings")

            print("[3/5] Computing metrics...")
            self.build_summary()
            print("✓ Metrics computed")

            print("[4/5] Building report...")
            self.build_story()
            print(f"✓ Story contains {len(self.story)} elements")

            print("[5/5] Exporting PDF...")
            self.export_pdf()

            print("\n" + "=" * 60)
            print("✓ Report Generated Successfully")
            print(f"📄 Saved to : {self.output_pdf}")
            print("=" * 60)

        except Exception as e:

            print("\n" + "=" * 60)
            print("✗ Report Generation Failed")
            print("=" * 60)

            raise e