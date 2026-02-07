import logging
import requests
from googlesearch import search as gsearch

def test_connectivity():
    print("Testing Network Connectivity...")
    try:
        r = requests.get("https://www.google.com", timeout=5)
        print(f"Google Status Code: {r.status_code}")
    except Exception as e:
        print(f"Google Connection Failed: {e}")

    print("\nTesting 'googlesearch' (Simple Mode)...")
    try:
        # Simple search returns generator of strings (URLs)
        results = list(gsearch("Elon Musk", num_results=5, advanced=False))
        if results:
            print(f"✅ Google Simple returned {len(results)} URLs:")
            for url in results:
                print(f"  - {url}")
        else:
            print("❌ Google Simple returned 0 results.")
    except Exception as e:
        print(f"❌ Google Simple Failed: {e}")

if __name__ == "__main__":
    test_connectivity()
