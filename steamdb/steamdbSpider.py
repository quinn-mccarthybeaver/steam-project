import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

df = pd.DataFrame()

options = webdriver.ChromeOptions()
cookie_name = "cf_clearance"
cookie_value = "COOKIE HERE"
driver = uc.Chrome(chrome_options=options)

driver.get("https://steamdb.info/stats/releases/")

# Inject the cookie into the Chrome WebDriver session
driver.add_cookie({"name": cookie_name, "value": cookie_value})
cookie_name = "__Host-steamdb"
cookie_value = "COOKIE HERE"
driver.add_cookie({"name": cookie_name, "value": cookie_value})
driver.get("https://steamdb.info/stats/releases/")
time.sleep(3)

table = driver.find_element(By.CLASS_NAME, "table")

rows = table.find_elements(By.TAG_NAME, "tr")

for i in range(1, len(rows)):
    #wait until table is loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "table")))
    table = driver.find_element(By.CLASS_NAME, "table")
    rows = table.find_elements(By.TAG_NAME, "tr")
    cell = rows[i].find_elements(By.TAG_NAME, "td")
    #getting date from selenium
    date = cell[0].text
    print(date)
    link = cell[2].find_elements(By.TAG_NAME, "a")[0]
    link.click()
    #wait until without limiting button is loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[1]/div[2]/a")))
    driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div[2]/a").click()
    time.sleep(5)
    #scroll to last listing to load all results
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #get page source
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    games = soup.find_all("tr", class_="app")
    for game in games:
        gameinfo = game.find_all("td")
        title = gameinfo[2].find("a").contents[0]
        release_date = f"{gameinfo[3].text.strip()} {date}"
        peak_players = gameinfo[4].text.strip()
        positive_reviews = gameinfo[5].text.strip()
        negative_reviews = gameinfo[6].text.strip()
        total_reviews = gameinfo[7].text.strip()
        rating = gameinfo[8].text.strip()
        dicst = {"game": title,
                 "link":gameinfo[2].find("a")['href'],
                 "release": release_date,
                 "peak_players": peak_players,
                 "positive_reviews": positive_reviews,
                 "negative_reviews": negative_reviews,
                 "total_reviews": negative_reviews,
                 "rating": rating
                 }
        df = df.append(dicst, ignore_index=True)

    df.to_csv("../data/steamdb2018-.csv")
    #back to year listings
    driver.get("https://steamdb.info/stats/releases/")
