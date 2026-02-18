"""Unit tests for Reservation."""
import pytest
from src.reservation import Reservation


class TestReservationCreate:
    """Tests for Reservation.create_reservation()."""

    def test_create_returns_reservation_instance(self,
                                                 sample_reservation_data):
        """Verify create_reservation returns a Reservation instance."""
        hotel, customer, info = sample_reservation_data
        reservation = Reservation.create_reservation(
            customer=customer, hotel=hotel, booking_info=info
        )
        assert isinstance(reservation, Reservation)

    def test_create_assigns_id(self, sample_reservation_data):
        """Verify create_reservation assigns a non-null id."""
        hotel, customer, info = sample_reservation_data
        reservation = Reservation.create_reservation(
            customer=customer, hotel=hotel, booking_info=info
        )
        assert reservation.id is not None

    def test_create_stores_hotel_id(self, sample_reservation_data):
        """Verify create_reservation stores the hotel id."""
        hotel, customer, info = sample_reservation_data
        reservation = Reservation.create_reservation(
            customer=customer, hotel=hotel, booking_info=info
        )
        assert reservation.hotel_id == hotel.id

    def test_create_stores_customer_id(self, sample_reservation_data):
        """Verify create_reservation stores the customer id."""
        hotel, customer, info = sample_reservation_data
        reservation = Reservation.create_reservation(
            customer=customer, hotel=hotel, booking_info=info
        )
        assert reservation.customer_id == customer.id

    def test_create_stores_booking_info(self, sample_reservation_data):
        """Verify create_reservation stores check-in, check-out, and room."""
        hotel, customer, info = sample_reservation_data
        reservation = Reservation.create_reservation(
            customer=customer, hotel=hotel, booking_info=info
        )
        assert reservation.booking_info.check_in == "2026-03-01"
        assert reservation.booking_info.check_out == "2026-03-05"
        assert reservation.booking_info.room == "101"

    def test_create_status_defaults_to_active(self, sample_reservation_data):
        """Verify create_reservation sets status to 'active'."""
        hotel, customer, info = sample_reservation_data
        reservation = Reservation.create_reservation(
            customer=customer, hotel=hotel, booking_info=info
        )
        assert reservation.status == "active"

    def test_create_persists_to_disk(self, sample_reservation_data):
        """Verify created reservation is persisted to disk."""
        hotel, customer, info = sample_reservation_data
        reservation = Reservation.create_reservation(
            customer=customer, hotel=hotel, booking_info=info
        )
        reservations = Reservation.all()
        assert len(reservations) == 1
        assert reservations[0].id == reservation.id


class TestReservationCancel:
    """Tests for Reservation.cancel_reservation()."""

    def test_cancel_sets_status_to_cancelled(self, sample_reservation_data):
        """Verify cancel_reservation sets status to 'cancelled'."""
        hotel, customer, info = sample_reservation_data
        reservation = Reservation.create_reservation(
            customer=customer, hotel=hotel, booking_info=info
        )
        reservation.cancel_reservation()
        assert reservation.status == "cancelled"

    def test_cancel_persists_to_disk(self, sample_reservation_data):
        """Verify cancel_reservation persists the change to disk."""
        hotel, customer, info = sample_reservation_data
        reservation = Reservation.create_reservation(
            customer=customer, hotel=hotel, booking_info=info
        )
        reservation.cancel_reservation()
        found = Reservation.find_by_id(reservation.id)
        assert found.status == "cancelled"

    def test_cancel_keeps_record_in_storage(self, sample_reservation_data):
        """Verify cancel_reservation keeps the record in storage."""
        hotel, customer, info = sample_reservation_data
        reservation = Reservation.create_reservation(
            customer=customer, hotel=hotel, booking_info=info
        )
        reservation.cancel_reservation()
        reservations = Reservation.all()
        assert len(reservations) == 1


class TestReservationFindById:
    """Tests for Reservation.find_by_id()."""

    def test_find_by_id_returns_reservation(self, sample_reservation_data):
        """Verify find_by_id returns the correct reservation."""
        hotel, customer, info = sample_reservation_data
        reservation = Reservation.create_reservation(
            customer=customer, hotel=hotel, booking_info=info
        )
        found = Reservation.find_by_id(reservation.id)
        assert isinstance(found, Reservation)
        assert found.id == reservation.id
        assert found.hotel_id == hotel.id
        assert found.customer_id == customer.id

    def test_find_by_id_nonexistent_raises(self):
        """Verify find_by_id raises ValueError for nonexistent id."""
        with pytest.raises(ValueError):
            Reservation.find_by_id("nonexistent-id")
