import os

import matplotlib.pyplot as plt

from reportlab.platypus import Image


class ChartBuilder:

    def __init__(self, summary):

        self.summary = summary

        self.chart_dir = "reports/charts"

        os.makedirs(self.chart_dir, exist_ok=True)

    # ---------------------------------------------
    # Attack Success Pie Chart
    # ---------------------------------------------

    def attack_success_chart(self):

        labels = ["Blocked", "Successful"]

        values = [
            self.summary.blocked_attacks,
            self.summary.successful_attacks,
        ]

        plt.figure(figsize=(5, 5))

        plt.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
        )

        plt.title("Attack Success Distribution")

        path = os.path.join(
            self.chart_dir,
            "attack_success.png"
        )

        plt.savefig(path, dpi=300, bbox_inches="tight")

        plt.close()

        return path

    # ---------------------------------------------
    # Severity Distribution
    # ---------------------------------------------

    def severity_chart(self):

        severity = self.summary.severity_distribution

        labels = list(severity.keys())

        values = list(severity.values())

        plt.figure(figsize=(6, 4))

        plt.bar(labels, values)

        plt.title("Severity Distribution")

        plt.xlabel("Severity")

        plt.ylabel("Count")

        path = os.path.join(
            self.chart_dir,
            "severity_distribution.png"
        )

        plt.savefig(path, dpi=300, bbox_inches="tight")

        plt.close()

        return path

    # ---------------------------------------------
    # Attack Strategy Distribution
    # ---------------------------------------------

    def strategy_chart(self):

        strategy = self.summary.strategy_distribution

        labels = list(strategy.keys())

        values = list(strategy.values())

        plt.figure(figsize=(8, 4))

        plt.barh(labels, values)

        plt.title("Attack Strategy Distribution")

        path = os.path.join(
            self.chart_dir,
            "strategy_distribution.png"
        )

        plt.savefig(path, dpi=300, bbox_inches="tight")

        plt.close()

        return path

    # ---------------------------------------------
    # Generate All Charts
    # ---------------------------------------------

    def generate(self):

        return {

            "attack": self.attack_success_chart(),

            "severity": self.severity_chart(),

            "strategy": self.strategy_chart()

        }


# -------------------------------------------------
# Helper
# -------------------------------------------------

def chart_image(path, width=420, height=240):

    return Image(
        path,
        width=width,
        height=height
    )