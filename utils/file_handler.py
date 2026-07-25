import json
import os


def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None

    except json.JSONDecodeError:
        print(f"Invalid JSON: {file_path}")
        return None


def save_json(data, file_path):

    folder = os.path.dirname(file_path)

    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"Saved: {file_path}")