"""Hotel model with JSON persistence."""
import json
import os
import uuid

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
DATA_FILE = os.path.join(DATA_DIR, 'hotels.json')


def _load():
    """
    Load hotel data from the JSON file.

    Returns an empty list if the file does not exist.
    """
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save(data):
    """
    Save hotel data to the JSON file.

    Creates the data directory if needed.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


class Hotel:
    """Represents a hotel with JSON persistence."""

    def __init__(self, hotel_id, name):
        """Initialize a Hotel instance with an id and name."""
        self.id = hotel_id
        self.name = name

    @classmethod
    def create(cls, name):
        """Create a new hotel, persist it to disk, and return the instance."""
        hotel = cls(hotel_id=str(uuid.uuid4()), name=name)
        data = _load()
        data.append({"id": hotel.id, "name": hotel.name})
        _save(data)
        return hotel

    @classmethod
    def all(cls):
        """Return a list of all persisted Hotel instances."""
        data = _load()
        return [cls(hotel_id=h["id"], name=h["name"]) for h in data]

    def delete(self):
        """Delete this hotel from disk. Raises ValueError if not found."""
        data = _load()
        original_len = len(data)
        data = [h for h in data if h["id"] != self.id]
        if len(data) == original_len:
            raise ValueError(f"Hotel {self.id} not found")
        _save(data)

    def update(self, name):
        """Update the hotel's name and persist the change to disk."""
        self.name = name
        data = _load()
        for h in data:
            if h["id"] == self.id:
                h["name"] = name
                break
        _save(data)

    def to_str(self):
        """Return a string representation of the hotel."""
        return f"Hotel({self.id}, {self.name})"
