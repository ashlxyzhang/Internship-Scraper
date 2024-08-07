import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import pandas as pd
import io

def Amazon(driver):
    url = "https://amazon.jobs/en/search?offset=0&result_limit=10&sort=recent&country%5B%5D=USA&category_type=studentprograms"
    driver.get(url)

    data = get_all_data([], driver)
    df = pd.DataFrame(data, columns=["Name", "Link"])
    df.to_csv("./CSV/amazon.csv")
    
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_string = csv_buffer.getvalue()
    csv_buffer.close()

    return csv_string


def get_data(data, driver):
    internships = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-link"))
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
        btn = driver.find_element(By.CSS_SELECTOR, ".btn.circle.right")
        while btn != None:
            btn.click()
            time.sleep(0.5)
            data = get_data(data, driver)
            btn = driver.find_element(By.CSS_SELECTOR, ".btn.circle.right")
        return data
    except NoSuchElementException:
        return data