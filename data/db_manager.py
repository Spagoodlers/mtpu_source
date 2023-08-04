# db_manager.py
import requests
import json
import os

DATA_FOLDER = "data"
SCRYFALL_DATASET_FILE = os.path.join(DATA_FOLDER, "scryfall_dataset.json")
TOKENS_FILE = os.path.join(DATA_FOLDER, "tokens.txt")


def fetch_and_save_tokens():
    if os.path.exists(SCRYFALL_DATASET_FILE):
        with open(SCRYFALL_DATASET_FILE, "r") as f:
            data = json.load(f)
            tokens = data["data"]
    else:
        print("Local dataset file not found. Please download it from Scryfall first.")
        return

    if os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE, "r") as f:
            existing_tokens = set(line.strip() for line in f.readlines())
    else:
        existing_tokens = set()

    new_tokens = set()

    for token in tokens:
        name = token["name"]
        if name not in existing_tokens:
            new_tokens.add(name)

    with open(TOKENS_FILE, "a") as f:
        for token in new_tokens:
            f.write(token + "\n")


def load_tokens_from_file():
    if os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE, "r") as f:
            tokens = list(set(line.strip() for line in f.readlines()))  # Consolidate duplicates
        return tokens
    else:
        return None
