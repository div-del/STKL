from search_logic import deep_dive_search
import logging

# Configure logging to console
logging.basicConfig(level=logging.INFO)

print("Starting independent search test...")
results = deep_dive_search("Sam Altman")
print(f"Search complete. Found {sum(len(v) for v in results.values())} results.")
print(results)
