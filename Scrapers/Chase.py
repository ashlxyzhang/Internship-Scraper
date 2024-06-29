import io
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def Chase(driver):
    url = "https://careers.jpmorgan.com/us/en/students/programs?search=&tags=location__Americas__UnitedStatesofAmerica"
    driver.get(url)
    time.sleep(0.5)

    checkbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'filter-found-show-open-check'))
        # EC.presence_of_element_located((By.CSS_SELECTOR, '.filter-display-card .active'))
    )
    if not checkbox.is_selected():
        checkbox.click()
    time.sleep(0.5)
    
    tabs = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'tab-nav-link'))
    )

    data = []
    for tab in tabs:
        if "Internship" in tab.text:
            tab.click()
            time.sleep(0.5)
            data = get_tab_data(data, driver)
            time.sleep(0.5)
    
    df = pd.DataFrame(data, columns=['Name', 'Link'])
    df.to_csv("./CSV/chase.csv")
    
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_string = csv_buffer.getvalue()
    csv_buffer.close()

    return csv_string

def get_tab_data(data, driver):
    internships = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.filter-display-card.active'))
    )
    for internship in internships:
        a = internship.find_element(By.TAG_NAME, 'a')
        href = a.get_attribute("href")
        title = a.text
        if title != "":
            data.append([title, href])
    
    return data