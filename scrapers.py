import logging
import os
import importlib
import requests
from selenium import webdriver

driver = webdriver.Chrome()
logging.basicConfig(level=logging.INFO)

bucketName = "internships-summer-2025"
csv_path = "/Users/ashley/Documents/repos/Internship Scraper/CSV/"
upload_endpoint = f"http://localhost:8080/api/s3/putObject/{bucketName}"

try:
    scrapers = [s for s in os.listdir("Scrapers") if s.endswith('.py')]

    for scraper in scrapers:
        module = scraper[:-3]
        m = importlib.import_module(f'Scrapers.{module}')
        func = getattr(m, module)

        csv = func(driver)
        logging.info(f'{module} done')
        logging.info(f'CSV length: {len(csv)}')

        objectName = module.lower() + ".csv"
        filePath = csv_path + objectName

        files = {'file': (f'{objectName}', csv, 'text/csv')}
        response = requests.post(f'{upload_endpoint}/{objectName}', files=files)
        logging.info(f'Upload complete: {response}')
    
    driver.quit()

except Exception as e:
    logging.error(f"Error: {e}")
