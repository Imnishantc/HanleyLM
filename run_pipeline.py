from utils.file_handler import load_json, save_json
from target_client import TargetClient
from agents.attacker_agent import AttackerAgent
from agents.judge_agent import JudgeAgent

# Initialize components
client = TargetClient()
attacker = AttackerAgent()
judge = JudgeAgent()


def process_prompt(seed):
    """
    Process a single prompt through the complete pipeline.
    """

    prompt_number = seed["No"]
    category = seed["Suggested Category"]
    prompt = seed["Prompt"]

    print("\n" + "=" * 60)
    print(f"Processing Prompt {prompt_number}")
    print(f"Category : {category}")
    print("-" * 60)

    print("✅ Prompt Loaded")

    # --------------------------------------------------
    # Step 1 : Generate attacked prompt
    # --------------------------------------------------
    attack_result = attacker.attack(prompt)

    if not attack_result.success:
        raise RuntimeError(
            f"Attack failed: {attack_result.error}"
        )

    attacked_prompt = attack_result.attacked_prompt

    print("Attack Stage      : Completed")
    print(f"Strategy          : {attack_result.strategy}")

    # --------------------------------------------------
    # Step 2 : Send attacked prompt to target model
    # --------------------------------------------------
    response = client.generate_response(attacked_prompt)

    print("Target Client     : Completed")

    # --------------------------------------------------
    # Step 3 : Judge Evaluation
    # --------------------------------------------------
    judge_result = judge.evaluate(
        original_prompt=prompt,
        attacked_prompt=attacked_prompt,
        model_response=response
    )

    print("Judge Agent       : Completed")

    # --------------------------------------------------
    # Final Result
    # --------------------------------------------------
    result = {
        "No": prompt_number,
        "Category": category,

        "Original Prompt": prompt,

        "Attack Strategy": attack_result.strategy,

        "Attacked Prompt": attacked_prompt,

        # Attack Generation Status
        "Attack Generated": attack_result.success,

        # Target Model Response
        "Target Response": response,

        # Judge Evaluation
        "Attack Success": judge_result.attack_success,
        "Risk Score": judge_result.risk_score,
        "Severity": judge_result.severity,
        "Judge Reason": judge_result.reasoning,
        "Timestamp": judge_result.timestamp,

        # Performance
        "Execution Time": attack_result.execution_time
    }

    print("Result Prepared")
    print("=" * 60)

    return result


def process_dataset():
    """
    Process all prompts from dataset.
    """

    seeds = load_json("data/seeds.json")

    if seeds is None:
        return

    print(f"\n✅ Loaded {len(seeds)} prompts.\n")

    results = []

    for seed in seeds:

        try:

            result = process_prompt(seed)

            results.append(result)

        except Exception as e:

            print(f"\n❌ Error processing Prompt {seed['No']}")
            print(e)

            results.append({
                "No": seed["No"],
                "Category": seed["Suggested Category"],
                "Original Prompt": seed["Prompt"],
                "Attack Strategy": None,
                "Attacked Prompt": None,
                "Attack Generated": False,
                "Target Response": None,
                "Attack Success": False,
                "Risk Score": 0.0,
                "Severity": "Unknown",
                "Judge Reason": str(e),
                "Timestamp": None,
                "Execution Time": None,
                "Error": str(e)
            })

    save_json(results, "reports/results.json")

    print("\n" + "=" * 60)
    print(f"✅ Successfully processed {len(results)} prompts.")
    print("Report generated successfully.")
    print("=" * 60)


def main():
    process_dataset()


if __name__ == "__main__":
    main()