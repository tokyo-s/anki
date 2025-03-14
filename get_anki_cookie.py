#!/usr/bin/env python3
"""
Script to help users extract their Anki cookie from a browser cookie file.
This script supports Chrome, Firefox, and Edge browsers.
"""

import os
import sqlite3
import argparse
import platform
import shutil

try:
    import browser_cookie3

    BROWSER_COOKIE3_AVAILABLE = True
except ImportError:
    BROWSER_COOKIE3_AVAILABLE = False


def get_chrome_cookie_path():
    """Get the path to the Chrome cookies file based on the operating system."""
    system = platform.system()
    if system == "Windows":
        return os.path.join(
            os.environ["LOCALAPPDATA"],
            "Google",
            "Chrome",
            "User Data",
            "Default",
            "Network",
            "Cookies",
        )
    elif system == "Darwin":  # macOS
        return os.path.join(
            os.path.expanduser("~"),
            "Library",
            "Application Support",
            "Google",
            "Chrome",
            "Default",
            "Cookies",
        )
    elif system == "Linux":
        return os.path.join(
            os.path.expanduser("~"), ".config", "google-chrome", "Default", "Cookies"
        )
    else:
        return None


def get_firefox_cookie_path():
    """Get the path to the Firefox cookies file based on the operating system."""
    system = platform.system()
    if system == "Windows":
        profile_path = os.path.join(
            os.environ["APPDATA"], "Mozilla", "Firefox", "Profiles"
        )
    elif system == "Darwin":  # macOS
        profile_path = os.path.join(
            os.path.expanduser("~"),
            "Library",
            "Application Support",
            "Firefox",
            "Profiles",
        )
    elif system == "Linux":
        profile_path = os.path.join(os.path.expanduser("~"), ".mozilla", "firefox")
    else:
        return None

    # Find the default profile
    if os.path.exists(profile_path):
        for folder in os.listdir(profile_path):
            if folder.endswith(".default") or "default" in folder:
                return os.path.join(profile_path, folder, "cookies.sqlite")

    return None


def get_edge_cookie_path():
    """Get the path to the Edge cookies file based on the operating system."""
    system = platform.system()
    if system == "Windows":
        return os.path.join(
            os.environ["LOCALAPPDATA"],
            "Microsoft",
            "Edge",
            "User Data",
            "Default",
            "Network",
            "Cookies",
        )
    elif system == "Darwin":  # macOS
        return os.path.join(
            os.path.expanduser("~"),
            "Library",
            "Application Support",
            "Microsoft Edge",
            "Default",
            "Cookies",
        )
    elif system == "Linux":
        return os.path.join(
            os.path.expanduser("~"), ".config", "microsoft-edge", "Default", "Cookies"
        )
    else:
        return None


def extract_anki_cookie_manual(browser="chrome"):
    """Extract the Anki cookie from the browser's cookie database."""
    cookie_path = None

    if browser.lower() == "chrome":
        cookie_path = get_chrome_cookie_path()
    elif browser.lower() == "firefox":
        cookie_path = get_firefox_cookie_path()
    elif browser.lower() == "edge":
        cookie_path = get_edge_cookie_path()

    if not cookie_path or not os.path.exists(cookie_path):
        print(f"Could not find cookie file for {browser}.")
        return None

    # Create a temporary copy of the cookie file (since it might be locked by the browser)
    temp_cookie_path = f"{cookie_path}.temp"
    try:
        shutil.copy2(cookie_path, temp_cookie_path)

        conn = sqlite3.connect(temp_cookie_path)
        cursor = conn.cursor()

        # Different query for Firefox vs Chrome/Edge
        if browser.lower() == "firefox":
            cursor.execute(
                "SELECT name, value FROM moz_cookies WHERE host LIKE '%ankiweb.net%' OR host LIKE '%ankiuser.net%'"
            )
        else:
            cursor.execute(
                "SELECT name, value, encrypted_value FROM cookies WHERE host_key LIKE '%ankiweb.net%' OR host_key LIKE '%ankiuser.net%'"
            )

        cookies = cursor.fetchall()
        conn.close()

        # Clean up the temporary file
        os.remove(temp_cookie_path)

        if not cookies:
            print(
                f"No Anki cookies found in {browser}. Please make sure you're logged into AnkiWeb."
            )
            return None

        # Format the cookies
        cookie_str = ""
        for cookie in cookies:
            if browser.lower() == "firefox":
                name, value = cookie
                cookie_str += f"{name}={value}; "
            else:
                name, value, encrypted_value = cookie
                # Chrome/Edge store cookies encrypted, we can only get the names here
                cookie_str += f"{name}=<encrypted>; "

        return cookie_str.strip("; ")

    except Exception as e:
        print(f"Error extracting cookies: {e}")
        if os.path.exists(temp_cookie_path):
            os.remove(temp_cookie_path)
        return None


