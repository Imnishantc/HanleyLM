from utils.file_handler import load_json, save_json
from target_client import TargetClient
from agents.attacker_agent import AttackerAgent
from agents.judge_agent import JudgeAgent
from utils.report_generator import ReportGenerator
from utils.reports_V2.report_generator_v2 import ReportGenerator

# ==========================================================
# Initialize Components
# ==========================================================

client = TargetClient()
attacker = AttackerAgent()
judge = JudgeAgent()


# ==========================================================
# Process a Single Prompt
# ==========================================================

def process_prompt(seed):
    """
    Process one prompt through all attack strategies.
    """

    prompt_number = seed["No"]
    category = seed["Suggested Category"]
    prompt = seed["Prompt"]

    print("\n" + "=" * 60)
    print(f"Processing Prompt {prompt_number}")
    print(f"Category : {category}")
    print("=" * 60)

    all_results = []

    # ------------------------------------------------------
    # Run Every Attack Strategy
    # ------------------------------------------------------

    for strategy in attacker.available_strategies():

        attack_result = attacker.attack(
            prompt=prompt,
            strategy=strategy
        )

        print("\n" + "-" * 60)
        print(f"Strategy : {attack_result.strategy}")
        print("-" * 60)

        if not attack_result.success:

            all_results.append({

                "No": prompt_number,

                "Category": category,

                "Original Prompt": prompt,

                "Attack Strategy": attack_result.strategy,

                "Attacked Prompt": None,

                "Attack Generated": False,

                "Target Response": None,

                "Attack Success": False,

                "Risk Score": 0.0,

                "Severity": "Unknown",

                "Judge Decision": attack_result.error,

                "Timestamp": None,

                "Execution Time": attack_result.execution_time

            })

            continue

        attacked_prompt = attack_result.attacked_prompt

        # --------------------------------------------------
        # Target Model
        # --------------------------------------------------

        response = client.generate_response(
            attacked_prompt
        )

        # --------------------------------------------------
        # Judge
        # --------------------------------------------------

        judge_result = judge.evaluate(

            original_prompt=prompt,

            attacked_prompt=attacked_prompt,

            model_response=response

        )

        # --------------------------------------------------
        # Store Result
        # --------------------------------------------------

        all_results.append({

            "No": prompt_number,

            "Category": category,

            "Original Prompt": prompt,

            "Attack Strategy": attack_result.strategy,

            "Attacked Prompt": attacked_prompt,

            "Attack Generated": True,

            "Target Response": response,

            "Attack Success": judge_result.attack_success,

            "Risk Score": judge_result.risk_score,

            "Severity": judge_result.severity,

            "Judge Decision": judge_result.reasoning,

            "Timestamp": judge_result.timestamp,

            "Execution Time": attack_result.execution_time

        })

    return all_results

# ==========================================================
# Process Complete Dataset
# ==========================================================

def process_dataset():

    seeds = load_json("data/seeds_test.json")

    if seeds is None:
        print("❌ Could not load dataset.")
        return

    print("\n" + "=" * 60)
    print(f"Loaded {len(seeds)} prompts.")
    print("=" * 60)

    results = []

    # ------------------------------------------------------
    # Process Each Prompt
    # ------------------------------------------------------

    for seed in seeds:

        try:

           prompt_results = process_prompt(seed)

           results.extend(prompt_results)

        except Exception as e:

            print("\n" + "=" * 60)
            print(f"❌ Error Processing Prompt {seed['No']}")
            print(e)
            print("=" * 60)

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

                "Judge Decision": str(e),

                "Timestamp": None,

                "Execution Time": None,

                "Error": str(e)

            })

    # ------------------------------------------------------
    # Save JSON Results
    # ------------------------------------------------------

    save_json(
        results,
        "reports/results.json"
    )

    print("\n✅ JSON Report Saved Successfully")

    # ------------------------------------------------------
    # Generate Professional PDF Report
    # ------------------------------------------------------

    print("\n" + "=" * 60)
    print("Generating Professional PDF Report...")
    print("=" * 60)

    try:

        ReportGenerator().generate_reports()

        print("\n✅ Professional PDF Report Generated Successfully!")

    except Exception as e:

        print("\n❌ Report Generation Failed")
        print(e)

    print("\n" + "=" * 60)
    print(f"Successfully Processed {len(seeds)} Prompts")
    print(f"Total Attack Executions : {len(results)}")
    print("=" * 60)


# ==========================================================
# Main
# ==========================================================

def main():

    process_dataset()


if __name__ == "__main__":

    main()