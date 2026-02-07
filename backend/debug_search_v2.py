import logging
import time
from duckduckgo_search import DDGS
from googlesearch import search as gsearch
import re

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_search_logic(query, required_terms):
    print(f"\n--- Testing Query: '{query}' ---")
    raw_results = []

    # 1. Test DuckDuckGo
    print("Testing DuckDuckGo...")
    for backend in ['api', 'html', 'lite']:
        print(f"  Testing DDG Backend: {backend}")
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5, backend=backend))
                if results:
                    print(f"  ✅ DDG ({backend}) returned {len(results)} results.")
                    for r in results:
                        raw_results.append({
                            "title": r.get('title', ''),
                            "url": r.get('href', ''),
                            "description": r.get('body', ''),
                            "source": f"DDG-{backend}"
                        })
                    break # Stop if we found results
                else:
                    print(f"  ❌ DDG ({backend}) returned 0 results.")
        except Exception as e:
            print(f"  ❌ DDG ({backend}) Failed: {e}")

    # 2. Test Google Fallback
    if not raw_results:
        print("\nTesting Google Search Fallback...")
        try:
            # Try without strict constraints first
            results = list(gsearch(query, num_results=5, advanced=True))
            if results:
                print(f"✅ Google returned {len(results)} results.")
                for r in results:
                    raw_results.append({
                        "title": r.title,
                        "url": r.url,
                        "description": r.description,
                        "source": "Google"
                    })
            else:
                print("❌ Google returned 0 results.")
        except Exception as e:
            print(f"❌ Google Failed: {e}")

    # 3. Test Filtering Logic
    print("\nTesting Filtering Logic...")
    processed_results = []
    
    for r in raw_results:
        title = r['title']
        body = r['description']
        url = r['url']
        combined_text = f"{title} {body} {url}"
        
        print(f"Checking Result: {title[:30]}...")
        
        match_found = False
        if required_terms:
            clean_terms = [t.replace('"', '').strip() for t in required_terms if t]
            
            for term in clean_terms:
                sub_words = term.split()
                if not sub_words: continue
                
                matched_words = []
                for word in sub_words:
                    if len(word) < 3: continue
                    pattern = rf"\b{re.escape(word)}(?![a-z])"
                    if re.search(pattern, combined_text, re.IGNORECASE):
                        matched_words.append(word)
                
                print(f"  Term '{term}': Matched {matched_words}")
                
                if len(matched_words) > 0:
                    match_found = True
                    break
        
        if match_found:
             print("  ✅ KEEP")
             processed_results.append(r)
        else:
             print("  ❌ DROP (No match found)")

    print(f"\nFinal Processed Results: {len(processed_results)}")

if __name__ == "__main__":
    # Test Case 1: Known Celebrity (Should work)
    test_search_logic("Elon Musk", ["Elon Musk"])
    
    # Test Case 2: Broad Search
    test_search_logic("Elon Musk site:twitter.com", ["Elon Musk"])
