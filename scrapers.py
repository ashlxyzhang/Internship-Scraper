import io
import json
import logging
import os
import importlib
import pandas as pd
import requests
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
logging.basicConfig(level=logging.INFO)

bucketName = "internships-summer-2025"
upload_endpoint = f"http://localhost:8080/api/s3"
email_endpoint = f"http://localhost:8080/api/email/send/ashlxyzhang@tamu.edu"

new_data = {}

try:
    scrapers = [s for s in os.listdir("Scrapers") if s.endswith('.py')]

    for scraper in scrapers:
        module = scraper[:-3]
        m = importlib.import_module(f'Scrapers.{module}')
        func = getattr(m, module)

        # getting new csv from scraper
        new_csv = func(driver)
        new_df = pd.read_csv(io.StringIO(new_csv))
        logging.info(f'{module} done')
        logging.info(f'CSV length: {len(new_csv)}')

        objectName = module.lower() + ".csv"

        # get current csv from s3
        response = requests.get(f'{upload_endpoint}/object/{bucketName}/{objectName}')
        if response.status_code == 200:
            curr_csv = response.content.decode('utf-8')
            curr_df = pd.read_csv(io.StringIO(curr_csv))

            # compare two df
            merged_df = pd.merge(new_df, curr_df, how='left', indicator=True)
            result_df = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge'])

            if len(result_df.values) != 0:
                new_data[module.capitalize()] = result_df.values.tolist()

        elif response.status_code == 500:
            if len(new_df.values) != 0:
                new_data[module.capitalize()] = new_df.values.tolist()

        else:
            raise Exception("Failed to get current csv from s3")
        
        # uploading new csv to s3
        files = {'file': (f'{objectName}', new_csv, 'text/csv')}
        response = requests.post(f'{upload_endpoint}/putObject/{bucketName}/{objectName}', files=files)
        if response.status_code == 200:
            logging.info(f'Upload complete: {response}')
        else:
            raise Exception("Failed to upload new csv to s3")

    requests.get(f'{email_endpoint}', params={'text': json.dumps(new_data)})
    driver.quit()

except Exception as e:
    logging.error(f"Error: {e}")
