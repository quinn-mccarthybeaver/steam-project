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
driver = uc.Chrome()

driver.get(f"https://steamdb.info")

cookie_name = "__Host-steamdb"
cookie_value = ""
driver.add_cookie({"name": cookie_name, "value": cookie_value})

with open('../data/games-release-steamdb.csv', mode='r', ) as file:
    csvFile = csv.DictReader(file)
    for line in csvFile:
        id = line['id']
        game = line['game']
        link = line['link']
        driver.get(f"https://steamdb.info{link}charts/")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        # tables load in the background (apparently>)
        tables = soup.find_all("table", class_="table")
        about_tables = tables[0].find_all("tr")
        info_table = soup.find("div", id="info").find("table", class_="table")
        info_rows = info_table.find_all("tr")

        ul = soup.find("ul", "app-chart-numbers-big").find_all("li")
        plrn = ul[1].find('strong').text.strip()
        tfpeak = ul[2].find('strong').text.strip()
        allTime = ul[3].find('strong').text.strip()
        allTime_date = ul[3].find('time', {'class': 'timeago'})['datetime']
        print(allTime_date)

        genre = ""
        publisher = ""
        developer = ""
        genres = ""
        technology = ""
        mod = ""
        rev = ""
        try:
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
                "game":game,
                "link":link,
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
                "all-time date": allTime_date
            }
        except:
            df.to_csv("../data/steamdb-info.csv")
            continue
        df = df.append(disct, ignore_index=True)
    df.to_csv("../data/steamdb-info.csv")
