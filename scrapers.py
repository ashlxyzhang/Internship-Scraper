import io
import json
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
email_endpoint = f"http://localhost:8080/api/email/send/ashlxyzhang@tamu.edu/New%20Internships"

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
        filePath = csv_path + objectName

        # get current csv from s3
        response = requests.get(f'{upload_endpoint}/object/{bucketName}/{objectName}')
        if response.status_code == 200:
            curr_csv = response.content.decode('utf-8')
            curr_df = pd.read_csv(io.StringIO(curr_csv))
        else:
            raise Exception("Failed to get current csv from s3")
        
        # compare two df
        merged_df = pd.merge(new_df, curr_df, how='left', indicator=True)
        result_df = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge'])

        new_data[module.capitalize()] = result_df.values.tolist()

        # uploading new csv to s3
        # files = {'file': (f'{objectName}', new_csv, 'text/csv')}
        # response = requests.post(f'{upload_endpoint}/putObject/{bucketName}/{objectName}', files=files)
        # if response.status_code == 200:
        #     logging.info(f'Upload complete: {response}')
        # else:
        #     raise Exception("Failed to upload new csv to s3")

    requests.get(f'{email_endpoint}', params={'text': json.dumps(new_data)})
    driver.quit()

except Exception as e:
    logging.error(f"Error: {e}")
