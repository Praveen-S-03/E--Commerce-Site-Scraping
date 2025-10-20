#E-commerce site with multiple categories, subcategories.
#Standard links are used for pagination.
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

# List of category URLs to scrape
base_urls = [
    "https://webscraper.io/test-sites/e-commerce/static/computers/laptops",
    "https://webscraper.io/test-sites/e-commerce/static/computers/tablets",
    "https://webscraper.io/test-sites/e-commerce/static/phones/touch",
]

product_list = []

for base_url in base_urls:
    page = 1
    print(f"\n🔎 Scraping category: {base_url}")

    while True:
        url = f"{base_url}?page={page}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f" Failed to retrieve page {page}. Stopping this category.")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        product_names = soup.find_all("a", class_="title")
        product_prices = soup.find_all(class_="price")
        descriptions = soup.find_all(class_="description")

        if not product_names:
            print(" No more products in this category. Moving to next.")
            break

        for item, price, info in zip(product_names, product_prices, descriptions):
            product_list.append({
                "Category": base_url.split("/")[-1],  # extract category name
                "Product Name": item.get("title"),
                "Price": price.text.strip(),
                "Description": info.text.strip().replace('"', ""),
                "Link": "https://webscraper.io" + item.get("href")
            })

        print(f"✅ Scraped page {page}")
        page += 1

# Save to JSON
with open("../JSON Outputs/output_scraper2.json", "w", encoding="utf-8") as data_file:
    json.dump(product_list, data_file, indent=4, ensure_ascii=False)

# Save to CSV
df = pd.DataFrame(product_list)
df.to_csv("../CSV Outputs/output_scraper2.csv", index=False)

print("\n✅ Scraping completed for all categories!")
print("Files saved:")
