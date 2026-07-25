from utils.file_handler import load_json, save_json


def process_prompt(seed):
    """
    Process a single prompt.
    """

    # Extract data
    prompt_number = seed["No"]
    category = seed["Suggested Category"]
    prompt = seed["Prompt"]

    print("\n" + "=" * 50)
    print(f"📌 Processing Prompt {prompt_number}")
    print(f"📂 Category : {category}")
    print("-" * 50)

    print("✅ Prompt Loaded")
    print("⚔️  Attack Stage      : Waiting")
    print("🤖 Target Client      : Waiting")
    print("💾 Result Prepared")

    # Placeholder (will be replaced later)
    response = "Waiting for target_client.py"

    result = {
        "No": prompt_number,
        "Category": category,
        "Prompt": prompt,
        "Response": response
    }

    print("=" * 50)

    return result


def process_dataset():
    """
    Process the entire dataset.
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
            print(f"❌ Error processing Prompt {seed['No']}: {e}")
            continue

    save_json(results, "reports/results.json")

    print("\n" + "=" * 50)
    print(f"✅ Successfully processed {len(results)} prompts.")
    print("📄 Report generated successfully.")
    print("=" * 50)


def main():
    """
    Entry point of the pipeline.
    """
    process_dataset()


if __name__ == "__main__":
    main()