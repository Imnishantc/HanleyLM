import json
import logging
import time

from models.judge_result import JudgeResult
from prompts.judge_prompts import JUDGE_PROMPT
from target_client import TargetClient


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)


class JudgeAgent:
    """
    Evaluates whether an adversarial attack successfully bypassed
    the target model's safety mechanisms.
    """

    def __init__(
        self,
        retries: int = 3,
        retry_delay: int = 2
    ):

        self.client = TargetClient()

        self.retries = retries
        self.retry_delay = retry_delay

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

    # -------------------------------------------------------

    def _build_judge_prompt(
        self,
        original_prompt: str,
        attacked_prompt: str,
        model_response: str
    ) -> str:

        return JUDGE_PROMPT.format(
            original_prompt=original_prompt,
            attacked_prompt=attacked_prompt,
            model_response=model_response
        )

    # -------------------------------------------------------

    def evaluate(
        self,
        original_prompt: str,
        attacked_prompt: str,
        model_response: str
    ) -> JudgeResult:

        prompt = self._build_judge_prompt(
            original_prompt,
            attacked_prompt,
            model_response
        )

        start_time = time.perf_counter()

        for attempt in range(1, self.retries + 1):

            try:

                self.logger.info(
                    f"Judge Attempt {attempt}"
                )

                response = self.client.generate_response(
                    prompt
                )

                # ====================================================
                # Clean Markdown code fences returned by the LLM
                # ====================================================
                response = response.strip()

                if response.startswith("```json"):
                    response = response.replace(
                        "```json",
                        "",
                        1
                    )

                if response.startswith("```"):
                    response = response.replace(
                        "```",
                        "",
                        1
                    )

                if response.endswith("```"):
                    response = response[:-3]

                response = response.strip()

                # Parse JSON
                data = json.loads(response)

                execution_time = (
                    time.perf_counter() - start_time
                )

                self.logger.info(
                    f"Evaluation completed in {execution_time:.2f}s"
                )

                return JudgeResult(
                    attack_success=data["attack_success"],
                    risk_score=float(data["risk_score"]),
                    severity=data["severity"],
                    reasoning=data["reasoning"]
                )

            except Exception as e:

                self.logger.warning(
                    f"Attempt {attempt} failed: {e}"
                )

                if attempt == self.retries:

                    return JudgeResult(
                        attack_success=False,
                        risk_score=0.0,
                        severity="Unknown",
                        reasoning=f"JudgeAgent failed: {e}"
                    )

                time.sleep(self.retry_delay)