def extract_anki_cookie_browser_cookie3(browser="chrome"):
    """Extract the Anki cookie using the browser_cookie3 library."""
    if not BROWSER_COOKIE3_AVAILABLE:
        print(
            "browser_cookie3 library not available. Please install it with: pip install browser-cookie3"
        )
        return None

    try:
        if browser.lower() == "chrome":
            cookies = browser_cookie3.chrome(domain_name=".ankiweb.net")
        elif browser.lower() == "firefox":
            cookies = browser_cookie3.firefox(domain_name=".ankiweb.net")
        elif browser.lower() == "edge":
            cookies = browser_cookie3.edge(domain_name=".ankiweb.net")
        else:
            print(f"Unsupported browser: {browser}")
            return None

        cookie_str = ""
        for cookie in cookies:
            cookie_str += f"{cookie.name}={cookie.value}; "

        # Also try ankiuser.net domain
        if browser.lower() == "chrome":
            cookies = browser_cookie3.chrome(domain_name=".ankiuser.net")
        elif browser.lower() == "firefox":
            cookies = browser_cookie3.firefox(domain_name=".ankiuser.net")
        elif browser.lower() == "edge":
            cookies = browser_cookie3.edge(domain_name=".ankiuser.net")

        for cookie in cookies:
            cookie_str += f"{cookie.name}={cookie.value}; "

        return cookie_str.strip("; ")

    except Exception as e:
        print(f"Error extracting cookies with browser_cookie3: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Extract Anki cookie from browser")
    parser.add_argument(
        "--browser",
        choices=["chrome", "firefox", "edge"],
        default="chrome",
        help="Browser to extract cookie from",
    )
    parser.add_argument(
        "--method",
        choices=["auto", "manual"],
        default="auto",
        help="Method to extract cookie",
    )
    parser.add_argument("--output", help="Output file to save the cookie to")

    args = parser.parse_args()

    print(f"Extracting Anki cookie from {args.browser}...")

    cookie = None
    if args.method == "auto" and BROWSER_COOKIE3_AVAILABLE:
        cookie = extract_anki_cookie_browser_cookie3(args.browser)

    if cookie is None:
        print("Falling back to manual extraction method...")
        cookie = extract_anki_cookie_manual(args.browser)

    if cookie:
        print("\nFound Anki cookie:")
        print(cookie)

        if args.output:
            with open(args.output, "w") as f:
                f.write(f'ANKI_COOKIE="{cookie}"')
            print(f"\nCookie saved to {args.output}")

        print("\nTo use this cookie in your .env file:")
        print(f'ANKI_COOKIE="{cookie}"')
    else:
        print(
            "\nCould not extract Anki cookie. Please make sure you're logged into AnkiWeb."
        )
        print("You can manually extract the cookie using browser developer tools:")
        print("1. Open your browser and go to https://ankiweb.net")
        print("2. Log in to your account")
        print("3. Open developer tools (F12 or Ctrl+Shift+I)")
        print("4. Go to the 'Application' or 'Storage' tab")
        print("5. Look for 'Cookies' in the sidebar and find the 'ankiweb' cookie")
        print("6. Copy the value and use it in your .env file")


if __name__ == "__main__":
    main()
