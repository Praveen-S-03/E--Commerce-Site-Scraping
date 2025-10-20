#E-commerce site with multiple categories, subcategories.
#Instead of using pagination this site loads items when user scrolls the page down.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import pandas as pd

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

urls = [
    "https://webscraper.io/test-sites/e-commerce/more/computers/laptops",
    "https://webscraper.io/test-sites/e-commerce/more/computers/tablets",
    "https://webscraper.io/test-sites/e-commerce/more/phones/touch"
]

product_list = []

for url in urls:
    driver.get(url)

    # Handle cookie banner if present
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'acceptCookies'))
        ).click()
    except:
        pass  # cookie banner not present

    # Infinite scroll
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Extract product data
    product_name_list = driver.find_elements(By.CLASS_NAME, "title")
    product_price_list = driver.find_elements(By.CLASS_NAME, "price")
    description_list = driver.find_elements(By.CLASS_NAME, "description")

    for item, price, desc in zip(product_name_list, product_price_list, description_list):
        product_list.append({
            "Product Name": item.get_attribute("title").strip(),
            "Price": price.text,
            "Description": desc.text.strip().replace('"', ""),
            "Link": item.get_attribute("href").strip()
        })
driver.quit()

with open("../JSON Outputs/output_scraper5.json", "w") as data_file:
    json.dump(product_list, data_file, indent=4)

df = pd.DataFrame(product_list)
df.to_csv("../CSV Outputs/output_scraper5.csv", index=False)

print("Scraping completed for all URLs!")
