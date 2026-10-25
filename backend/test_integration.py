import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("Running Integration Tests...")

    # 1. Register a new user
    print("Testing Registration...")
    res = requests.post(f"{BASE_URL}/register", json={
        "email": "testuser@example.com",
        "full_name": "Integration Test User",
        "password": "securepassword123"
    })

    if res.status_code == 400: # Already registered
        print("User already registered, moving on...")
    else:
        assert res.status_code == 200
        print("Registration successful.")

    # 2. Login
    print("Testing Login...")
    res = requests.post(f"{BASE_URL}/token", data={
        "username": "testuser@example.com",
        "password": "securepassword123"
    })
    assert res.status_code == 200
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Login successful.")

    # 3. Create Listing
    print("Testing Create Listing...")
    listing_data = {
        "title": "Drill Machine",
        "description": "Powerful 18V cordless drill.",
        "category": "Tools",
        "condition": "Excellent",
        "daily_rate": 15.0,
        "deposit": 50.0,
        "pickup_location": "Gujrat City"
    }
    res = requests.post(f"{BASE_URL}/listings", json=listing_data, headers=headers)
    assert res.status_code == 200
    listing = res.json()
    listing_id = listing["id"]
    print("Listing created successfully.")

    # 4. Search Listings
    print("Testing Search...")
    res = requests.get(f"{BASE_URL}/listings?search=Drill")
    assert res.status_code == 200
    assert len(res.json()) > 0
    print("Search successful.")

    # 5. Create Booking
    print("Testing Booking...")
    booking_data = {
        "listing_id": listing_id,
        "start_date": "2026-11-01T10:00:00",
        "end_date": "2026-11-03T10:00:00"
    }
    res = requests.post(f"{BASE_URL}/bookings", json=booking_data, headers=headers)
    assert res.status_code == 200
    booking = res.json()
    booking_id = booking["id"]
    total_amount = booking["total_amount"]
    print(f"Booking created successfully. Total amount: {total_amount}")

    # 6. Mock Payment Sandbox
    print("Testing Payment...")
    payment_data = {
        "amount": total_amount,
        "provider_token": "test_token_999"
    }
    res = requests.post(f"{BASE_URL}/bookings/{booking_id}/pay", json=payment_data, headers=headers)
    assert res.status_code == 200
    print("Payment completed successfully.")

    print("All integration tests passed!")

if __name__ == "__main__":
    run_tests()
