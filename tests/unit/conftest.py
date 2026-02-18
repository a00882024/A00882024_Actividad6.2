"""Shared fixtures for unit tests."""
import os
import glob
import pytest
from src.hotel import Hotel
from src.customer import Customer
from src.reservation import BookingInfo

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


@pytest.fixture
def sample_reservation_data():
    """Create a hotel, customer, and booking info for reservation tests."""
    hotel = Hotel.create(name="Four Seasons")
    customer = Customer.create(name="Jon Doe")
    info = BookingInfo(
        check_in="2026-03-01", check_out="2026-03-05", room="101"
    )
    return hotel, customer, info
