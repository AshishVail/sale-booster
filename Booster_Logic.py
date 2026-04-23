import random
import re

def get_seo_title(original_title):
    """
    Cleans old tags and adds only [Best Seller]
    """
    # This line removes any existing text inside brackets like [Premium], [Top Rated] etc.
    clean_title = re.sub(r'\[.*?\]', '', original_title).strip()
    
    # This removes extra emojis or repeated 'HOT SELLING' text if any
    clean_title = clean_title.replace('🔥', '').replace('HOT SELLING', '').strip()
    
    # Adding ONLY the Best Seller tag as requested
    return f"[Best Seller] {clean_title}"

def get_marketing_html(inventory):
    """Generates a clean Marketing Box"""
    viewers = random.randint(15, 55)
    status = f"Urgent: Only {inventory} units left!" if inventory < 10 else "In Stock: Ready to Ship"
    trust_badges = "FREE Global Shipping | 7-Day Money Back Guarantee"

    html_box = f"""
    <div style="border:1px solid #ddd; padding:15px; border-radius:10px; background:#f9f9f9; margin-bottom:25px; font-family:Arial, sans-serif;">
        <p style="color:#e63946; font-weight:bold; margin:0;">🔥 {viewers} customers are viewing this product!</p>
        <p style="color:#1d3557; font-weight:bold; margin:10px 0;">📦 {status}</p>
        <p style="color:#2a9d8f; font-size:0.85em; margin:0;">⭐ {trust_badges}</p>
    </div>
    <br>
    """
    return html_box

def get_status_report(count):
    return f"Optimization Finished: {count} products updated with [Best Seller] tag."
