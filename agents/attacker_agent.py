import logging
import random
import time
from typing import List, Optional

from models.attack_result import AttackResult
from prompts.attacker_prompts import ATTACK_PROMPTS
from strategies.attack_strategy import AttackStrategy
from target_client import TargetClient


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)


class AttackerAgent:
    """
    Generates adversarial prompt variations using
    different attack strategies.
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

    def available_strategies(
        self
    ) -> List[AttackStrategy]:

        return list(AttackStrategy)

    # -------------------------------------------------------

    def _validate_prompt(
        self,
        prompt: str
    ):

        if not isinstance(prompt, str):

            raise TypeError(
                "Prompt must be a string."
            )

        if not prompt.strip():

            raise ValueError(
                "Prompt cannot be empty."
            )

    # -------------------------------------------------------

    def _validate_strategy(
        self,
        strategy: AttackStrategy
    ):

        if strategy not in ATTACK_PROMPTS:

            raise ValueError(
                f"Unsupported strategy: {strategy}"
            )

    # -------------------------------------------------------

    def _select_random_strategy(
        self
    ) -> AttackStrategy:

        return random.choice(
            list(AttackStrategy)
        )

    # -------------------------------------------------------

    def _build_attack_prompt(

        self,

        prompt: str,

        strategy: AttackStrategy

    ) -> str:

        template = ATTACK_PROMPTS[strategy]

        return template.format(
            prompt=prompt
        )

    # -------------------------------------------------------

    def _execute_attack(

        self,

        attack_prompt: str

    ) -> str:

        last_exception = None

        for attempt in range(
            1,
            self.retries + 1
        ):

            try:

                self.logger.info(
                    f"Attempt {attempt}"
                )

                response = self.client.generate_response(
                    attack_prompt
                )               

                return response.strip()

            except Exception as e:

                last_exception = e

                self.logger.warning(
                    f"Attempt {attempt} failed: {e}"
                )

                if attempt < self.retries:

                    time.sleep(
                        self.retry_delay
                    )

        raise RuntimeError(
            f"Attack failed after {self.retries} retries."
        ) from last_exception

            # -------------------------------------------------------

    def attack(
        self,
        prompt: str,
        strategy: Optional[AttackStrategy] = None
    ) -> AttackResult:

        self._validate_prompt(prompt)

        if strategy is None:
            strategy = self._select_random_strategy()

        self._validate_strategy(strategy)

        attack_prompt = self._build_attack_prompt(
            prompt,
            strategy
        )

        self.logger.info("=" * 60)
        self.logger.info(f"Strategy : {strategy.value}")
        self.logger.info(f"Original : {prompt}")

        start_time = time.perf_counter()

        try:

            attacked_prompt = self._execute_attack(
                attack_prompt
            )

            execution_time = (
                time.perf_counter() - start_time
            )

            self.logger.info(
                "Attack completed successfully."
            )

            return AttackResult(
                original_prompt=prompt,
                attacked_prompt=attacked_prompt,
                strategy=strategy.value,
                success=True,
                execution_time=execution_time
            )

        except Exception as e:

            execution_time = (
                time.perf_counter() - start_time
            )

            self.logger.error(str(e))

            return AttackResult(
                original_prompt=prompt,
                attacked_prompt="",
                strategy=strategy.value,
                success=False,
                execution_time=execution_time,
                error=str(e)
            )

    # -------------------------------------------------------

    def attack_random(
        self,
        prompt: str
    ) -> AttackResult:

        strategy = self._select_random_strategy()

        return self.attack(
            prompt=prompt,
            strategy=strategy
        )

    # -------------------------------------------------------

    def attack_all(
        self,
        prompt: str
    ) -> List[AttackResult]:

        results = []

        for strategy in AttackStrategy:

            result = self.attack(
                prompt=prompt,
                strategy=strategy
            )

            results.append(result)

        return results

    # -------------------------------------------------------

    def print_available_strategies(
        self
    ):

        print("\nAvailable Attack Strategies\n")

        for strategy in AttackStrategy:

            print(
                f"• {strategy.value}"
            )