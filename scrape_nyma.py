import asyncio
from playwright.async_api import async_playwright
import json
import re

async def main():
    results = {
        "images": [],
        "social": [],
        "wolt_link": None
    }
    
    try:
        async with async_playwright() as p:
            print("Launching browser...")
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            url = "https://www.google.com/search?q=nyma+pharmacy+%CE%B7%CF%81%CE%B1%CE%BA%CE%BB%CE%B5%CE%B9%CE%BF"
            print(f"Navigating to {url} ...")
            await page.goto(url, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            
            # Click reject all / accept all if cookie popup is there
            try:
                btns = await page.locator('button').all()
                for btn in btns:
                    text = await btn.inner_text()
                    if text and ('Απόρριψη' in text or 'Reject' in text):
                        await btn.click()
                        await page.wait_for_timeout(1000)
                        break
            except:
                pass

            print("Extracting links from Google...")
            links = await page.locator("a").all()
            for link in links:
                href = await link.get_attribute("href")
                if not href: continue
                # Google wraps links in /url?q=...
                actual_href = href
                if href.startswith("/url?"):
                    try:
                        actual_href = href.split("q=")[1].split("&")[0]
                    except:
                        pass
                        
                if "instagram.com" in actual_href or "facebook.com" in actual_href:
                    if "google" not in actual_href and actual_href not in results["social"]:
                        results["social"].append(actual_href)
                        print(f"Found Social Link: {actual_href}")
                        
                if "wolt.com" in actual_href and "nyma" in actual_href:
                    results["wolt_link"] = actual_href
                    print(f"Found Wolt Link: {actual_href}")
            
            # Extract image from Google Business Profile
            print("Extracting images from Google Maps profile...")
            imgs = await page.locator("g-img img, img[alt*='Nyma'], img[alt*='φαρμακείο']").all()
            for img in imgs:
                src = await img.get_attribute("src")
                if src and src.startswith("http"):
                    if src not in results["images"]:
                        results["images"].append(src)
                        print(f"Found Maps Image: {src}")

            if results["wolt_link"]:
                print(f"Navigating to Wolt: {results['wolt_link']}")
                try:
                    await page.goto(results["wolt_link"], wait_until="domcontentloaded")
                    await page.wait_for_timeout(3000)
                    imgs = await page.locator("img").all()
                    for img in imgs:
                        src = await img.get_attribute("src")
                        if not src: continue
                        if "brand" in src.lower() or "logo" in src.lower() or "venue" in src.lower():
                            if src not in results["images"]:
                                results["images"].append(src)
                                print(f"Found Wolt Image: {src}")
                except Exception as e:
                    print(f"Error on Wolt: {e}")
                    
            await browser.close()
            
    except Exception as e:
        print(f"Script Error: {e}")
            
    with open("scraped_assets.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    print("Done. Results saved to scraped_assets.json")

if __name__ == "__main__":
    asyncio.run(main())
