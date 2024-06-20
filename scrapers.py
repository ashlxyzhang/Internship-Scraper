import logging
import os
import importlib
import requests
from selenium import webdriver

driver = webdriver.Chrome()
logging.basicConfig(level=logging.INFO)
bucketName = "internships-summer-2025"

try:
    scrapers = [s for s in os.listdir("Scrapers") if s.endswith('.py')]

    for scraper in scrapers:
        module = scraper[:-3]
        m = importlib.import_module(f'Scrapers.{module}')
        func = getattr(m, module)

        func(driver)
        logging.info(f'{module} done')

        objectName = module.lower() + ".csv"
        filePath = requests.utils.quote(f"/Users/ashley/Documents/repos/Internship Scraper/CSV/{objectName}", safe='')
        response = requests.post(f'http://localhost:8080/api/s3/putObject/{bucketName}/{objectName}/{filePath}')
        logging.info(response)
    
    driver.quit()

except Exception as e:
    logging.error(f"Error: {e}")
