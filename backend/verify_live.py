import requests
import json

BASE_URL = "https://stkl.vercel.app"

def test_live():
    print(f"Testing {BASE_URL}...")
    
    # 1. Health Check
    try:
        resp = requests.get(f"{BASE_URL}/api/health", timeout=10)
        print(f"Health Check: {resp.status_code}")
        print(resp.text)
    except Exception as e:
        print(f"Health Check Failed: {e}")

    # 2. Search Check (Wikipedia Fallback)
    try:
        print("\nTesting Search (Elon Musk)...")
        resp = requests.post(
            f"{BASE_URL}/api/search", 
            json={"name": "Elon Musk", "extra_info": ""},
            timeout=30
        )
        print(f"Search Status: {resp.status_code}")
        data = resp.json()
        if "results" in data and len(data["results"]) > 0:
            print("SUCCESS: Found results!")
            print(f"Source: {data['results'][0].get('source')}")
            print(f"Title: {data['results'][0].get('title')}")
        else:
            print("FAILURE: No results found.")
            print(data)
    except Exception as e:
        print(f"Search Failed: {e}")

if __name__ == "__main__":
    test_live()
