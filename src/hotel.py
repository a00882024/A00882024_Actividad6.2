"""Hotel model with JSON persistence."""
import uuid
from src.storage import load, save

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

    @classmethod
    def all(cls):
        """Return a list of all persisted Hotel instances."""
        data = load(DATA_FILE)
        return [cls(hotel_id=h["id"], name=h["name"]) for h in data]

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

    def to_str(self):
        """Return a string representation of the hotel."""
        return f"Hotel({self.id}, {self.name})"
