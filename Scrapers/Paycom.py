import io
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def Paycom(driver):

    url = "https://pc00.paycomonline.com/v4/ats/web.php/jobs?jobSearchSettingsId=20&clientkey=A38173AIE92874820ALRE20847CDE927PIW76526&_gl=1*13nwcap*_gcl_au*NjIyMjcwOTQwLjE2OTM1ODExNTguMTQ1MTI0MTM5MC4xNjk1NzM0MDQ5LjE2OTU3MzQwNDg."
    driver.get(url)

    data = get_all_data([], driver)
    df = pd.DataFrame(data, columns=["Name", "Link"])
    
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_string = csv_buffer.getvalue()
    csv_buffer.close()

    return csv_string

def get_data(data, driver):
    try:
        internships = WebDriverWait(driver, 2).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".JobListing__container"))
        )
        for i in internships:
            href = i.get_attribute("href")
            title = i.text
            if title != '':
                data.append([title, href])
        return data
    except TimeoutException:
        return data
    
def get_all_data(data, driver):
    try:
        data = get_data(data, driver)
        btn = driver.find_element(By.CSS_SELECTOR, ".js-pagination-link-next")
        while btn != None and btn.get_attribute("tabindex") != '-1':
            btn.click()
            time.sleep(0.5)
            data = get_data(data, driver)
            btn = driver.find_element(By.CSS_SELECTOR, ".js-pagination-link-next")
        return data
    except NoSuchElementException:
        return data