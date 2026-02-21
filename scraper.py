import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os
import time

os.makedirs("data", exist_ok=True)

scrape_date = datetime.today().date()

base_url = "https://www.property24.co.ke/property-for-sale-in-westlands-s14537"

headers = {
    "User-Agent": "Mozilla/5.0"
}

data = []

for page in range(1, 21):  # Scrape 20 pages
    print(f"Scraping page {page}...")

    url = f"{base_url}?page={page}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed on page", page)
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    properties = soup.find_all("span", class_="p24_content")

    print("Found:", len(properties), "properties")

    for prop in properties:

        price_tag = prop.select_one(".p24_price")
        if price_tag:
            raw_price = price_tag.text.strip()
            clean_price = raw_price.replace("KSh", "").replace(" ", "")
            price = int(clean_price)
        else:
            price = None

        title_tag = prop.select_one(".p24_propertyTitle")
        title = title_tag.text.strip() if title_tag else "N/A"

        location_tag = prop.select_one(".p24_location")
        location = location_tag.text.strip() if location_tag else "N/A"

        features = prop.select(".p24_featureDetails span")
        bedrooms = features[0].text.strip() if len(features) > 0 else None
        bathrooms = features[1].text.strip() if len(features) > 1 else None
        parking = features[2].text.strip() if len(features) > 2 else None

        data.append([price, title, location, bedrooms, bathrooms, parking, scrape_date])

    time.sleep(2)  # polite delay

print("Total extracted:", len(data))

with open("data/westlands_sale_raw_listing.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Price", "Title", "Location", "Bedrooms", "Bathrooms", "Parking", "Scrape Date"])
    writer.writerows(data)

print("Data saved successfully.")
