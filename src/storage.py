"""Shared JSON persistence utilities."""
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')


def load(filename):
    """
    Load data from a JSON file in the data directory.

    Returns an empty list if the file does not exist.
    """
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Corrupt JSON in {filename}: {e}")
        return []


def save(filename, data):
    """
    Save data to a JSON file in the data directory.

    Creates the data directory if needed.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
