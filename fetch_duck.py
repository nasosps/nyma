import requests
from bs4 import BeautifulSoup
import json

def fetch_links():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    results = {"wolt": None, "facebook": None, "instagram": None, "omikron": None}
    
    # query 1
    url = "https://html.duckduckgo.com/html/?q=nyma+pharmacy+heraklion"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    for a in soup.find_all('a', class_='result__url'):
        href = a.get('href', '').lower()
        if "wolt.com" in href and "nyma" in href: results["wolt"] = a.get('href')
        elif "facebook.com" in href: results["facebook"] = a.get('href')
        elif "instagram.com" in href: results["instagram"] = a.get('href')
        elif "omikron" in href: results["omikron"] = a.get('href')
        
    print("Links found:", json.dumps(results, indent=2))
    
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f)

if __name__ == "__main__":
    fetch_links()
