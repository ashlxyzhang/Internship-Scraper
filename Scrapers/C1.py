import io
import pandas as pd
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def C1(driver):
    url = "https://www.capitalonecareers.com/search-jobs?acm=ALL&alrpm=ALL&ascf=[%7B%22key%22:%22custom_fields.Campus%22,%22value%22:%22Internships%22%7D]"
    driver.get(url)

    data = get_all_data([], driver)
    df = pd.DataFrame(data, columns=["Name", "Link"])
    df.to_csv("./CSV/C1.csv")
    
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_string = csv_buffer.getvalue()
    csv_buffer.close()

    return csv_string


def get_data(data, driver):
    internships = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[@data-job-id]"))
    )
    for i in internships:
        href = i.get_attribute("href")
        title = i.find_element(By.XPATH, ".//h2").text
        if title != '':
            data.append([title, href])
    return data

def get_all_data(data, driver):
    try:
        # cookies = driver.find_element(By.ID, 'system-ialert-button')
        # cookies.click()
        data = get_data(data, driver)
        btn = driver.find_element(By.CSS_SELECTOR, '.next')
        while 'disabled' not in btn.get_attribute("class"):
            btn.click()
            time.sleep(0.5)
            data = get_data(data, driver)
            btn = driver.find_element(By.CSS_SELECTOR, '.next')
        return data
    except Exception:
        return data