from duckduckgo_search import DDGS

def search_nyma():
    with DDGS() as ddgs:
        print("General Search:")
        res = list(ddgs.text('nyma pharmacy heraklion', max_results=20))
        for r in res:
            print("-", r.get("title"), "\n  ", r.get("href"))
            
        print("\nGreek Search:")
        res = list(ddgs.text('Νύμα Φαρμακείο Ηράκλειο', max_results=20))
        for r in res:
            print("-", r.get("title"), "\n  ", r.get("href"))

if __name__ == "__main__":
    search_nyma()
