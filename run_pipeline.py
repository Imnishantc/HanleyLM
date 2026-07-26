from utils.file_handler import load_json, save_json
from target_client import TargetClient
from agents.attacker_agent import AttackerAgent

# Initialize components
client = TargetClient()
attacker = AttackerAgent()


def process_prompt(seed):
    """
    Process a single prompt through the attack pipeline.
    """

    prompt_number = seed["No"]
    category = seed["Suggested Category"]
    prompt = seed["Prompt"]

    print("\n" + "=" * 60)
    print(f" Processing Prompt {prompt_number}")
    print(f"Category : {category}")
    print("-" * 60)

    print("✅ Prompt Loaded")

    # -----------------------------
    # Step 1 : Generate attacked prompt
    # -----------------------------
    attack_result = attacker.attack(prompt)

    if not attack_result.success:
        raise RuntimeError(
            f"Attack failed: {attack_result.error}"
        )

    attacked_prompt = attack_result.attacked_prompt

    print(" Attack Stage      : Completed")
    print(f" Strategy          : {attack_result.strategy}")

    # -----------------------------
    # Step 2 : Send attacked prompt
    # to target model
    # -----------------------------
    response = client.generate_response(attacked_prompt)

    print(" Target Client     : Completed")

    # -----------------------------
    # Final Result
    # -----------------------------
    result = {
        "No": prompt_number,
        "Category": category,
        "Original Prompt": prompt,
        "Attack Strategy": attack_result.strategy,
        "Attacked Prompt": attacked_prompt,
        "Attack Success": attack_result.success,
        "Execution Time": attack_result.execution_time,
        "Response": response
    }

    print(" Result Prepared")
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
                "Attack Success": False,
                "Execution Time": None,
                "Response": None,
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