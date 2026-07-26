from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Dict, Any


@dataclass
class JudgeResult:
    """
    Represents the evaluation produced by the JudgeAgent.
    """

    attack_success: bool
    risk_score: float
    severity: str
    reasoning: str

    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def __str__(self) -> str:
        return (
            f"\n"
            f"{'=' * 60}\n"
            f"Attack Success : {self.attack_success}\n"
            f"Risk Score     : {self.risk_score}/10\n"
            f"Severity       : {self.severity}\n"
            f"Timestamp      : {self.timestamp}\n"
            f"{'-' * 60}\n"
            f"Reasoning:\n"
            f"{self.reasoning}\n"
            f"{'=' * 60}"
        )