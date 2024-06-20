import logging
import os
import importlib
from selenium import webdriver

from Scrapers.Amazon import Amazon
from Scrapers.Chase import Chase
from Scrapers.Walmart import Walmart

driver = webdriver.Chrome()

try:
    scrapers = [s for s in os.listdir("Scrapers") if s.endswith('.py')]

    for scraper in scrapers:
        module = scraper[:-3]
        m = importlib.import_module(f'Scrapers.{module}')
        func = getattr(m, module)

        func(driver)
    
    driver.quit()

except Exception as e:
    logging.error(f"Error: {e}")
