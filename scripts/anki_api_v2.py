import requests
import time


def add_anki_card(
    front_text, back_text, deck_name="default", cookie=None, verbose=False
):
    """
    Add a card to Anki with the specified parameters using the exact format from PowerShell commands

    Args:
        front_text (str): Text for the front of the card
        back_text (str): Text for the back of the card
        deck_name (str): Name of the deck to add the card to. Options include:
            - default
            - test
            - life_tricks
            - ai_facts
            - general_facts
            - it
            - transformers
            - universe
            - words_in_english
            - words_in_romanian
        cookie (str, optional): Authentication cookie. If None, uses the default cookie.
        verbose (bool, optional): If True, prints detailed information about the request.

    Returns:
        dict: A dictionary containing:
            - success (bool): Whether the request was successful
            - status_code (int): HTTP status code
            - message (str): Success or error message
            - response (Response): The full response object
    """
    try:
        # Create the length indicators for front and back text
        if len(front_text) < 128:
            front_len_bytes = bytes([len(front_text)])
        else:
            # For longer text, encode as two bytes
            front_len_bytes = bytes(
                [128 + (len(front_text) % 128), len(front_text) // 128]
            )

        if len(back_text) < 128:
            back_len_bytes = bytes([len(back_text)])
        else:
            # For longer text, encode as two bytes
            back_len_bytes = bytes(
                [128 + (len(back_text) % 128), len(back_text) // 128]
            )

        # First part of the payload with length indicators is the same for all decks
        text_part = (
            bytes([10])
            + front_len_bytes
            + front_text.encode("utf-8")
            + bytes([10])
            + back_len_bytes
            + back_text.encode("utf-8")
        )

        # Binary suffix based on the PowerShell commands for different decks
        if deck_name.lower() == "default":
            binary_suffix = bytes([26, 9, 8, 177, 246, 164, 207, 197, ord("2"), 16, 1])
        elif deck_name.lower() == "test":
            binary_suffix = bytes(
                [
                    26,
                    14,
                    8,
                    177,
                    246,
                    164,
                    207,
                    197,
                    ord("2"),
                    16,
                    200,
                    136,
                    203,
                    146,
                    205,
                    ord("2"),
                ]
            )
        elif deck_name.lower() == "life_tricks":
            binary_suffix = bytes(
                [
                    26,
                    14,
                    8,
                    177,
                    246,
                    164,
                    207,
                    197,
                    ord("2"),
                    16,
                    178,
                    197,
                    246,
                    250,
                    215,
                    ord("2"),
                ]
            )
        elif deck_name.lower() == "ai_facts":
            binary_suffix = bytes(
                [
                    26,
                    14,
                    8,
                    177,
                    246,
                    164,
                    207,
                    197,
                    ord("2"),
                    16,
                    162,
                    192,
                    203,
                    248,
                    209,
                    ord("2"),
                ]
            )
        elif deck_name.lower() == "general_facts":
            binary_suffix = bytes(
                [
                    26,
                    14,
                    8,
                    177,
                    246,
                    164,
                    207,
                    197,
                    ord("2"),
                    16,
                    219,
                    129,
                    138,
                    146,
                    210,
                    ord("2"),
                ]
            )
        elif deck_name.lower() == "it":
            binary_suffix = bytes(
                [
                    26,
                    14,
                    8,
                    177,
                    246,
                    164,
                    207,
                    197,
                    ord("2"),
                    16,
                    255,
                    146,
                    136,
                    170,
                    198,
                    ord("2"),
                ]
            )
        elif deck_name.lower() == "transformers":
            binary_suffix = bytes(
                [
                    26,
                    14,
                    8,
                    177,
                    246,
                    164,
                    207,
                    197,
                    ord("2"),
                    16,
                    193,
                    251,
                    172,
                    215,
                    208,
                    ord("2"),
                ]
            )
        elif deck_name.lower() == "universe":
            binary_suffix = bytes(
                [
                    26,
                    14,
                    8,
                    177,
                    246,
                    164,
                    207,
                    197,
                    ord("2"),
                    16,
                    249,
                    130,
                    170,
                    138,
                    198,
                    ord("2"),
                ]
            )
        elif deck_name.lower() == "words_in_english":
            binary_suffix = bytes(
                [
                    26,
                    14,
                    8,
                    177,
                    246,
                    164,
                    207,
                    197,
                    ord("2"),
                    16,
                    223,
                    204,
                    141,
                    170,
                    198,
                    ord("2"),
                ]
            )
        elif deck_name.lower() == "words_in_romanian":
            binary_suffix = bytes(
                [
                    26,
                    14,
                    8,
                    177,
                    246,
                    164,
                    207,
                    197,
                    ord("2"),
                    16,
                    198,
                    151,
                    176,
                    130,
                    201,
                    ord("2"),
                ]
            )
        else:
            # Use default deck format for unknown decks
            if verbose:
                print(
                    f"Warning: Unknown deck '{deck_name}'. Using default deck format."
                )
            binary_suffix = bytes([26, 9, 8, 177, 246, 164, 207, 197, ord("2"), 16, 1])

        # Construct the full payload
        payload = text_part + binary_suffix

        # Define the AnkiWeb API URL
        url = "https://ankiuser.net/svc/editor/add-or-update"

        # Default cookie if none provided
        if cookie is None:
            cookie = (
                "has_auth=1; ankiweb=eyJvcCI6ImNrIiwiaWF0IjoxNzM2Nzk4ODI1LCJqdiI6MCwiayI6"
                "InZidTxTQ1EqOVFHb34uaTwiLCJjIjoyLCJ0IjoxNzM2Nzk4ODI1fQ.mwUZf4Fym4BWUbMTQFlAeHa-3bq9fOIdxsNl2W1bcEs"
            )

        # Headers
        headers = {
            "Content-Type": "application/octet-stream",
            "Cookie": cookie,
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
            ),
            "Origin": "https://ankiuser.net",
            "Referer": "https://ankiuser.net/add",
        }

        if verbose:
            print(f"Adding card to deck '{deck_name}':")
            print(f"  Front: {front_text}")
            print(f"  Back: {back_text}")
            print(f"  Payload length: {len(payload)} bytes")

        # Send the request
        response = requests.post(url, headers=headers, data=payload)

        # Check if the request was successful
        if response.status_code == 200:
            result = {
                "success": True,
                "status_code": response.status_code,
                "message": f"Card successfully added to deck '{deck_name}'",
                "response": response,
            }
        else:
            result = {
                "success": False,
                "status_code": response.status_code,
                "message": f"Failed to add card. Status code: {response.status_code}",
                "response": response,
            }

        if verbose:
            print(f"  Status Code: {response.status_code}")
            print(f"  Response: {response.text}")

        return result

    except Exception as e:
        # Handle any exceptions
        error_message = f"Error adding card: {str(e)}"
        if verbose:
            print(error_message)

        return {
            "success": False,
            "status_code": None,
            "message": error_message,
            "response": None,
        }


def add_multiple_cards(
    cards, deck_name="default", cookie=None, delay=1.0, verbose=False
):
    """
    Add multiple cards to Anki

    Args:
        cards (list): List of (front, back) tuples
        deck_name (str): Name of the deck to add the cards to
        cookie (str, optional): Authentication cookie
        delay (float, optional): Delay in seconds between requests to avoid rate limiting
        verbose (bool, optional): If True, prints detailed information

    Returns:
        dict: A dictionary containing:
            - total (int): Total number of cards
            - success (int): Number of successfully added cards
            - failed (int): Number of failed cards
            - results (list): List of individual results
    """
    results = []
    success_count = 0

    for i, (front, back) in enumerate(cards):
        if verbose:
            print(f"\nAdding card {i+1}/{len(cards)}:")

        result = add_anki_card(front, back, deck_name, cookie, verbose)
        results.append(result)

        if result["success"]:
            success_count += 1

        # Add delay between requests to avoid rate limiting
        if i < len(cards) - 1 and delay > 0:
            if verbose:
                print(f"Waiting {delay} seconds before next request...")
            time.sleep(delay)

    summary = {
        "total": len(cards),
        "success": success_count,
        "failed": len(cards) - success_count,
        "results": results,
    }

    if verbose:
        print("\nSummary:")
        print(f"  Total cards: {summary['total']}")
        print(f"  Successfully added: {summary['success']}")
        print(f"  Failed: {summary['failed']}")

    return summary


def register_deck_format(deck_name, binary_suffix):
    """
    Register a new deck format for use with add_anki_card

    Args:
        deck_name (str): Name of the deck
        binary_suffix (bytes): Binary suffix for the deck

    Returns:
        bool: True if registration was successful
    """
    # This function would modify a global dictionary of deck formats
    # For now, we'll just print a message
    print(f"To add support for deck '{deck_name}', modify the add_anki_card function")
    print(f"Add an elif block for deck_name.lower() == '{deck_name.lower()}'")
    print(f"with binary_suffix = {binary_suffix}")
    return True


def test_character_limits():
    """
    Test function to check if there are character limits for front and back text

    This function tests various lengths of text to determine if there are any
    limitations in the Anki API for the front and back text of cards.
    """
    print("\nTesting character limits:")

    # Test with exactly 127 characters
    back_text_127 = "A" * 127
    print(f"Testing with 127 characters (len={len(back_text_127)})")
    print(
        f"Encoded as: chr({len(back_text_127)}) = {ord(chr(len(back_text_127)))} (decimal)"
    )
    result_127 = add_anki_card(
        front_text="Test 127 chars",
        back_text=back_text_127,
        deck_name="test",
        verbose=True,
    )
    print(f"Result with 127 chars: {'Success' if result_127['success'] else 'Failed'}")

    # Test with exactly 128 characters
    back_text_128 = "A" * 128
    print(f"Testing with 128 characters (len={len(back_text_128)})")
    print(
        f"Encoded as: chr(128 + {len(back_text_128) % 128}) + chr({len(back_text_128) // 128}) = {ord(chr(128 + (len(back_text_128) % 128)))} and {ord(chr(len(back_text_128) // 128))} (decimal)"
    )
    result_128 = add_anki_card(
        front_text="Test 128 chars",
        back_text=back_text_128,
        deck_name="test",
        verbose=True,
    )
    print(f"Result with 128 chars: {'Success' if result_128['success'] else 'Failed'}")

    # Test with 129 characters
    back_text_129 = "A" * 129
    print(f"Testing with 129 characters (len={len(back_text_129)})")
    print(
        f"Encoded as: chr(128 + {len(back_text_129) % 128}) + chr({len(back_text_129) // 128}) = {ord(chr(128 + (len(back_text_129) % 128)))} and {ord(chr(len(back_text_129) // 128))} (decimal)"
    )
    result_129 = add_anki_card(
        front_text="Test 129 chars",
        back_text=back_text_129,
        deck_name="test",
        verbose=True,
    )
    print(f"Result with 129 chars: {'Success' if result_129['success'] else 'Failed'}")

    # Test with 255 characters
    back_text_255 = "A" * 255
    print(f"Testing with 255 characters (len={len(back_text_255)})")
    print(
        f"Encoded as: chr(128 + {len(back_text_255) % 128}) + chr({len(back_text_255) // 128}) = {ord(chr(128 + (len(back_text_255) % 128)))} and {ord(chr(len(back_text_255) // 128))} (decimal)"
    )
    result_255 = add_anki_card(
        front_text="Test 255 chars",
        back_text=back_text_255,
        deck_name="test",
        verbose=True,
    )
    print(f"Result with 255 chars: {'Success' if result_255['success'] else 'Failed'}")

    # Test with 256 characters
    back_text_256 = "A" * 256
    print(f"Testing with 256 characters (len={len(back_text_256)})")
    print(
        f"Encoded as: chr(128 + {len(back_text_256) % 128}) + chr({len(back_text_256) // 128}) = {ord(chr(128 + (len(back_text_256) % 128)))} and {ord(chr(len(back_text_256) // 128))} (decimal)"
    )
    result_256 = add_anki_card(
        front_text="Test 256 chars",
        back_text=back_text_256,
        deck_name="test",
        verbose=True,
    )
    print(f"Result with 256 chars: {'Success' if result_256['success'] else 'Failed'}")

    # Test with 260 characters
    back_text_260 = "A" * 260
    print(f"Testing with 260 characters (len={len(back_text_260)})")
    print(
        f"Encoded as: chr(128 + {len(back_text_260) % 128}) + chr({len(back_text_260) // 128}) = {ord(chr(128 + (len(back_text_260) % 128)))} and {ord(chr(len(back_text_260) // 128))} (decimal)"
    )
    result_260 = add_anki_card(
        front_text="Test 260 chars",
        back_text=back_text_260,
        deck_name="test",
        verbose=True,
    )
    print(f"Result with 260 chars: {'Success' if result_260['success'] else 'Failed'}")

    return {
        "127_chars": result_127,
        "128_chars": result_128,
        "129_chars": result_129,
        "255_chars": result_255,
        "256_chars": result_256,
        "260_chars": result_260,
    }


# Example usage
if __name__ == "__main__":
    # Example 1: Add a single card
    result = add_anki_card(
        front_text="Example vocabulary",
        back_text="Example definition",
        deck_name="default",
        verbose=True,
    )

    # Example 2: Add multiple cards
    cards = [
        ("Word 1", "Definition 1"),
        ("Word 2", "Definition 2"),
        ("Word 3", "Definition 3"),
    ]

    summary = add_multiple_cards(
        cards=cards,
        deck_name="test",
        delay=1.5,  # 1.5 seconds between requests
        verbose=True,
    )

    # Example 3: Add a card to one of the new decks
    result_new_deck = add_anki_card(
        front_text="AI concept",
        back_text="AI explanation",
        deck_name="ai_facts",
        verbose=True,
    )

    # Example 4: Add cards from a CSV file
    print("\nExample: Adding cards from a CSV file")
    print("To use this functionality, uncomment and modify the code below:")
    """
    import csv

    def add_cards_from_csv(csv_file, deck_name="default", cookie=None, delay=1.0, verbose=False):
        cards = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    front, back = row[0], row[1]
                    cards.append((front, back))

        return add_multiple_cards(cards, deck_name, cookie, delay, verbose)

    # Usage:
    csv_summary = add_cards_from_csv(
        csv_file="vocabulary.csv",
        deck_name="default",
        delay=1.5,
        verbose=True
    )
    """

    # Uncomment to test character limits
    # test_results = test_character_limits()
