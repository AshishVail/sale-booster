from flask import Flask, request, redirect, jsonify
import requests
import sqlite3
import os

app = Flask(__name__)

# --- Secure App Configuration ---
# Keys are now fetched from Environment Variables for maximum security
# When you or a client deploys this, they will set these keys in the server settings
CLIENT_ID = os.environ.get('SHOPIFY_API_KEY')
CLIENT_SECRET = os.environ.get('SHOPIFY_API_SECRET')
SCOPES = "read_products,write_products"

# The Host URL will be automatically set by the server (Render/VPS)
HOST_URL = os.environ.get('HOST') 
REDIRECT_URI = f"{HOST_URL}/auth/callback"

# --- Database Initialization ---
def init_db():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS shops 
                      (shop_url TEXT PRIMARY KEY, access_token TEXT)''')
    connection.commit()
    connection.close()

# --- Routes ---

@app.route('/install')
def install():
    shop = request.args.get('shop')
    if shop:
        # Generate the Shopify Installation URL
        install_url = (
            f"https://{shop}/admin/oauth/authorize?"
            f"client_id={CLIENT_ID}&"
            f"scope={SCOPES}&"
            f"redirect_uri={REDIRECT_URI}"
        )
        return redirect(install_url)
    return "Error: Missing shop parameter", 400

@app.route('/auth/callback')
def callback():
    shop = request.args.get('shop')
    code = request.args.get('code')
    
    if not shop or not code:
        return "Error: Invalid request parameters", 400

    # Exchange authorization code for a permanent access token
    token_url = f"https://{shop}/admin/oauth/access_token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code
    }
    
    try:
        response = requests.post(token_url, json=payload)
        token_data = response.json()
        access_token = token_data.get('access_token')

        if access_token:
            # Securely save the shop URL and token for future API calls
            connection = sqlite3.connect('users.db')
            cursor = connection.cursor()
            cursor.execute("INSERT OR REPLACE INTO shops VALUES (?, ?)", (shop, access_token))
            connection.commit()
            connection.close()
            return "Installation Successful! Your store is now being optimized by Sale Booster."
        
    except Exception as e:
        return f"Installation Error: {str(e)}", 500
    
    return "Error: Failed to retrieve access token", 500

if __name__ == '__main__':
    init_db()
    # Port 8080 is standard for many cloud hosting providers
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
