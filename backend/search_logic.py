import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time
import random
import logging

from duckduckgo_search import DDGS
from googlesearch import search as gsearch


import re

def perform_search(query, required_terms=None, max_results=5):
    """
    Performs a search using DuckDuckGo, falling back to Google Search if needed.
    Filters results to ensure they contain at least one of the required_terms.
    """
    raw_results = []
    
    # 1. Try DuckDuckGo
    try:
        # Random sleep to minimize rate limiting
        time.sleep(random.uniform(1.0, 2.0))
        logging.info(f"DDG Search: {query}")
        with DDGS() as ddgs:
            ddg_gen = ddgs.text(query, max_results=max_results)
            if ddg_gen:
                for r in ddg_gen:
                    raw_results.append({
                        "title": r.get('title', ''),
                        "url": r.get('href', ''),
                        "description": r.get('body', ''),
                        "source": "DDG"
                    })
    except Exception as e:
        logging.error(f"DDG failed for '{query}': {e}")

    # 2. Fallback to Google Search if DDG failed or returned 0
    if not raw_results:
        try:
            logging.info(f"Google Fallback: {query}")
            from googlesearch import search as gsearch
            # advanced=True returns objects with title/description
            g_gen = gsearch(query, num_results=max_results, advanced=True, sleep_interval=5)
            for r in g_gen:
                raw_results.append({
                    "title": r.title,
                    "url": r.url,
                    "description": r.description,
                    "source": "Google"
                })
        except Exception as e:
             logging.error(f"Google failed for '{query}': {e}")

    # 3. Fallback to Bing Search (Scraping) if Google failed
    if not raw_results:
        try:
            logging.info(f"Bing Fallback: {query}")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            # Search English results
            response = requests.get(f"https://www.bing.com/search?q={query}", headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Bing results are usually in 'li.b_algo'
                results = soup.find_all('li', class_='b_algo')
                for r in results[:max_results]:
                    title_tag = r.find('h2')
                    link_tag = r.find('a')
                    desc_tag = r.find('p')
                    
                    if title_tag and link_tag:
                        raw_results.append({
                            "title": title_tag.get_text(),
                            "url": link_tag.get('href'),
                            "description": desc_tag.get_text() if desc_tag else "",
                            "source": "Bing"
                        })
        except Exception as e:
            logging.error(f"Bing failed for '{query}': {e}")

    # 3. Process and Filter Results
    processed_results = []
    
    for r in raw_results:
        title = r['title']
        body = r['description']
        url = r['url']
        
        combined_text = f"{title} {body} {url}"
        
        match_found = False
        match_reason = ""
        
        # Strict Relevance Check
        if required_terms:
            clean_terms = [t.replace('"', '').strip() for t in required_terms if t]
            
            for term in clean_terms:
                sub_words = term.split()
                if not sub_words:
                    continue
                
                matched_words = []
                for word in sub_words:
                    if len(word) < 3: 
                        continue
                    
                    pattern = rf"\b{re.escape(word)}(?![a-z])"
                    if re.search(pattern, combined_text, re.IGNORECASE):
                        matched_words.append(word)
                        if "#:~:text=" not in url:
                            url += f"#:~:text={word}"

                # Grading
                if len(matched_words) == len([w for w in sub_words if len(w) >= 3]):
                    match_found = True
                    match_reason = f"Exact Match: '{term}'"
                    break
                elif len(matched_words) > 0:
                    match_found = True
                    match_reason = f"Partial Match: {', '.join(matched_words)}"
                
            if not match_found:
                logging.debug(f"Filtered result: '{title}'")
                continue
        else:
            match_reason = "General Search Result"

        processed_results.append({
            "title": title,
            "url": url,
            "description": body,
            "match_context": match_reason 
        })
            
    return processed_results

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
            f'{base_query} "linkedin"', # Broad keyword search
            f'{base_query} "instagram"',
        ],
        "Documents": [
            f'{base_query} resume filetype:pdf',
            f'{base_query} cv filetype:pdf',
            f'{base_query} resume OR cv',
            f'{base_query} filetype:pdf', # Broad document search
        ],
        "news": [
             f'{base_query} news',
             f'{base_query} latest article',
        ],
        "Videos & Media": [
            f'{base_query} site:youtube.com',
            f'{base_query} site:tiktok.com',
            f'{base_query} video OR reel OR channel',
        ],
        "Mentions": [
            f'{base_query} -site:linkedin.com -site:instagram.com -site:facebook.com -site:twitter.com -site:youtube.com',
        ],
        "General": [
            f'{name}', # Fallback broad search
        ]
    }

    # Helper function for threading
    def execute_query(query, category):
        try:
            # Pass list of required terms (Name + Extra Info)
            terms = [name]
            if extra_info:
                terms.append(extra_info)
                
            # Increase max_results to 25 to catch "bits and pieces"
            return category, perform_search(query, required_terms=terms, max_results=25)
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
        "news": [],
        "Videos & Media": [],
        "Mentions": [],
        "General": []
    }

    # Execute in parallel 
    # Reduced workers to 3 to avoid rate limits
    # Deduplication Set
    unique_urls = set()

    def normalize_url(u):
        return u.rstrip('/').lower()

    # Execute tasks in parallel
    # DRASTICALLY REDUCED workers to 2 to bypass bot detection
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_to_query = {executor.submit(execute_query, q, cat): (q, cat) for q, cat in query_tasks}
        
        for future in concurrent.futures.as_completed(future_to_query):
            query_str, original_category = future_to_query[future] # Store original query and category for logging
            try:
                cat, results = future.result()
                if results:
                    for res in results:
                        # Deduplication Check
                        norm_url = normalize_url(res['url'])
                        if norm_url in unique_urls:
                            continue
                        
                        unique_urls.add(norm_url)
                        
                        # Add Score for Sorting
                        # Exact Match = 100 points
                        # Partial Match = 10 points per word
                        # Penalty for generic "General" category? No.
                        score = 0
                        if "Exact Match" in res['match_context']:
                            score = 100
                        elif "Partial Match" in res['match_context']:
                            # Count commas to guess number of words
                            match_count = res['match_context'].count(',') + 1
                            score = 10 * match_count
                        
                        res['_score'] = score
                        structured_results[cat].append(res)
                        
                    # logging.info(f"Added {len(results)} results to {cat}")
            except Exception as e:
                logging.error(f"Task failed for query '{query_str}' in category '{original_category}': {e}")

    # Sort each category by Score (Highest First)
    for cat in structured_results:
        structured_results[cat].sort(key=lambda x: x.get('_score', 0), reverse=True)

    # Calculate stats
    total_results = sum(len(v) for v in structured_results.values())
    logging.info(f"Total results found: {total_results}")
    
    return structured_results
