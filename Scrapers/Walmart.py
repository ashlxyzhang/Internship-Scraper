import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def Walmart(driver):
    url = "https://careers.walmart.com/results?q=2024&page=1&sort=date&jobCategory=00000159-759e-d286-a3f9-7fbe44710000,00000159-75a2-d286-a3f9-7fa2bac60000,00000159-75a8-d2b4-abdd-f5af3e670000,00000159-7627-d286-a3f9-7ea7d10c0000,00000161-8bda-d3dd-a1fd-bbda62130000,00000161-7bf4-da32-a37b-fbf7c59e0000,00000161-8bd0-d3dd-a1fd-bbd0febc0000,00000161-8be6-da32-a37b-cbe70c150000&jobSubCategory=0000015a-a527-d752-a75a-f7f73e820000,00000188-e346-df4d-affe-effebb320000,0000018b-48a2-d283-abeb-5afe854e0000,0000018b-492e-da98-adfb-79ef66c60000,0000018b-482e-dbdf-a19b-6fbe62a80000,0000018b-48e0-dd60-a3af-6dfd11120000,0000018b-492b-de4a-ad9f-59ff1a230000,0000018b-484c-de4a-ad9f-58df75a80000,0000018b-491b-d494-a3cb-ed9b5efc0000,0000018b-491e-de4a-ad9f-59df415f0000,0000018b-491f-d494-a3cb-ed9f2fff0000,0000018b-4921-dbdf-a19b-6fbf76cc0000,0000015a-a52a-d06d-af5f-f5bb06450000,0000018b-4831-d283-abeb-5a7d7b260000,0000018b-485e-da98-adfb-78ff5f550000,0000018b-4860-d283-abeb-5a7c5d410000,0000018b-4920-d494-a3cb-edb3f3c30000,0000018b-4926-dbdf-a19b-6fbe42760000,0000017c-a4f6-dfa9-a77d-acf64f2f0000,0000018b-48dd-de4a-ad9f-58dffc9d0000,0000018b-4926-da98-adfb-79e7eca60000,0000018b-492b-de4a-ad9f-59ffa0d10000,0000018b-492d-de4a-ad9f-59ff17530000,0000018b-492c-d283-abeb-5b7c8e360000&jobEmploymentType=0000015a-721c-de53-ab7e-767e668d0000&expand=department,brand,type,rate&type=jobs"
    driver.get(url)

    loc = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'location'))
    )
    time.sleep(7)
    loc.click()

    data = get_data([], driver)
    df = pd.DataFrame(data, columns=['Name', 'Link'])
    df.to_csv("./CSV/walmart.csv")


def get_data(data, driver):
    internships = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.job-listing__link'))
    )
    for internship in internships:
        href = internship.get_attribute("href")
        title = internship.text
        if title != "":
            data.append([title, href])
    
    return data