from utils.file_handler import load_json, save_json

# Load Dataset
seeds = load_json("data/seeds.json")

if seeds is None:
    exit()

print(f"Loaded {len(seeds)} prompts.\n")

results = []

for seed in seeds:

    print(f"Processing Prompt {seed['No']}...")

    results.append({
        "No": seed["No"],
        "Category": seed["Suggested Category"],
        "Prompt": seed["Prompt"],
        "Response": "Waiting for target_client.py"
    })

save_json(results, "reports/results.json")

print("\n====================================")
print(f"Successfully processed {len(results)} prompts.")
print("Report saved at : reports/results.json")
print("====================================")