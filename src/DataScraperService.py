#Scrape tables, dates, and ETF links from webpages.

from bs4 import BeautifulSoup
from src import constant as c 
from urllib.parse import urljoin
import requests

# Fetches HTML from a URL, returns text or empty string on failure.
def fetch_html(url, timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
         return ""
    
# Finds the ETF fund div; returns BeautifulSoup object or None. 

def parse_fund_div(html,element, div_class_name): 
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find(element, class_=div_class_name)

# Extracts ETF info (url, name, ticker from a nav div)
def extract_etfs(nav_div, base_url):
    etfs = []
    if not nav_div:
        return etfs
    for a in nav_div.find_all('a', href=True):
        etf_url = urljoin(base_url,a['href'].strip())
        etf_name = a.get('title', '').strip()
        etf_ticker = a.get_text(strip=True)
        etfs.append((etf_url, etf_name, etf_ticker))

def get_fund_list(url, divClassName,  ):
    html = fetch_html(c.URL)
    if not html:
        return []
    nav_div = parse_fund_div(html, c.FUND_LIST_DIV_CLASS)
    base_url = "{0.scheme}://{0.netloc}".format(requests.utils.urlparse(url))
    return extract_etfs(nav_div, base_url)