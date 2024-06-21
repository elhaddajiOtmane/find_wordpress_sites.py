import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

# Function to perform a Google search and return the result URLs
def google_search(query, num_results):
    query = urllib.parse.quote_plus(query)
    google_url = f"https://www.google.com/search?q={query}&num={num_results}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(google_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve search results for query: {query}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    result_urls = []
    for g in soup.find_all('div', class_='tF2Cxc'):
        anchors = g.find_all('a')
        if anchors:
            result_urls.append(anchors[0]['href'])
    return result_urls

# List of Google Dorks to identify WordPress sites
queries = [
    'inurl:wp-content',
    'inurl:wp-admin',
    'inurl:wp-includes',
    'intitle:"Powered by WordPress"',
    'intitle:"Just another WordPress site"',
    'intitle:"Proudly powered by WordPress"'
]

# Number of results to retrieve per query
num_results = 10  # Increase this number to get more results

# Find WordPress sites
wordpress_sites = set()
for query in queries:
    print(f"Searching for: {query}")
    urls = google_search(query, num_results)
    wordpress_sites.update(urls)
    # To prevent Google from blocking our requests, we add a delay between queries
    time.sleep(2)  # Adjust the delay as needed

# Save results to a file
with open("wordpress_sites.txt", "w") as file:
    for site in wordpress_sites:
        file.write(site + "\n")

print(f"Found {len(wordpress_sites)} WordPress sites.")
