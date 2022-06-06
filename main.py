from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from random import random
from bs4 import BeautifulSoup
import pandas as pd

def to_float(x): # converts strange strings to float
    a = ""
    flag = 0 # have we met "," or "."
    for i in x:
        if ord(i) >= ord("0") and ord(i) <= ord("9"):
            a += i
        elif not flag and (i == "." or i == ","):
            a += i
            flag = 1
    a = a.replace(",", ".")
    return float(a)

options = webdriver.ChromeOptions() # setting options for window
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

driver = webdriver.Chrome('chromedriver', options=options) # start and get target page
driver.get("https://store.steampowered.com/specials#p=0&tab=TopSellers")
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
totalpages = (soup.find("span", {"id" : "TopSellers_links"})).find_all("span", {"class" : "paged_items_paging_pagelink"})
totalpages = int(totalpages[-1].getText())

header = ["Game", "Original price", "Discount", "Final price"]
table = []
current_page = 0

while (current_page < totalpages):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    soup = soup.find("div", {"id" : "TopSellersTable"})
    games = soup.find_all("div", {"class" : "tab_item_name"})
    original_prices = soup.find_all("div", {"class" : "discount_original_price"})
    discounts = soup.find_all("div", {"class": "discount_pct"})
    final_prices = soup.find_all("div", {"class": "discount_final_price"})
    for i in range(len(games)):
        games[i] = games[i].getText()
        original_prices[i] = to_float(original_prices[i].getText())
        discounts[i] = to_float(discounts[i].getText())
        final_prices[i] = to_float(final_prices[i].getText())
        table.append([games[i], original_prices[i], discounts[i], final_prices[i]])
    sleep(1 + 2 * random()) # 1 - 3 sec
    current_page += 1
    element = driver.find_element(By.ID, "TopSellers_btn_next")  # find and push button to increase list of games to parse
    element.click()
    sleep(1 + 2 * random())

pd.DataFrame(table).to_csv('SteamDiscounts.csv', index=False, header=header)

driver.quit()