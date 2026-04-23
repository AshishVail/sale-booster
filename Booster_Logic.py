import random
import re

def get_seo_title(original_title):
    """
    Cleans old tags and prefixes with [Best Seller] for better conversion.
    """
    # Removes any existing text inside brackets like [Premium], [Top Rated] etc.
    clean_title = re.sub(r'\[.*?\]', '', original_title).strip()
    
    # Removes extra emojis or repeated marketing text to keep it clean
    clean_title = clean_title.replace('🔥', '').replace('HOT SELLING', '').strip()
    
    # Returns the professional SEO title
    return f"[Best Seller] {clean_title}"

def get_marketing_html(inventory):
    """Generates a high-conversion Marketing UI Box for the Product Page"""
    viewers = random.randint(15, 55)
    
    # Dynamic stock messaging
    if inventory < 5:
        status = f"Extremely Low Stock: Only {inventory} left!"
    elif inventory < 15:
        status = f"Limited Edition: {inventory} units remaining!"
    else:
        status = "High Demand: In Stock & Ready to Ship"

    trust_badges = "FREE Express Shipping | Secure Checkout | Quality Guaranteed"

    # Professional HTML Layout
    html_box = f"""
    <div class="sale-booster-box" style="border:2px solid #efefef; padding:15px; border-radius:12px; background:#ffffff; margin-bottom:20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; box-shadow: 0px 4px 6px rgba(0,0,0,0.05);">
        <p style="color:#d90429; font-weight:bold; margin:0; font-size:1.1em;">🔥 {viewers} people are browsing this right now!</p>
        <p style="color:#2b2d42; font-weight:600; margin:12px 0;">📦 {status}</p>
        <div style="border-top:1px solid #eee; padding-top:10px;">
            <p style="color:#457b9d; font-size:0.9em; margin:0; font-weight:500;">✅ {trust_badges}</p>
        </div>
    </div>
    <br>
    """
    return html_box

def get_status_report(count):
    """Generates a summary report after optimization"""
    return f"Success: {count} products have been optimized with the [Best Seller] tag and marketing elements."
