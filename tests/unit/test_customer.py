"""Unit tests for Customer."""
import pytest
from src.customer import Customer


class TestCustomerCreate:
    """Tests for Customer.create()."""

    def test_create_returns_customer_instance(self):
        """Verify create returns a Customer instance."""
        customer = Customer.create(name="Jon Doe")
        assert isinstance(customer, Customer)

    def test_create_assigns_id(self):
        """Verify create assigns a non-null id."""
        customer = Customer.create(name="Jon Doe")
        assert customer.id is not None

    def test_create_sets_name(self):
        """Verify create sets the customer name."""
        customer = Customer.create(name="Jon Doe")
        assert customer.name == "Jon Doe"

    def test_create_persists_to_disk(self):
        """Verify created customer is persisted to disk."""
        customer = Customer.create(name="Jon Doe")
        customers = Customer.all()
        assert len(customers) == 1
        assert customers[0].id == customer.id

    def test_create_multiple_customers(self):
        """Verify multiple customers can be created."""
        Customer.create(name="Jon Doe")
        Customer.create(name="Jane Doe")
        customers = Customer.all()
        assert len(customers) == 2

    def test_create_assigns_unique_ids(self):
        """Verify each customer gets a unique id."""
        customer1 = Customer.create(name="Jon Doe")
        customer2 = Customer.create(name="Jane Doe")
        assert customer1.id != customer2.id


class TestCustomerDelete:
    """Tests for Customer.delete()."""

    def test_delete_removes_customer(self):
        """Verify delete removes the customer from disk."""
        customer = Customer.create(name="Jon Doe")
        customer.delete()
        customers = Customer.all()
        assert len(customers) == 0

    def test_delete_only_removes_target(self):
        """Verify delete only removes the targeted customer."""
        customer1 = Customer.create(name="Jon Doe")
        customer2 = Customer.create(name="Jane Doe")
        customer1.delete()
        customers = Customer.all()
        assert len(customers) == 1
        assert customers[0].id == customer2.id

    def test_delete_nonexistent_raises(self):
        """Verify deleting a nonexistent customer raises ValueError."""
        customer = Customer.create(name="Jon Doe")
        customer.delete()
        with pytest.raises(ValueError):
            customer.delete()


class TestCustomerToStr:
    """Tests for Customer.to_str()."""

    def test_to_str_contains_name(self):
        """Verify to_str output contains the customer name."""
        customer = Customer.create(name="Jon Doe")
        assert "Jon Doe" in customer.to_str()

    def test_to_str_contains_id(self):
        """Verify to_str output contains the customer id."""
        customer = Customer.create(name="Jon Doe")
        assert str(customer.id) in customer.to_str()


class TestCustomerUpdate:
    """Tests for Customer.update()."""

    def test_update_name(self):
        """Verify update changes the customer name."""
        customer = Customer.create(name="Jon Doe")
        customer.update(name="Jane Doe")
        assert customer.name == "Jane Doe"

    def test_update_persists_to_disk(self):
        """Verify update persists the change to disk."""
        customer = Customer.create(name="Jon Doe")
        customer.update(name="Jane Doe")
        customers = Customer.all()
        assert customers[0].name == "Jane Doe"

    def test_update_does_not_change_id(self):
        """Verify update does not change the customer id."""
        customer = Customer.create(name="Jon Doe")
        original_id = customer.id
        customer.update(name="Jane Doe")
        assert customer.id == original_id


class TestCustomerFindById:
    """Tests for Customer.find_by_id()."""

    def test_find_by_id_returns_customer(self):
        """Verify find_by_id returns the correct customer."""
        customer = Customer.create(name="Jon Doe")
        found = Customer.find_by_id(customer.id)
        assert isinstance(found, Customer)
        assert found.id == customer.id
        assert found.name == customer.name

    def test_find_by_id_nonexistent_raises(self):
        """Verify find_by_id raises ValueError for nonexistent id."""
        with pytest.raises(ValueError):
            Customer.find_by_id("nonexistent-id")
