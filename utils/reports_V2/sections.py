from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether
)

from reportlab.lib import colors
from reportlab.lib.units import inch

from .styles import ColorTheme
from .charts import ChartBuilder, chart_image

def create_cover(story, styles, summary):

    story.append(Spacer(1, 1.2 * inch))

    story.append(
        Paragraph(
            "HanleyLM",
            styles["CoverTitle"]
        )
    )

    story.append(
        Paragraph(
            "AI Red Team Security Assessment Report",
            styles["Heading"]
        )
    )

    story.append(
        Spacer(1, 0.4 * inch)
    )

    info = [

        ["Assessment", "AI Red Team Evaluation"],

        ["Framework", "HanleyLM"],

        ["Total Test Cases", str(summary.total_tests)],

        ["Security Score", f"{summary.security_score:.1f}/100"],

        ["Attack Success Rate",
         f"{summary.attack_success_rate:.2f}%"]

    ]

    table = Table(
        info,
        colWidths=[180, 250]
    )

    table.setStyle(

        TableStyle([

            ("GRID",(0,0),(-1,-1),0.5,colors.grey),

            ("BACKGROUND",(0,0),(0,-1),
             ColorTheme.LIGHT_BLUE),

            ("BOTTOMPADDING",(0,0),(-1,-1),8),

            ("FONTNAME",(0,0),(-1,-1),
             "Helvetica")

        ])

    )

    story.append(table)

    story.append(PageBreak())

def create_executive_summary(
    story,
    styles,
    summary
):

    story.append(

        Paragraph(
            "Executive Summary",
            styles["Heading"]
        )

    )

    text = f"""

    This report summarizes the AI Red Team assessment
    conducted using HanleyLM.

    <br/><br/>

    Total Test Cases :
    <b>{summary.total_tests}</b>

    <br/><br/>

    Successful Attacks :
    <b>{summary.successful_attacks}</b>

    <br/><br/>

    Blocked Attacks :
    <b>{summary.blocked_attacks}</b>

    <br/><br/>

    Average Risk Score :
    <b>{summary.average_risk:.2f}</b>

    <br/><br/>

    Security Score :
    <b>{summary.security_score:.1f}/100</b>

    """

    story.append(

        Paragraph(

            text,

            styles["Body"]

        )

    )

    story.append(
        Spacer(1,20)
    )

def create_dashboard(
    story,
    styles,
    summary
):

    story.append(

        Paragraph(
            "Assessment Dashboard",
            styles["Heading"]
        )

    )

    data = [

        ["Metric","Value"],

        ["Total Tests",
         summary.total_tests],

        ["Successful",
         summary.successful_attacks],

        ["Blocked",
         summary.blocked_attacks],

        ["Attack Success Rate",
         f"{summary.attack_success_rate:.2f}%"],

        ["Average Risk",
         f"{summary.average_risk:.2f}"],

        ["Security Score",
         f"{summary.security_score:.1f}/100"]

    ]

    table = Table(
        data,
        colWidths=[220,140]
    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND",
             (0,0),(-1,0),
             ColorTheme.NAVY),

            ("TEXTCOLOR",
             (0,0),(-1,0),
             colors.white),

            ("GRID",
             (0,0),(-1,-1),
             0.5,
             colors.grey),

            ("BACKGROUND",
             (0,1),(0,-1),
             ColorTheme.LIGHT_BLUE),

            ("BOTTOMPADDING",
             (0,0),(-1,-1),
             8)

        ])

    )

    story.append(table)

    story.append(
        Spacer(1,20)
    )

def create_charts(
    story,
    styles,
    summary
):

    builder = ChartBuilder(summary)

    charts = builder.generate()

    story.append(

        Paragraph(

            "Assessment Charts",

            styles["Heading"]

        )

    )

    story.append(

        chart_image(
            charts["attack"]
        )

    )

    story.append(
        Spacer(1,15)
    )

    story.append(

        chart_image(
            charts["severity"]
        )

    )

    story.append(
        Spacer(1,15)
    )

    story.append(

        chart_image(
            charts["strategy"]
        )

    )

    story.append(PageBreak())


def severity_color(severity):

    severity = str(severity).lower()

    if severity == "critical":
        return colors.red

    if severity == "high":
        return colors.orange

    if severity == "medium":
        return colors.gold

    return colors.green

def finding_card(
    styles,
    finding
):

    severity = finding.severity or "Unknown"

    color = severity_color(severity)

    title = Table(

        [[

            Paragraph(
                f"<b>Finding #{finding.id}</b>",
                styles["SubHeading"]
            ),

            Paragraph(
                f"<font color='{color.hexval()}'><b>{severity}</b></font>",
                styles["SubHeading"]
            )

        ]],

        colWidths=[320,120]

    )

    title.setStyle(

        TableStyle([

            ("BACKGROUND",
             (0,0),
             (-1,-1),
             ColorTheme.LIGHT_BLUE),

            ("BOX",
             (0,0),
             (-1,-1),
             0.5,
             colors.grey),

            ("BOTTOMPADDING",
             (0,0),
             (-1,-1),
             8)

        ])

    )

    info = [

        ["Category", finding.category],

        ["Attack Strategy", finding.attack_strategy],

        ["Risk Score", finding.risk_score],

        ["Judge Decision", finding.judge_decision],

        ["Execution Time",
         f"{finding.execution_time:.2f}s"]

    ]

    table = Table(

        info,

        colWidths=[140,300]

    )

    table.setStyle(

        TableStyle([

            ("GRID",
             (0,0),
             (-1,-1),
             0.25,
             colors.grey),

            ("BACKGROUND",
             (0,0),
             (0,-1),
             ColorTheme.LIGHT_BLUE),

            ("BOTTOMPADDING",
             (0,0),
             (-1,-1),
             6)

        ])

    )

    flowables = [

        title,

        Spacer(1,10),

        table,

        Spacer(1,10),

        Paragraph(
            "<b>Original Prompt</b>",
            styles["SubHeading"]
        ),

        Paragraph(
            str(finding.original_prompt),
            styles["Body"]
        ),

        Spacer(1,8),

        Paragraph(
            "<b>Adversarial Prompt</b>",
            styles["SubHeading"]
        ),

        Paragraph(
            str(finding.attacked_prompt),
            styles["Body"]
        ),

        Spacer(1,8),

        Paragraph(
            "<b>Target Response</b>",
            styles["SubHeading"]
        ),

        Paragraph(
            str(finding.target_response),
            styles["Body"]
        ),

        Spacer(1,15)

    ]

    return KeepTogether(flowables)

def create_findings(
    story,
    styles,
    findings
):

    story.append(

        Paragraph(

            "Detailed Findings",

            styles["Heading"]

        )

    )

    story.append(

        Spacer(1,20)

    )

    for finding in findings:

        story.append(

            finding_card(

                styles,

                finding

            )

        )

        story.append(

            Spacer(1,20)

        )

        story.append(

            PageBreak()

        )

