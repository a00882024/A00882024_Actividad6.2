"""Unit tests for invalid file data handling."""
import os
from src.storage import DATA_DIR
from src.hotel import Hotel
from src.customer import Customer
from src.reservation import Reservation


def _write_raw(filename, content):
    """Write raw content to a data file."""
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


class TestCorruptJson:
    """Tests for corrupt JSON file handling."""

    def test_corrupt_json_returns_empty_list(self, capsys):
        """Verify load returns empty list for corrupt JSON."""
        _write_raw('hotels.json', '{not valid json')
        hotels = Hotel.all()
        assert hotels == []
        captured = capsys.readouterr()
        assert "Error: Corrupt JSON" in captured.out

    def test_corrupt_json_allows_new_create(self, capsys):
        """Verify create works after corrupt JSON is encountered."""
        _write_raw('hotels.json', '{bad}')
        Hotel.all()  # triggers the error, resets to []
        hotel = Hotel.create(name="Four Seasons")
        assert hotel.name == "Four Seasons"
        captured = capsys.readouterr()
        assert "Error: Corrupt JSON" in captured.out


class TestMalformedHotelRecords:
    """Tests for malformed hotel records."""

    def test_all_skips_record_missing_name(self, capsys):
        """Verify all() skips hotel records missing the name key."""
        _write_raw('hotels.json', '[{"id": "1"}]')
        hotels = Hotel.all()
        assert len(hotels) == 0
        captured = capsys.readouterr()
        assert "Warning: Skipping invalid hotel record" in captured.out

    def test_all_skips_non_dict_record(self, capsys):
        """Verify all() skips non-dict entries in the list."""
        _write_raw('hotels.json', '[42, {"id": "1", "name": "Valid"}]')
        hotels = Hotel.all()
        assert len(hotels) == 1
        assert hotels[0].name == "Valid"
        captured = capsys.readouterr()
        assert "Warning: Skipping invalid hotel record" in captured.out

    def test_all_keeps_valid_records(self):
        """Verify all() returns valid records alongside invalid ones."""
        _write_raw(
            'hotels.json',
            '[{"id": "1", "name": "Good"}, {"id": "2"}]'
        )
        hotels = Hotel.all()
        assert len(hotels) == 1
        assert hotels[0].name == "Good"


class TestMalformedCustomerRecords:
    """Tests for malformed customer records."""

    def test_all_skips_record_missing_id(self, capsys):
        """Verify all() skips customer records missing the id key."""
        _write_raw('customers.json', '[{"name": "Jon"}]')
        customers = Customer.all()
        assert len(customers) == 0
        captured = capsys.readouterr()
        assert "Warning: Skipping invalid customer record" in captured.out

    def test_all_keeps_valid_records(self):
        """Verify all() returns valid records alongside invalid ones."""
        _write_raw(
            'customers.json',
            '[{"id": "1", "name": "Good"}, {"name": "Bad"}]'
        )
        customers = Customer.all()
        assert len(customers) == 1
        assert customers[0].name == "Good"


class TestMalformedReservationRecords:
    """Tests for malformed reservation records."""

    def test_all_skips_record_missing_keys(self, capsys):
        """Verify all() skips reservation records missing required keys."""
        _write_raw('reservations.json', '[{"id": "1"}]')
        reservations = Reservation.all()
        assert len(reservations) == 0
        captured = capsys.readouterr()
        assert "Warning: Skipping invalid reservation record" in captured.out

    def test_all_keeps_valid_records(self):
        """Verify all() returns valid records alongside invalid ones."""
        valid = (
            '{"id": "1", "hotel_id": "h1", "customer_id": "c1",'
            ' "check_in": "2026-03-01", "check_out": "2026-03-05",'
            ' "room": "101", "status": "active"}'
        )
        _write_raw(
            'reservations.json',
            f'[{valid}, {{"id": "2"}}]'
        )
        reservations = Reservation.all()
        assert len(reservations) == 1
        assert reservations[0].id == "1"
