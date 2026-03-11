import requests
from bs4 import BeautifulSoup
import json
import urllib.request
import os

def check_direct_links():
    results = {"wolt_images": [], "social": []}
    
    # Check Wolt
    wolt_url = "https://wolt.com/en/grc/heraklion/venue/nyma-pharmacy"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
    
    try:
        r = requests.get(wolt_url, headers=headers)
        if r.status_code == 200:
            print("Wolt page found!")
            soup = BeautifulSoup(r.text, 'html.parser')
            # Look for venue hero image and logo
            for img in soup.find_all('img'):
                src = img.get('src')
                if src and ('brand' in src or 'venue' in src or 'logo' in src):
                    if src not in results["wolt_images"]:
                        results["wolt_images"].append(src)
                        print(f"Found Wolt image: {src}")
    except Exception as e:
        print("Wolt error:", e)
        
    # Check Instagram handles
    handles = ["nyma_pharmacy", "nymapharmacy", "to_nyma_pharmacy", "tonyma", "nyma.pharmacy"]
    for h in handles:
        try:
            url = f"https://www.instagram.com/{h}/"
            r = requests.get(url, headers=headers)
            if r.status_code == 200 and "Page Not Found" not in r.text and "<title>Instagram</title>" not in r.text:
                # Need a crude content check because IG returns 200 with a login page sometimes
                if h in r.text.lower():
                    results["social"].append(url)
                    print(f"Possible IG found: {url}")
        except: pass
        
    # Check Facebook handles
    for h in handles:
        try:
            url = f"https://www.facebook.com/{h}/"
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                results["social"].append(url)
                print(f"Possible FB found: {url}")
        except: pass

    with open("direct_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    check_direct_links()
