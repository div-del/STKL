from duckduckgo_search import DDGS
import json

def test_search():
    print("Testing DDGS...")
    try:
        with DDGS() as ddgs:
            # Test default (no backend arg)
            print("1. Testing default backend...")
            results = list(ddgs.text("python programming", max_results=3))
            print(f"   Success! Found {len(results)} results.")
            if results:
                print(f"   Sample: {results[0]['title']}")

            # Test 'html' backend (used in code)
            print("\n2. Testing 'html' backend param...")
            try:
                results_html = list(ddgs.text("python programming", max_results=3, backend='html'))
                print(f"   Success! Found {len(results_html)} results.")
            except Exception as e:
                print(f"   Failed: {e}")

    except Exception as eq:
        print(f"CRITICAL FAILURE: {eq}")

if __name__ == "__main__":
    test_search()
