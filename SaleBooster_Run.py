import requests
import time
import os
import Store_Config as config
import Booster_Logic as logic

def start_process():
    # Use environment variables for security if they exist, otherwise fallback to config
    store_name = os.environ.get('SHOP_NAME', config.STORE_NAME)
    access_token = os.environ.get('SHOPIFY_ACCESS_TOKEN', config.ACCESS_TOKEN)
    api_version = config.API_VERSION

    print(f"🚀 Initializing Sale Booster for: {store_name}...")
    
    endpoint = f"https://{store_name}.myshopify.com/admin/api/{api_version}/products.json"
    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(endpoint, headers=headers)
        
        # Professional Error Handling
        if response.status_code == 401:
            print("❌ Error: Unauthorized. Please check your Access Token.")
            return
        elif response.status_code != 200:
            print(f"❌ Connection Error: Status Code {response.status_code}")
            return

        products = response.json().get('products', [])
        
        if not products:
            print("ℹ️ No products found in the store to optimize.")
            return

        for p in products:
            p_id = p['id']
            # Safeguard against missing variants or inventory data
            variants = p.get('variants', [])
            stock = variants[0].get('inventory_quantity', 0) if variants else 0
            
            # 1. Generate SEO Optimized Title
            new_title = logic.get_seo_title(p['title'])
            
            # 2. Generate Marketing/Sales UI Element
            new_box = logic.get_marketing_html(stock)
            
            # 3. Clean Description (Removing legacy clutter)
            current_body = p.get('body_html', '') or ''
            
            # Smart cleaning logic to prevent duplicate marketing boxes
            if "<div" in current_body and "viewing" in current_body:
                parts = current_body.split("</div>")
                clean_description = parts[-1].strip()
            else:
                clean_description = current_body

            # 4. Final Update Payload
            payload = {
                "product": {
                    "id": p_id,
                    "title": new_title,
                    "body_html": f"{new_box}\n{clean_description}"
                }
            }
            
            put_url = f"https://{store_name}.myshopify.com/admin/api/{api_version}/products/{p_id}.json"
            update_res = requests.put(put_url, json=payload, headers=headers)
            
            if update_res.status_code == 200:
                print(f"✅ Optimized: {new_title}")
            else:
                print(f"⚠️ Failed to update: {p['title']}")
                
            # Respect Shopify API Rate Limits
            time.sleep(0.5)

        print("\n🚀 Optimization Complete! Your store is now boosted.")

    except Exception as e:
        print(f"❌ Critical System Error: {e}")

if __name__ == "__main__":
    start_process()
