from collections import Counter
from statistics import mean

from .models import Summary


class MetricsBuilder:

    def __init__(self, findings):

        self.findings = findings

    def build(self):

        total = len(self.findings)

        successful = sum(
            1 for f in self.findings if f.attack_success
        )

        blocked = total - successful

        success_rate = (
            successful / total * 100
            if total else 0
        )

        risk_scores = [
            f.risk_score
            for f in self.findings
            if isinstance(f.risk_score, (int, float))
        ]

        avg_risk = (
            round(mean(risk_scores), 2)
            if risk_scores else 0
        )

        execution_times = [
            f.execution_time
            for f in self.findings
            if isinstance(f.execution_time, (int, float))
        ]

        avg_time = (
            round(mean(execution_times), 2)
            if execution_times else 0
        )

        severity = Counter(
            f.severity for f in self.findings
        )

        strategy = Counter(
            f.attack_strategy
            for f in self.findings
            if f.attack_strategy
        )

        security_score = max(
            0,
            100 - (success_rate * 1.5 + avg_risk * 10)
        )

        return Summary(

            total_tests=total,

            successful_attacks=successful,

            blocked_attacks=blocked,

            attack_success_rate=round(success_rate, 2),

            average_risk=avg_risk,

            average_execution_time=avg_time,

            security_score=round(security_score, 1),

            severity_distribution=dict(severity),

            strategy_distribution=dict(strategy),
        )