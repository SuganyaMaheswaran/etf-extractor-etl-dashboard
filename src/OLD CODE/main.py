import DataScraperService as ds
import ScrapeETF as etfScraper 
from dotenv import load_dotenv
import os

load_dotenv()

if __name__=="__main__":
    
   for etf in ds.get_funds():
    url=etf[0]
    etf =etf[1]
    etfScraper.scrapeETF(url, etf)

