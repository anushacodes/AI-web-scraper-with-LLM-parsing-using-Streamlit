import requests
from bs4 import BeautifulSoup
import re

def scrape_website(url, selector=None):
    """
    Scrapes content from a website URL.
    
    Args:
        url (str): The URL to scrape
        selector (str, optional): CSS selector to target specific content
        
    Returns:
        str: The scraped and cleaned text content
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "header", "footer", "nav"]):
            script.extract()
        
        # Get text based on selector if provided
        if selector and selector.strip():
            content = soup.select(selector)
            text = ' '.join([element.get_text(strip=True) for element in content])
        else:
            # Default to main content areas if no selector
            main_content = soup.find_all(['article', 'main', '.content', '#content', '.post', '.article'])
            if main_content:
                text = ' '.join([element.get_text(strip=True) for element in main_content])
            else:
                text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Clean up excessive whitespace
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r' +', ' ', text)
        
        return text
    except Exception as e:
        return f"Error scraping the website: {str(e)}"
