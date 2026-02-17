"""Shared fixtures for unit tests."""
import os
import glob
import pytest

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')


@pytest.fixture(autouse=True)
def clean_data():
    """Clean up all JSON data files before and after each test."""
    os.makedirs(DATA_DIR, exist_ok=True)
    for filepath in glob.glob(os.path.join(DATA_DIR, '*.json')):
        os.remove(filepath)
    yield
    for filepath in glob.glob(os.path.join(DATA_DIR, '*.json')):
        os.remove(filepath)
