import pathlib
from random import randint

import pandas
import pandas as pd
import time
import csv
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

df = pd.DataFrame()
driver = uc.Chrome(use_subprocess=True)

driver.get("https://steamdb.info")
driver.delete_all_cookies()
cookie_name = "__Host-steamdb"
cookie_value = "0%3B4694406%3B58094db8c565c7aa52aca1b2d44f33f733998aad"
driver.add_cookie({"name": cookie_name, "value": cookie_value})
driver.get("https://steamdb.info")
time.sleep(40)

if pathlib.Path("../data/steamdb-info.csv").is_file():
    df = pandas.read_csv("../data/steamdb-info.csv", index_col=0)

with open('../data/games-release-steamdb.csv', mode='r', ) as file:
    csvFile = csv.DictReader(file)

    index = 37324

    try:
        for a, line in enumerate(csvFile):
            if a >= index:
                driver.set_window_size(1024, randint(768, 800))
                id = line['id']
                game = line['game']
                link = line['link']
                driver.get(f"https://steamdb.info{link}charts/")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)

                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'lxml')
                # tables load in the background (apparently>)
                tables = soup.find_all("table", class_="table")
                about_tables = tables[0].find_all("tr")
                info_table = soup.find("div", id="info").find("table", class_="table")
                info_rows = info_table.find_all("tr")

                ul = ""
                plrn = ""
                tfpeak = ""
                allTime = ""
                allTime_date = ""

                try:
                    ul = soup.find("ul", "app-chart-numbers-big").find_all("li")
                    plrn = ul[1].find('strong').text.strip()
                    tfpeak = ul[2].find('strong').text.strip()
                    allTime = ul[3].find('strong').text.strip()
                    allTime_date = ul[3].find('time', {'class': 'timeago'})['datetime']
                    print(allTime_date)
                except:
                    print(f"chart not found for {game}")

                genre = ""
                publisher = ""
                developer = ""
                genres = ""
                technology = ""
                mod = ""
                rev = ""

                for i in range(len(info_rows)):
                    if info_rows[i].find_all("td")[0].text.strip() == "Primary Genre":
                        genre = info_rows[i].find_all("td")[1].text.strip()
                    if info_rows[i].find_all("td")[0].text.strip() == "Publisher":
                        publisher = info_rows[i].find_all("td")[1].text.strip()
                    if info_rows[i].find_all("td")[0].text.strip() == "Developer":
                        developer = info_rows[i].find_all("td")[1].text.strip()
                    if info_rows[i].find_all("td")[0].text.strip() == "Store Genres":
                        genres = info_rows[i].find_all("td")[1].text.strip()
                    if info_rows[i].find_all("td")[0].text.strip() == "Detected Technologies (?)":
                        technology = info_rows[i].find_all("td")[1].text.strip()
                    if info_rows[i].find_all("td")[0].text.strip() == "Store Asset Modification Time":
                        mod = info_rows[i].find_all("td")[1].text.strip()
                    if info_rows[i].find_all("td")[0].text.strip() == "review_percentage":
                        rev = info_rows[i].find_all("td")[1].text.strip()
                disct = {
                    "id": id,
                    "game": game,
                    "link": link,
                    "Primary Genre": genre,
                    "Store Genres": genres,
                    "Publisher": publisher,
                    "Developer": developer,
                    "Detected Technologies": technology,
                    "Store Asset Modification Time": mod,
                    "review_percentage": rev,
                    "players right now": plrn,
                    "24-hour peak": tfpeak,
                    "all-time peak": allTime,
                    "all-time date": allTime_date,
                }
                df = df.append(disct, ignore_index=True)
                print(df.head())
                time.sleep(2)

    except Exception as e:
        print(e)
        df.to_csv("../data/steamdb-info.csv")
    df.to_csv("../data/steamdb-info.csv")
