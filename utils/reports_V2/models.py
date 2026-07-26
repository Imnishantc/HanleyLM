from dataclasses import dataclass


@dataclass
class Finding:

    id: int

    category: str

    original_prompt: str

    attack_strategy: str

    attacked_prompt: str

    target_response: str

    attack_success: bool

    risk_score: float

    severity: str

    judge_decision: str

    execution_time: float

    timestamp: str


@dataclass
class Summary:

    total_tests: int

    successful_attacks: int

    blocked_attacks: int

    attack_success_rate: float

    average_risk: float

    average_execution_time: float

    security_score: float

    severity_distribution: dict

    strategy_distribution: dict