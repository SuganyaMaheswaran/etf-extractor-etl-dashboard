import DataScraperService as ds
import ScrapeETF as etfScraper 
  

if __name__=="__main__":
    
   for etf in ds.get_funds():
    url=etf[0]
    etf =etf[1]
    etfScraper.scrapeETF(url, etf)

