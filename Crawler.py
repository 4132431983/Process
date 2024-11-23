import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Set to keep track of visited URLs
visited_urls = set()

# Function to crawl a URL and search for a specific word
def crawl_url(url, search_word, base_url):
    try:
        # Check if the URL has already been visited
        if url in visited_urls:
            return False  # Return False to indicate that the word was not found on this path

        # Add the URL to the set of visited URLs
        visited_urls.add(url)

        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Search for the specific word in the page's text
            page_text = soup.get_text()
            if search_word in page_text:
                print(f"Found '{search_word}' on {url}")
                return True  # Return True to indicate that the word was found

            # Find and crawl links on the page
            for link in soup.find_all('a', href=True):
                next_url = urljoin(url, link['href'])
                if urlparse(next_url).netloc == urlparse(base_url).netloc:
                    if crawl_url(next_url, search_word, base_url):
                        return True  # Return True if the word is found in a subpage
        else:
            print(f"Failed to crawl {url} (Status Code: {response.status_code})")

    except Exception as e:
        print(f"Error crawling {url}: {str(e)}")

    return False  # Return False if the word was not found on this path

# Start crawling from a seed URL
seed_url = 'https://lbc.cryptoguru.org/dio/1'  # Replace with the URL of the website you want to crawl
search_word = '1JYRNTLhwfZJxbaZAPmgx83Fm3s5rx4NeH'  # Replace with the word you want to search for

if not crawl_url(seed_url, search_word, seed_url):
    print(f"'{search_word}' not found on the entire website.")
