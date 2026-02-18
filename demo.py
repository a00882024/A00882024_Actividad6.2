"""Demo script that exercises the Hotel, Customer, and Reservation models."""
import glob
import os
from src.hotel import Hotel
from src.customer import Customer
from src.storage import DATA_DIR
from src.reservation import BookingInfo, Reservation


def _clean_data():
    """Remove all JSON data files to start fresh."""
    os.makedirs(DATA_DIR, exist_ok=True)
    for filepath in glob.glob(os.path.join(DATA_DIR, '*.json')):
        os.remove(filepath)


def main():
    """Run the demo."""
    _clean_data()

    print("=" * 60)
    print("  Hotel Reservation System Demo")
    print("=" * 60)

    # --- Hotels ---
    print("\n--- Creating Hotels ---")
    hotels = [
        Hotel.create(name="Four Seasons"),
        Hotel.create(name="Hilton"),
        Hotel.create(name="Marriott"),
    ]
    for h in hotels:
        print(f"  Created: {h.to_str()}")

    # --- Customers ---
    print("\n--- Creating Customers ---")
    customers = [
        Customer.create(name="Alice Johnson"),
        Customer.create(name="Bob Smith"),
        Customer.create(name="Carol White"),
        Customer.create(name="David Brown"),
        Customer.create(name="Eva Martinez"),
    ]
    for c in customers:
        print(f"  Created: {c.to_str()}")

    # --- Reservations ---
    print("\n--- Creating 10 Reservations ---")
    bookings = [
        (0, 0, "2026-03-01", "2026-03-05", "101"),
        (1, 0, "2026-03-10", "2026-03-14", "202"),
        (2, 1, "2026-04-01", "2026-04-03", "303"),
        (3, 1, "2026-04-05", "2026-04-10", "104"),
        (4, 2, "2026-05-01", "2026-05-07", "501"),
        (0, 2, "2026-05-10", "2026-05-15", "502"),
        (1, 0, "2026-06-01", "2026-06-04", "201"),
        (2, 1, "2026-06-10", "2026-06-12", "301"),
        (3, 2, "2026-07-01", "2026-07-05", "105"),
        (4, 0, "2026-07-10", "2026-07-14", "103"),
    ]

    reservations = []
    for cust_idx, hotel_idx, ci, co, room in bookings:
        customer = customers[cust_idx]
        hotel = hotels[hotel_idx]
        info = BookingInfo(check_in=ci, check_out=co, room=room)
        res = hotel.reserve_a_room(customer, info)
        reservations.append(res)
        print(
            f"  Reservation {res.id[:8]}... | "
            f"{customer.name} @ {hotel.name} | "
            f"Room {room} | {ci} -> {co}"
        )

    # --- Display summary ---
    print("\n--- Summary ---")
    print(f"  Hotels:       {len(Hotel.all())}")
    print(f"  Customers:    {len(Customer.all())}")
    print(f"  Reservations: {len(Reservation.all())}")

    # --- Cancel a couple reservations ---
    print("\n--- Cancelling 2 Reservations ---")
    for res in reservations[:2]:
        hotels[0].cancel_a_reservation(res)
        print(f"  Cancelled: {res.id[:8]}... (status: {res.status})")

    # --- Final status ---
    print("\n--- Final Reservation Statuses ---")
    for res in Reservation.all():
        print(
            f"  {res.id[:8]}... | "
            f"room {res.booking_info.room} | "
            f"status: {res.status}"
        )

    print("\n" + "=" * 60)
    print("  Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
