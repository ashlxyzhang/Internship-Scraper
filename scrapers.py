import io
import logging
import os
import importlib
import pandas as pd
import requests
from selenium import webdriver

driver = webdriver.Chrome()
logging.basicConfig(level=logging.INFO)

bucketName = "internships-summer-2025"
csv_path = "/Users/ashley/Documents/repos/Internship Scraper/CSV/"
upload_endpoint = f"http://localhost:8080/api/s3"

try:
    scrapers = [s for s in os.listdir("Scrapers") if s.endswith('.py')]

    for scraper in scrapers:
        module = scraper[:-3]
        m = importlib.import_module(f'Scrapers.{module}')
        func = getattr(m, module)

        # getting new csv from scraper
        csv = func(driver)
        logging.info(f'{module} done')
        logging.info(f'CSV length: {len(csv)}')

        objectName = module.lower() + ".csv"
        filePath = csv_path + objectName

        # get current csv from s3
        response = requests.get(f'{upload_endpoint}/object/{bucketName}/{objectName}')
        if response.status_code == 200:
            curr_csv = response.content.decode('utf-8')
            df = pd.read_csv(io.StringIO(curr_csv))
        else:
            raise Exception("Failed to get current csv from s3")
        
        # compare two csv
        
        # uploading new csv to s3
        files = {'file': (f'{objectName}', csv, 'text/csv')}
        response = requests.post(f'{upload_endpoint}/putObject/{bucketName}/{objectName}', files=files)
        if response.status_code == 200:
            logging.info(f'Upload complete: {response}')
        else:
            raise Exception("Failed to upload new csv to s3")
    
    driver.quit()

except Exception as e:
    logging.error(f"Error: {e}")
