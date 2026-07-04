import time
import csv
from datetime import date
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://www.amazon.in/")

time.sleep(3)

search = input("Enter product name: ")

box = driver.find_element(By.ID, "twotabsearchtextbox")
box.send_keys(search)
box.submit()

time.sleep(3)
def scrape():
    soup = BeautifulSoup(driver.page_source, "html.parser")

    products = soup.find_all("div", {"data-component-type": "s-search-result"})

    result = []

    for p in products:

        try:
            title = p.h2.text.strip()
        except:
            title = "N/A"

        try:
            price = p.find("span", "a-price-whole").text
        except:
            price = "N/A"

        try:
            rating = p.find("span", "a-icon-alt").text
        except:
            rating = "N/A"

        result.append((title, price, rating))

    return result

all_data = []

for page in range(1, 21):

    print(f"Scraping page {page}...")

    driver.get(f"https://www.amazon.in/s?k={search}&page={page}")

    time.sleep(3)

    data = scrape()

    all_data.extend(data)

file_name = f"{search}_{date.today()}.csv"

with open(file_name, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow(["Title", "Price", "Rating"])

    writer.writerows(all_data)

driver.quit()

print("File saved:", file_name)