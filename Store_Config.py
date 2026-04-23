import os

# --- Secure Configuration ---
# We use os.environ.get to fetch sensitive data from the server environment.
# This keeps your access token and store name hidden from the source code.

STORE_NAME = os.environ.get('SHOP_NAME', 'your-default-store-name')
ACCESS_TOKEN = os.environ.get('SHOPIFY_ACCESS_TOKEN')
API_VERSION = "2024-04"

# Only print if keys are present to avoid errors
if ACCESS_TOKEN:
    print(f"--- SaleBooster Config for {STORE_NAME} Loaded Successfully ---")
else:
    print("--- Error: Access Token Missing! Please set environment variables. ---")
