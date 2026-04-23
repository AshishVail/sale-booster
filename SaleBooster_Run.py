import requests
import time
import Store_Config as config
import Booster_Logic as logic

def start_process():
    print("🚀 Cleaning duplicates and boosting store...")
    
    endpoint = f"https://{config.STORE_NAME}.myshopify.com/admin/api/{config.API_VERSION}/products.json"
    headers = {
        "X-Shopify-Access-Token": config.ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(endpoint, headers=headers)
        if response.status_code != 200:
            print("❌ Connection Error.")
            return

        products = response.json().get('products', [])
        
        for p in products:
            p_id = p['id']
            stock = p['variants'][0].get('inventory_quantity', 0)
            
            # 1. Clean Title
            new_title = logic.get_seo_title(p['title'])
            
            # 2. Get Fresh Marketing Box
            new_box = logic.get_marketing_html(stock)
            
            # 3. Clean Description (पुराने फालतू बॉक्स को हटाना)
            current_body = p.get('body_html', '')
            
            # अगर पहले से बॉक्स मौजूद है, तो उसे काटकर सिर्फ असली प्रोडक्ट जानकारी बचाना
            if "<div" in current_body and "viewing" in current_body:
                # यह पुराने कोड द्वारा बनाए गए सभी 'div' बॉक्स को साफ कर देगा
                parts = current_body.split("</div>")
                # आखिरी हिस्से में असली डिस्क्रिप्शन होता है
                clean_description = parts[-1].strip()
            else:
                clean_description = current_body

            # 4. Final Payload (सिर्फ एक बॉक्स + असली जानकारी)
            payload = {
                "product": {
                    "id": p_id,
                    "title": new_title,
                    "body_html": new_box + clean_description
                }
            }
            
            put_url = f"https://{config.STORE_NAME}.myshopify.com/admin/api/{config.API_VERSION}/products/{p_id}.json"
            requests.put(put_url, json=payload, headers=headers)
            print(f"✅ Fixed & Boosted: {new_title}")
            time.sleep(0.5)

        print("\n🚀 All cleaned up! Now check your store.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    start_process()
