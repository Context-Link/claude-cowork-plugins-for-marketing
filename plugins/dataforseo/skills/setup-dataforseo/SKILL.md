---
name: setup-dataforseo
description: Set up DataForSEO API credentials for accessing SEO, SERP, backlinks, and keyword data APIs
---

# DataForSEO API Setup

This skill helps you configure your DataForSEO API credentials so you can use all the DataForSEO analysis tools.

## Getting Your API Credentials

1. Go to https://app.dataforseo.com/ and sign up or log in
2. Navigate to your API credentials section in the dashboard
3. Your **API Login** is your registered email address
4. Your **API Password** is generated in the dashboard (not your account password)

## Setup Instructions

Once you have your credentials, provide them and I will verify and save them securely.

**Required information:**
- API Login (your registered email)
- API Password (from the dashboard)

## What Happens During Setup

1. Your credentials are verified against the DataForSEO API
2. If valid, they are saved to `~/.dataforseo_config.json` with secure permissions (600)
3. All other DataForSEO skills will use these stored credentials automatically

## Verification Script

```python
import sys, os
skill_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else os.getcwd()
sys.path.insert(0, os.path.join(skill_dir, '..', '..', 'scripts'))
from dataforseo_client import save_credentials, verify_credentials, get_user_data

# Replace with actual credentials provided by user
login = "YOUR_API_LOGIN"
password = "YOUR_API_PASSWORD"

print("Verifying DataForSEO credentials...")
if verify_credentials(login, password):
    save_credentials(login, password)
    print("Credentials verified and saved successfully!")

    # Show account info
    user_data = get_user_data()
    if user_data.get("status_code") == 20000:
        result = user_data["tasks"][0]["result"][0]
        print(f"\nAccount Details:")
        print(f"  Login: {result.get('login')}")
        print(f"  Timezone: {result.get('timezone')}")
else:
    print("ERROR: Invalid credentials. Please check your API login and password.")
    print("Get credentials at: https://app.dataforseo.com/")
```

## Test Connection

After setup, verify the connection works:

```python
import sys, os
skill_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else os.getcwd()
sys.path.insert(0, os.path.join(skill_dir, '..', '..', 'scripts'))
from dataforseo_client import get_user_data

response = get_user_data()
if response.get("status_code") == 20000:
    result = response["tasks"][0]["result"][0]
    print("Connection successful!")
    print(f"  Logged in as: {result.get('login')}")
    print(f"  Timezone: {result.get('timezone')}")
else:
    print(f"Connection failed: {response.get('status_message', 'Unknown error')}")
```

## Troubleshooting

- **Invalid credentials**: Double-check you're using the API password from the dashboard, not your account login password
- **Connection errors**: Ensure you have internet connectivity
- **File permission errors**: The config file requires write access to your home directory

## Security Notes

- Credentials are stored locally at `~/.dataforseo_config.json`
- File permissions are set to 600 (owner read/write only)
- Never share your API password or config file
