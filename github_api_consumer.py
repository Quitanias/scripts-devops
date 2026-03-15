import requests
import sys

url = "https://api.github.com/users/hashicorp/repos"

try:
    # A 5-second timeout is a must in DevOps scripts
    response = requests.get(url, timeout=5)

    # raise_for_status() is a requests shortcut.
    # If the status code is 4XX or 5XX, it raises an exception and jumps to 'except'
    response.raise_for_status()

    data = response.json()

    for item in data:
        # Using .get() safely, in case the 'name' key is missing from the API response
        name = item.get('name', '')
        if 'terraform' in name:
            print(f"Name: {item['name']}")
            print(f"URL: {item['html_url']}")

# Catches any network error (Timeout, bad DNS, HTTP 500, etc.)
except requests.exceptions.RequestException as e:
    print(f"[CRITICAL] Failed to communicate with the GitHub API: {e}")
    sys.exit(1)  # Force the script to fail so the CI/CD pipeline is stopped
