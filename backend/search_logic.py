import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time
import random
import logging

from duckduckgo_search import DDGS


import re

def perform_search(query, required_terms=None, max_results=5, retries=3):
    """
    Performs a search using the duckduckgo_search library.
    Filters results to ensure they contain at least one of the required_terms as a WHOLE WORD.
    Returns the result with a 'match_context' explaining why it was kept.
    """
    for attempt in range(retries):
        try:
            # Random sleep to avoid hitting rate limits
            time.sleep(random.uniform(0.5, 1.5))
            
            logging.info(f"Searching for: {query}")
            results = []
            
            with DDGS() as ddgs:
                # safesearch='off' to show EVERYTHING, but we categorize/filter by strict relevance
                ddg_gen = ddgs.text(query, max_results=max_results, safesearch='off')
                
                if ddg_gen:
                    for r in ddg_gen:
                        title = r.get('title', '')
                        body = r.get('body', '')
                        url = r.get('href', '')
                        
                        # Strict Relevance Check (Whole Word Only)
                        # If required_terms are provided, AT LEAST ONE defined term set (e.g., Name OR Extra) must fully match
                        if required_terms:
                            # Normalize terms: remove quotes, strip
                            clean_terms = [t.replace('"', '').strip() for t in required_terms if t]
                            
                            term_matched = False
                            
                            for term in clean_terms:
                                # Split term into individual words (e.g. "John Doe" -> ["John", "Doe"])
                                sub_words = term.split()
                                if not sub_words:
                                    continue
                                
                                # Check if ALL words in this term exist in the text as whole words
                                all_words_found = True
                                missing_word = ""
                                
                                for word in sub_words:
                                    # Smart Regex: 
                                    # \b -> Start of word
                                    # word -> The term
                                    # (?![a-z]) -> Negative lookahead: Next char must NOT be a letter.
                                    # This allows "modi123" (1 != letter) but blocks "modification" (f == letter)
                                    pattern = rf"\b{re.escape(word)}(?![a-z])"
                                    
                                    if not re.search(pattern, combined_text, re.IGNORECASE):
                                        all_words_found = False
                                        missing_word = word
                                        break
                                
                                if all_words_found:
                                    term_matched = True
                                    match_reason = f"Matched Name '{term}'"
                                    match_found = True
                                    
                                    # Highlight the first word found to be helpful
                                    if "#:~:text=" not in url:
                                        url += f"#:~:text={sub_words[0]}"
                                    break # Stop checking other terms if one full term matches
                                else:
                                    logging.debug(f"Partial match fail: '{word}' missing from '{term}' in '{title}'")

                            if not match_found:
                                logging.debug(f"Filtered result: '{title}' (Full name parts not found)")
                                continue
                        else:
                            match_reason = "General Search Result"

                        # Add result with context
                        results.append({
                            "title": title,
                            "url": url,
                            "description": body,
                            "match_context": match_reason 
                        })
            
            if results:
                logging.info(f"Success for '{query}': {len(results)} results")
                return results
            else:
                logging.warning(f"No results found for '{query}' via DDGS.")
                
        except Exception as e:
            logging.error(f"Attempt {attempt+1} failed for '{query}': {e}")
            time.sleep(2 ** attempt)
    
    return []

def deep_dive_search(name, extra_info=""):
    """
    Constructs specific queries to find deeper information and categorizes results.
    Uses parallel execution to speed up the process.
    """
    # Remove specific quotes to allow broader search, relying on strict filter for precision
    base_query = f"{name}"
    if extra_info:
        base_query += f" {extra_info}"
    
    # Define query map: Query -> Category
    query_tasks = []
    
    categories = {
        "Social Profiles": [
            f'{base_query} site:linkedin.com',
            f'{base_query} site:instagram.com',
            f'{base_query} site:facebook.com',
            f'{base_query} site:twitter.com',
            f'{base_query} site:github.com',
        ],
        "Documents": [
            f'{base_query} resume filetype:pdf', # stricter
            f'{base_query} cv filetype:pdf',
            f'{base_query} resume OR cv',
        ],
        "News": [
             f'{base_query} news',
             f'{base_query} latest article',
        ],
        "Mentions": [
            f'{base_query} -site:linkedin.com -site:instagram.com -site:facebook.com -site:twitter.com',
        ],
        "General": [
            f'{name}', # Fallback broad search without quotes for general info
        ]
    }

    # Helper function for threading
    def execute_query(query, category):
        try:
            # Pass list of required terms (Name + Extra Info)
            terms = [name]
            if extra_info:
                terms.append(extra_info)
                
            return category, perform_search(query, required_terms=terms, max_results=4)
        except Exception as e:
            logging.error(f"Error executing {query}: {e}")
            return category, []

    # Prepare tasks
    for category, queries in categories.items():
        for q in queries:
            query_tasks.append((q, category))

    structured_results = {
        "Social Profiles": [],
        "Documents": [],
        "News": [],
        "Mentions": [],
        "General": []
    }

    # Execute in parallel 
    # Reduced workers to 3 to avoid rate limits
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_query = {executor.submit(execute_query, q, cat): (q, cat) for q, cat in query_tasks}
        
        for future in concurrent.futures.as_completed(future_to_query):
            try:
                category, findings = future.result()
                if findings:
                    structured_results[category].extend(findings)
                else:
                    logging.warning(f"No results found for category: {category}")
            except Exception as exc:
                logging.error(f"Task generated an exception: {exc}")

    # Deduplicate results
    for category in structured_results:
        unique_results = []
        seen_urls = set()
        for item in structured_results[category]:
            if item['url'] not in seen_urls:
                unique_results.append(item)
                seen_urls.add(item['url'])
        structured_results[category] = unique_results
        
    return structured_results
