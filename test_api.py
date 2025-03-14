import requests

# Base URL of the API
BASE_URL = "http://localhost:8000"


def test_health():
    """Test the health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code}")
    print(response.json())
    print("-" * 40)
    return response.status_code == 200


def test_decks():
    """Test the decks endpoint"""
    response = requests.get(f"{BASE_URL}/decks")
    print(f"List decks: {response.status_code}")
    print(response.json())
    print("-" * 40)
    return response.status_code == 200


def test_add_card():
    """Test adding a single card"""
    payload = {
        "front": "API Test Card",
        "back": "This card was added via the API",
        "deck_name": "default",
    }

    response = requests.post(f"{BASE_URL}/add-card", json=payload)

    print(f"Add card: {response.status_code}")
    print(response.json() if response.status_code == 200 else response.text)
    print("-" * 40)
    return response.status_code == 200


def test_add_multiple_cards():
    """Test adding multiple cards"""
    payload = {
        "cards": [
            {"front": "API Test Card 1", "back": "This is test card 1"},
            {"front": "API Test Card 2", "back": "This is test card 2"},
        ],
        "deck_name": "default",
        "delay": 1.0,
    }

    response = requests.post(f"{BASE_URL}/add-multiple-cards", json=payload)

    print(f"Add multiple cards: {response.status_code}")
    print(response.json() if response.status_code == 200 else response.text)
    print("-" * 40)
    return response.status_code == 200


def run_all_tests():
    """Run all tests and return the results"""
    results = {
        "health": test_health(),
        "decks": test_decks(),
        "add_card": test_add_card(),
        "add_multiple_cards": test_add_multiple_cards(),
    }

    print("\nTest Results:")
    for test, result in results.items():
        print(f"{test}: {'PASS' if result else 'FAIL'}")

    return all(results.values())


if __name__ == "__main__":
    print("Running API tests...\n")
    success = run_all_tests()
    print(f"\nOverall result: {'PASS' if success else 'FAIL'}")
