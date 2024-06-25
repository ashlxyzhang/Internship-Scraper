import io
import pandas as pd
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def AWS(driver):
    url = "https://amazon.jobs/content/en/teams/amazon-web-services/internships?country%5B%5D=US"
    driver.get(url)

    data = get_all_data([], driver)
    df = pd.DataFrame(data, columns=["Name", "Link"])
    df.to_csv("./CSV/aws.csv")
    
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_string = csv_buffer.getvalue()
    csv_buffer.close()

    return csv_string


def get_data(data, driver):
    internships = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".header-module_title__9-W3R"))
    )
    for i in internships:
        href = i.get_attribute("href")
        title = i.text
        if title != '':
            data.append([title, href])
    return data

def get_all_data(data, driver):
    try:
        data = get_data(data, driver)
        btn = driver.find_element(By.CSS_SELECTOR, '[data-test-id="next-page"]')
        while btn.get_attribute("tabindex") != '-1':
            btn.click()
            time.sleep(0.5)
            data = get_data(data, driver)
            btn = driver.find_element(By.CSS_SELECTOR, '[data-test-id="next-page"]')
        return data
    except Exception:
        return data