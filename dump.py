import asyncio
from playwright.async_api import async_playwright
import re

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Use an actual user agent
        page = await browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        url = "https://www.google.com/search?q=nyma+pharmacy+heraklion"
        print(f"Going to {url} ...")
        await page.goto(url, wait_until="networkidle")
        
        html = await page.content()
        print("Page loaded. Extracting links...")
        
        # Regex for all https links
        urls = re.findall(r'https?://[^\s"\'<>]+', html)
        
        # Filter URLs
        interesting = set()
        for u in urls:
            u_lower = u.lower()
            if "facebook.com" in u_lower or "instagram.com" in u_lower or "wolt.com" in u_lower or "omikron" in u_lower:
                if "js" not in u_lower and "css" not in u_lower and "google" not in u_lower:
                    interesting.add(u)
                    
        print("\nFound interesting URLs:")
        for u in interesting:
            print("-", u)
            
        with open("raw_html.txt", "w", encoding="utf-8") as f:
            f.write(html)
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
