"""Hotel model with JSON persistence."""
import uuid
from src.storage import load, save
from src.reservation import Reservation

DATA_FILE = 'hotels.json'


class Hotel:
    """Represents a hotel with JSON persistence."""

    def __init__(self, hotel_id, name):
        """Initialize a Hotel instance with an id and name."""
        self.id = hotel_id
        self.name = name

    @classmethod
    def create(cls, name):
        """Create a new hotel, persist it, and return the instance."""
        hotel = cls(hotel_id=str(uuid.uuid4()), name=name)
        data = load(DATA_FILE)
        data.append({"id": hotel.id, "name": hotel.name})
        save(DATA_FILE, data)
        return hotel

    @staticmethod
    def _is_valid_record(record):
        """Check if a record has all required keys."""
        required = {"id", "name"}
        if not isinstance(record, dict) or not required.issubset(record):
            print(f"Warning: Skipping invalid hotel record: {record}")
            return False
        return True

    @classmethod
    def find_by_id(cls, hotel_id):
        """Find a hotel by id. Raises ValueError if not found."""
        data = load(DATA_FILE)
        for h in data:
            if cls._is_valid_record(h) and h["id"] == hotel_id:
                return cls(hotel_id=h["id"], name=h["name"])
        raise ValueError(f"Hotel {hotel_id} not found")

    @classmethod
    def all(cls):
        """Return a list of all persisted Hotel instances."""
        data = load(DATA_FILE)
        return [
            cls(hotel_id=h["id"], name=h["name"])
            for h in data if cls._is_valid_record(h)
        ]

    def delete(self):
        """Delete this hotel from disk. Raises ValueError if not found."""
        data = load(DATA_FILE)
        original_len = len(data)
        data = [h for h in data if h["id"] != self.id]
        if len(data) == original_len:
            raise ValueError(f"Hotel {self.id} not found")
        save(DATA_FILE, data)

    def update(self, name):
        """Update the hotel's name and persist the change to disk."""
        self.name = name
        data = load(DATA_FILE)
        for h in data:
            if h["id"] == self.id:
                h["name"] = name
                break
        save(DATA_FILE, data)

    def reserve_a_room(self, customer, booking_info):
        """Reserve a room at this hotel for a customer."""
        return Reservation.create_reservation(
            customer=customer, hotel=self, booking_info=booking_info
        )

    def cancel_a_reservation(self, reservation):
        """Cancel a reservation at this hotel."""
        reservation.cancel_reservation()

    def to_str(self):
        """Return a string representation of the hotel."""
        return f"Hotel({self.id}, {self.name})"
