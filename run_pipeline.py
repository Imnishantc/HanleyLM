from utils.file_handler import load_json, save_json
from target_client import TargetClient
from utils.file_handler import load_json, save_json

# Initialize Target Client
client = TargetClient()

# Load Dataset
seeds = load_json("data/seeds.json")

if seeds is None:
    exit()

print(f"Loaded {len(seeds)} prompts.\n")

results = []

for seed in seeds:

    print(f"Processing Prompt {seed['No']}...")

    try:
        response = client.generate_response(seed["Prompt"])

    except Exception as e:
        response = f"ERROR: {str(e)}"

    results.append({
        "No": seed["No"],
        "Category": seed["Suggested Category"],
        "Prompt": seed["Prompt"],
        "Response": response
    })

save_json(results, "reports/results.json")

print("\n====================================")
print(f"Successfully processed {len(results)} prompts.")
print("Report saved at : reports/results.json")
print("====================================")