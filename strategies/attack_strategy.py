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