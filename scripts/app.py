#!/usr/bin/env python3
"""
Simple script to run the Anki API server.
This script checks if the required dependencies are installed and if the .env file exists.
"""

import os
import sys
import subprocess
import importlib.util


def check_dependency(package):
    """Check if a Python package is installed."""
    return importlib.util.find_spec(package) is not None


def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = ["fastapi", "uvicorn", "pydantic", "dotenv", "requests"]
    missing_packages = []

    for package in required_packages:
        if not check_dependency(package):
            missing_packages.append(package)

    if missing_packages:
        print("The following required packages are missing:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nPlease install them using:")
        print("pip install -r requirements.txt")
        return False

    return True


def check_env_file():
    """Check if the .env file exists and contains the ANKI_COOKIE variable."""
    if not os.path.exists(".env"):
        print("The .env file does not exist.")
        print("Please create a .env file with your Anki cookie.")
        print("You can use the .env.example file as a template:")
        print("cp .env.example .env")
        print("\nOr run the get_anki_cookie.py script to extract your cookie:")
        print("python get_anki_cookie.py --output .env")
        return False

    with open(".env", "r") as f:
        env_content = f.read()

    if "ANKI_COOKIE" not in env_content:
        print("The .env file does not contain the ANKI_COOKIE variable.")
        print("Please add your Anki cookie to the .env file.")
        print("You can use the get_anki_cookie.py script to extract your cookie:")
        print("python get_anki_cookie.py --output .env")
        return False

    return True


def run_server():
    """Run the FastAPI server."""
    print("Starting Anki API server...")

    # Get the port from the .env file or use the default
    port = os.environ.get("PORT", "8000")

    # Run the server
    subprocess.run(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "anki_fastapi:app",
            "--host",
            "0.0.0.0",
            "--port",
            port,
            "--reload",
        ]
    )


def main():
    """Main function."""
    print("Anki API Server")
    print("==============")

    # Check dependencies
    if not check_dependencies():
        return

    # Check .env file
    if not check_env_file():
        return

    # Run the server
    run_server()


if __name__ == "__main__":
    main()
