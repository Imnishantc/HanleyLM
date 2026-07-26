from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor


class ColorTheme:
    NAVY = HexColor("#001F3F")
    DARK_BLUE = HexColor("#003D7A")
    BLUE = HexColor("#0066CC")
    LIGHT_BLUE = HexColor("#EAF3FF")

    GREEN = HexColor("#28A745")
    ORANGE = HexColor("#FFA500")
    RED = HexColor("#DC3545")

    LIGHT_GRAY = HexColor("#F5F5F5")
    GRAY = HexColor("#6C757D")

    WHITE = colors.white
    BLACK = colors.black


def build_styles():

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            fontName="Helvetica-Bold",
            fontSize=30,
            alignment=TA_CENTER,
            textColor=ColorTheme.NAVY,
            spaceAfter=20,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Heading",
            fontName="Helvetica-Bold",
            fontSize=18,
            textColor=ColorTheme.NAVY,
            spaceAfter=10,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SubHeading",
            fontName="Helvetica-Bold",
            fontSize=13,
            textColor=ColorTheme.DARK_BLUE,
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Body",
            fontName="Helvetica",
            fontSize=10,
            leading=16,
            alignment=TA_LEFT,
            textColor=ColorTheme.BLACK,
        )
    )

    return styles