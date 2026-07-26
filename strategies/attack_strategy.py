from enum import Enum


class AttackStrategy(Enum):
    """
    Supported attack strategies for adversarial prompt generation.
    """

    ROLEPLAY = "roleplay"
    PERSONA = "persona"
    ACADEMIC = "academic"
    RESEARCH = "research"
    FICTION = "fiction"
    STYLE_TRANSFER = "style_transfer"
    CONSTRAINT = "constraint"
    FEWSHOT = "fewshot"
    TRANSLATION = "translation"
    PROMPT_INJECTION = "prompt_injection"
    DAN = "dan"
    DEVELOPER_MODE = "developer_mode"
    ROLE_CONFUSION = "role_confusion"
    GOAL_HIJACKING = "goal_hijacking"
    SYSTEM_PROMPT_EXTRACTION = "system_prompt_extraction"
    AUTHORITY_IMPERSONATION = "authority_impersonation"
    RECURSIVE_INJECTION = "recursive_injection"
    MULTILINGUAL = "multilingual"
    ETHICAL_JUSTIFICATION = "ethical_justification"
    SIMULATION_ATTACK = "simulation_attack"
    HYPOTHETICAL_SCENARIO = "hypothetical_scenario"