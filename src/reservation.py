"""Reservation model with JSON persistence."""
import uuid
from collections import namedtuple
from src.storage import load, save

DATA_FILE = 'reservations.json'

BookingInfo = namedtuple('BookingInfo', ['check_in', 'check_out', 'room'])


class Reservation:
    """Represents a reservation with JSON persistence."""

    # pylint: disable=too-many-arguments
    def __init__(self, *, reservation_id, hotel_id, customer_id,
                 booking_info, status="active"):
        """Initialize a Reservation instance."""
        self.id = reservation_id
        self.hotel_id = hotel_id
        self.customer_id = customer_id
        self.booking_info = booking_info
        self.status = status

    @classmethod
    def create_reservation(cls, *, customer, hotel, booking_info):
        """Create a new reservation, persist it, and return the instance."""
        reservation = cls(
            reservation_id=str(uuid.uuid4()),
            hotel_id=hotel.id,
            customer_id=customer.id,
            booking_info=booking_info,
        )
        data = load(DATA_FILE)
        data.append({
            "id": reservation.id,
            "hotel_id": reservation.hotel_id,
            "customer_id": reservation.customer_id,
            "check_in": reservation.booking_info.check_in,
            "check_out": reservation.booking_info.check_out,
            "room": reservation.booking_info.room,
            "status": reservation.status,
        })
        save(DATA_FILE, data)
        return reservation

    def cancel_reservation(self):
        """Cancel this reservation and persist the change."""
        self.status = "cancelled"
        data = load(DATA_FILE)
        for r in data:
            if r["id"] == self.id:
                r["status"] = "cancelled"
                break
        save(DATA_FILE, data)

    @staticmethod
    def _is_valid_record(record):
        """Check if a record has all required keys."""
        required = {
            "id", "hotel_id", "customer_id",
            "check_in", "check_out", "room", "status",
        }
        if not isinstance(record, dict) or not required.issubset(record):
            print(f"Warning: Skipping invalid reservation record: {record}")
            return False
        return True

    @classmethod
    def _build(cls, record):
        """Build a Reservation instance from a JSON record."""
        return cls(
            reservation_id=record["id"],
            hotel_id=record["hotel_id"],
            customer_id=record["customer_id"],
            booking_info=BookingInfo(
                check_in=record["check_in"],
                check_out=record["check_out"],
                room=record["room"],
            ),
            status=record["status"],
        )

    @classmethod
    def find_by_id(cls, reservation_id):
        """Find a reservation by id. Raises ValueError if not found."""
        data = load(DATA_FILE)
        for r in data:
            if cls._is_valid_record(r) and r["id"] == reservation_id:
                return cls._build(r)
        raise ValueError(f"Reservation {reservation_id} not found")

    @classmethod
    def all(cls):
        """Return a list of all persisted Reservation instances."""
        data = load(DATA_FILE)
        return [cls._build(r) for r in data if cls._is_valid_record(r)]
