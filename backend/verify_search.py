
import logging
from duckduckgo_search import DDGS
import time
import random
import re

# Setup console logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

def perform_search(query, required_terms=None, max_results=5):
    print(f"\n--- Searching for: {query} ---")
    results = []
    
    with DDGS() as ddgs:
        # Replicating search_logic.py
        ddg_gen = ddgs.text(query, max_results=max_results, safesearch='off')
        
        if ddg_gen:
            for r in ddg_gen:
                title = r.get('title', '')
                body = r.get('body', '')
                url = r.get('href', '')
                
                combined_text = f"{title} {body} {url}"
                print(f"\nPotential Candidate: {title}")
                print(f"URL: {url}")
                # print(f"Body: {body}")
                
                match_found = False
                
                if required_terms:
                    clean_terms = [t.replace('"', '').strip() for t in required_terms if t]
                    print(f"Checking against terms: {clean_terms}")
                    
                    for term in clean_terms:
                        sub_words = term.split()
                        all_words_found = True
                        missing_word = ""
                        
                        for word in sub_words:
                            pattern = rf"\b{re.escape(word)}\b"
                            if not re.search(pattern, combined_text, re.IGNORECASE):
                                all_words_found = False
                                missing_word = word
                                break
                        
                        if all_words_found:
                            print(f"  [MATCH] Found term: {term}")
                            match_found = True
                            break
                        else:
                            print(f"  [FAIL] Missing word: {missing_word}")
                    
                    if not match_found:
                        print("  [DROP] No required terms matched fully.")
                        continue
                
                results.append(title)
    
    print(f"Total Kept: {len(results)}")

# Simulating the user's search
# User was likely searching for their name. I'll use a placeholder or generic assumption 
# based on earlier context ("modi" was mentioned).
# Let's try searching for "Narendra Modi" to see if it filters correctly.
# And "John Doe" for generic checking.

print("TEST 1: 'Narendra Modi'")
perform_search('"Narendra Modi"', required_terms=['Narendra Modi'])

print("\n\nTEST 2: 'Alexander The Great'")
perform_search('Alexander The Great', required_terms=['Alexander The Great'])
