# E-commerce site with multiple categories, subcategories.
# All items are loaded in one page.
import requests
from bs4 import  BeautifulSoup
import json
import pandas
product_list = []

api_url = ["https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops",
           "https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets",
           "https://webscraper.io/test-sites/e-commerce/allinone/phones/touch"]

for url in api_url:
    print(f"\n🔎 Scraping category: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f" Failed to retrieve the URL {url}. Stopping this category.")
        break
    soup = BeautifulSoup(response.text, "html.parser")
    product_names = soup.find_all("a",class_="title")
    product_prices = soup.find_all(class_="price")
    description = soup.find_all(class_="description")
    for item, price , info in zip(product_names, product_prices,description):
        product_list.append(
            {"Category": url.split("/")[-1],
             "Product Name" : item.get("title"),
             "Price" :price.text.strip(),
             "Description" : info.text.strip().replace('"',""),
             "Link": "https://webscraper.io" + item.get("href")
             })
    print(" No more products in this category. Moving to next.")

with open("../JSON Outputs/output_scraper1.json", "w") as data:
    json.dump(product_list,data ,indent=4)

df =pandas.DataFrame(product_list)
df.to_csv("../CSV Outputs/output_scraper1.csv",index=False)
print("\n✅ Scraping completed for all categories!")

