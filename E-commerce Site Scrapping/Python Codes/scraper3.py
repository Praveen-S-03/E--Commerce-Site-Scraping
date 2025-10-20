#E-commerce site with multiple categories, subcategories.
# Dynamic links that use data without reloading the page for pagination.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import pandas as pd

product_list = []

urls = [
    "https://webscraper.io/test-sites/e-commerce/ajax/computers/laptops",
    "https://webscraper.io/test-sites/e-commerce/ajax/computers/tablets",
    "https://webscraper.io/test-sites/e-commerce/ajax/phones/touch"
]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

for url in urls:
    print(f"Scraping: {url}")
    driver.get(url)

    # Accept cookies only once
    try:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME, 'acceptCookies'))).click()
    except:
        pass  # Ignore if already accepted

    while True:
        product_name_list = driver.find_elements(By.CLASS_NAME, "title")
        product_price_list = driver.find_elements(By.CLASS_NAME, "price")
        description_list = driver.find_elements(By.CLASS_NAME, "description")

        for item, price, info in zip(product_name_list, product_price_list, description_list):
            product_list.append(
                {
                    "Category": url.split("/")[-1],
                    "Product Name": item.get_attribute("title").strip(),
                    "Price": price.text,
                    "Description": info.text.strip().replace('"', ""),
                    "Link": "https://webscraper.io" + item.get_attribute("href")
                }
            )

        try:
            next_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div[2]/div[3]/button[2]')
            if not next_button.is_enabled():
                print(" No more products in this category. Moving to next.")
                break
            next_button.click()
            time.sleep(2)
        except:
            print("Next button not found. Exiting.")
            break

driver.quit()

# Save JSON
with open("../JSON Outputs/output_scraper3.json", "w") as data_file:
    json.dump(product_list, data_file, indent=4)

# Save CSV
df = pd.DataFrame(product_list)
df.to_csv("../CSV Outputs/output_scraper3.csv", index=False)

print("Scraping Completed ✅")
