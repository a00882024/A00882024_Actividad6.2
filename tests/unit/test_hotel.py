"""Unit tests for Hotel."""
import pytest
from src.hotel import Hotel


class TestHotelCreate:
    """Tests for Hotel.create()."""

    def test_create_returns_hotel_instance(self):
        """Verify create returns a Hotel instance."""
        hotel = Hotel.create(name="Four Seasons")
        assert isinstance(hotel, Hotel)

    def test_create_assigns_id(self):
        """Verify create assigns a non-null id."""
        hotel = Hotel.create(name="Four Seasons")
        assert hotel.id is not None

    def test_create_sets_name(self):
        """Verify create sets the hotel name."""
        hotel = Hotel.create(name="Four Seasons")
        assert hotel.name == "Four Seasons"

    def test_create_persists_to_disk(self):
        """Verify created hotel is persisted to disk."""
        hotel = Hotel.create(name="Four Seasons")
        hotels = Hotel.all()
        assert len(hotels) == 1
        assert hotels[0].id == hotel.id

    def test_create_multiple_hotels(self):
        """Verify multiple hotels can be created."""
        Hotel.create(name="Four Seasons")
        Hotel.create(name="Hilton")
        hotels = Hotel.all()
        assert len(hotels) == 2

    def test_create_assigns_unique_ids(self):
        """Verify each hotel gets a unique id."""
        hotel1 = Hotel.create(name="Four Seasons")
        hotel2 = Hotel.create(name="Hilton")
        assert hotel1.id != hotel2.id


class TestHotelDelete:
    """Tests for Hotel.delete()."""

    def test_delete_removes_hotel(self):
        """Verify delete removes the hotel from disk."""
        hotel = Hotel.create(name="Four Seasons")
        hotel.delete()
        hotels = Hotel.all()
        assert len(hotels) == 0

    def test_delete_only_removes_target(self):
        """Verify delete only removes the targeted hotel."""
        hotel1 = Hotel.create(name="Four Seasons")
        hotel2 = Hotel.create(name="Hilton")
        hotel1.delete()
        hotels = Hotel.all()
        assert len(hotels) == 1
        assert hotels[0].id == hotel2.id

    def test_delete_nonexistent_raises(self):
        """Verify deleting a nonexistent hotel raises ValueError."""
        hotel = Hotel.create(name="Four Seasons")
        hotel.delete()
        with pytest.raises(ValueError):
            hotel.delete()


class TestHotelToStr:
    """Tests for Hotel.to_str()."""

    def test_to_str_contains_name(self):
        """Verify to_str output contains the hotel name."""
        hotel = Hotel.create(name="Four Seasons")
        assert "Four Seasons" in hotel.to_str()

    def test_to_str_contains_id(self):
        """Verify to_str output contains the hotel id."""
        hotel = Hotel.create(name="Four Seasons")
        assert str(hotel.id) in hotel.to_str()


class TestHotelUpdate:
    """Tests for Hotel.update()."""

    def test_update_name(self):
        """Verify update changes the hotel name."""
        hotel = Hotel.create(name="Four Seasons")
        hotel.update(name="Hilton")
        assert hotel.name == "Hilton"

    def test_update_persists_to_disk(self):
        """Verify update persists the change to disk."""
        hotel = Hotel.create(name="Four Seasons")
        hotel.update(name="Hilton")
        hotels = Hotel.all()
        assert hotels[0].name == "Hilton"

    def test_update_does_not_change_id(self):
        """Verify update does not change the hotel id."""
        hotel = Hotel.create(name="Four Seasons")
        original_id = hotel.id
        hotel.update(name="Hilton")
        assert hotel.id == original_id


class TestHotelFindById:
    """Tests for Hotel.find_by_id()."""

    def test_find_by_id_returns_hotel(self):
        """Verify find_by_id returns the correct hotel."""
        hotel = Hotel.create(name="Four Seasons")
        found = Hotel.find_by_id(hotel.id)
        assert isinstance(found, Hotel)
        assert found.id == hotel.id
        assert found.name == hotel.name

    def test_find_by_id_nonexistent_raises(self):
        """Verify find_by_id raises ValueError for nonexistent id."""
        with pytest.raises(ValueError):
            Hotel.find_by_id("nonexistent-id")
