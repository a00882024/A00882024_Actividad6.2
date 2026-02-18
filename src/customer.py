"""Customer model with JSON persistence."""
import uuid
from src.storage import load, save

DATA_FILE = 'customers.json'


class Customer:
    """Represents a customer with JSON persistence."""

    def __init__(self, customer_id, name):
        """Initialize a Customer instance with an id and name."""
        self.id = customer_id
        self.name = name

    @classmethod
    def create(cls, name):
        """Create a new customer, persist it, and return the instance."""
        customer = cls(customer_id=str(uuid.uuid4()), name=name)
        data = load(DATA_FILE)
        data.append({"id": customer.id, "name": customer.name})
        save(DATA_FILE, data)
        return customer

    @classmethod
    def find_by_id(cls, customer_id):
        """Find a customer by id. Raises ValueError if not found."""
        data = load(DATA_FILE)
        for c in data:
            if c["id"] == customer_id:
                return cls(customer_id=c["id"], name=c["name"])
        raise ValueError(f"Customer {customer_id} not found")

    @classmethod
    def all(cls):
        """Return a list of all persisted Customer instances."""
        data = load(DATA_FILE)
        return [cls(customer_id=c["id"], name=c["name"]) for c in data]

    def delete(self):
        """Delete this customer from disk. Raises ValueError if not found."""
        data = load(DATA_FILE)
        original_len = len(data)
        data = [c for c in data if c["id"] != self.id]
        if len(data) == original_len:
            raise ValueError(f"Customer {self.id} not found")
        save(DATA_FILE, data)

    def update(self, name):
        """Update the customer's name and persist the change to disk."""
        self.name = name
        data = load(DATA_FILE)
        for c in data:
            if c["id"] == self.id:
                c["name"] = name
                break
        save(DATA_FILE, data)

    def to_str(self):
        """Return a string representation of the customer."""
        return f"Customer({self.id}, {self.name})"
