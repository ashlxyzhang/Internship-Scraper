import os
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def Chase(driver):
    url = "https://careers.jpmorgan.com/US/en/students/programs"
    driver.get(url)

    checkbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'filter-found-show-open-check'))
        # EC.presence_of_element_located((By.CSS_SELECTOR, '.filter-display-card .active'))
    )
    if not checkbox.is_selected():
        checkbox.click()

    tabs = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'tab-nav-link'))
    )
    for tab in tabs:
        if "Internship" in tab.text:
            tab.click()
            data = get_tab_data([], driver)
    
    df = pd.DataFrame(data, columns=['Name', 'Link'])
    df.to_csv("./CSV/chase.csv")

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