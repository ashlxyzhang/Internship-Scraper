import io
import pandas as pd
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def Microsoft(driver):
    url = "https://jobs.careers.microsoft.com/global/en/search?lc=United%20States&exp=Students%20and%20graduates&et=Internship&l=en_us&pg=1&pgSz=20&o=Recent"
    driver.get(url)

    data = get_all_data([], driver)
    df = pd.DataFrame(data, columns=["Name", "Link"])
    df.to_csv("./CSV/microsoft.csv")
    
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_string = csv_buffer.getvalue()
    csv_buffer.close()

    return csv_string


def get_data(data, driver):
    internships = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".MZGzlrn8gfgSs8TZHhv2"))
    )
    for i in internships:
        job_item_div = i.find_element(By.XPATH, '../../../..')
        href = "https://jobs.careers.microsoft.com/global/en/job/" + job_item_div.get_attribute('aria-label').split(' ')[-1]
        title = i.text
        if title != '':
            data.append([title, href])
    return data

def get_all_data(data, driver):
    try:
        data = get_data(data, driver)
        btn = driver.find_element(By.XPATH, '//button[@title="Next"]')
        while btn.get_attribute("data-is-focusable") != 'false':
            btn.click()
            time.sleep(0.5)
            data = get_data(data, driver)
            btn = driver.find_element(By.XPATH, '//button[@title="Next"]')
        return data
    except Exception as e:
        return data