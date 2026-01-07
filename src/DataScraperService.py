#Scrape tables, dates, and ETF links from webpages.

from bs4 import BeautifulSoup
from src import constant as c 
import requests

def get_fund_list():
    """Scrapes the Sprott website and return a list of all etfs """
    try:
        response = requests.get(c.SPROTT_ETF_LIST_PAGE, timeout=5)
        response.raise_for_status()
        html = response.text
        print("Success")
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    
    etfs = []
    
    # Return empty list if the fund list div is not found
    nav_div =  soup.find('div', class_=c.FUND_LIST_DIV_CLASS)
    if not nav_div:
        return []
   
    #inserts a tuple for each fund wtih url, name, ticker 
    for a in nav_div.find_all('a', href=True):
        etf_url = c.SPROTT_BASE_URL + a['href'].strip()
        etf_name = a['title'].strip()  # Full name from title attribute
        etf_ticker = a.text.strip()    # Ticker like SETM, URNM
        etfs.append((etf_url, etf_name, etf_ticker))
    
    return etfs
   