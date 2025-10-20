#E-commerce site with multiple categories, subcategories.
#Instead of using pagination this site uses a "Load more" button to load more items.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import pandas as pd

urls = [
    "https://webscraper.io/test-sites/e-commerce/more/computers/laptops",
    "https://webscraper.io/test-sites/e-commerce/more/computers/tablets",
    "https://webscraper.io/test-sites/e-commerce/more/phones/touch"
]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

product_list= []

for url in urls:
    print(f"Scraping: {url}")
    driver.get(url)

    # Accept cookies if present
    try:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME, 'acceptCookies'))).click()
    except:
        pass

    # Load all products
    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            more_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-primary"))
            )

            if not more_button:
                break

            more_button.click()
            time.sleep(2)

        except Exception:
            break

    # Extract products
    product_name_list = driver.find_elements(By.CLASS_NAME, "title")
    product_price_list = driver.find_elements(By.CLASS_NAME, "price")
    description = driver.find_elements(By.CLASS_NAME, "description")

    for item, price, info in zip(product_name_list, product_price_list, description):
        product_list.append({
            "Category": url.split("/")[-1],
            "Product Name": item.get_attribute("title").strip(),
            "Price": price.text,
            "Description": info.text.strip().replace('"', ""),
            "Link": item.get_attribute("href").strip()
        })

driver.quit()

# Save output
with open("../JSON Outputs/output_scraper4.json", "w") as data_file:
    json.dump(product_list, data_file, indent=4)

df = pd.DataFrame(product_list)
df.to_csv("../CSV Outputs/output_scraper4.csv", index=False)

print("Scraping completed for all URLs!")
