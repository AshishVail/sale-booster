from flask import Flask, request, redirect, jsonify
import requests
import sqlite3

app = Flask(__name__)

# --- App Configuration ---
# Use your actual credentials from the Shopify Partner Dashboard
CLIENT_ID = "YOUR_CLIENT_ID_HERE"
CLIENT_SECRET = "YOUR_CLIENT_SECRET_HERE"
SCOPES = "read_products,write_products"

# Your Cloudflare URL
REDIRECT_URI = "https://pubmed-jackets-possess-not.trycloudflare.com/auth/callback"

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

    # Exchange authorization code for permanent access token
    token_url = f"https://{shop}/admin/oauth/access_token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code
    }
    
    response = requests.post(token_url, json=payload)
    token_data = response.json()
    access_token = token_data.get('access_token')

    if access_token:
        # Save shop details in the database
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute("INSERT OR REPLACE INTO shops VALUES (?, ?)", (shop, access_token))
        connection.commit()
        connection.close()
        return "App Installed Successfully! Your store optimization is now active."
    
    return "Error: Failed to retrieve access token", 500

if __name__ == '__main__':
    init_db()
    # Running on port 8080 for tunnel compatibility
    app.run(host='0.0.0.0', port=8080)
