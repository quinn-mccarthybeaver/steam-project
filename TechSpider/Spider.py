from random import randint

import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select

df = pd.DataFrame()

driver = webdriver.Firefox()
prod_status = ["Active", "End-of-life", "Unknown", "Unreleased"]
for prod in prod_status:
    link = f"https://www.techpowerup.com/gpu-specs/?eol={prod}"
    driver.get(link)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    mfgr_option = soup.find("select", {"name": "mfgr"}).findAll("option")[1:]
    for mfgr_selection in mfgr_option:
        drop_val = mfgr_selection.get("value")
        print(drop_val)
        driver.get(link + f"&mfgr={drop_val}")
        # reset page source
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        # load date lists
        year_option = soup.find("select", {"name": "released"}).findAll("option")[1:]
        for year_selection in year_option:
            time.sleep(randint(9, 20))
            driver.get(link + f"&mfgr={drop_val}&released={year_selection.get('value')}")
            # reset page source
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')
            #
            table_elements = soup.find("table", class_="processors").findAll("tr")
            print(table_elements[0].text)
            for itr in range(2, len(table_elements)):
                td_val = table_elements[itr].findAll("td")
                dicst = {"Product": td_val[0].text.strip(),
                         "Manufacturer": drop_val,
                         "Architecture": td_val[1].text.strip(),
                         "Released": td_val[2].text.strip(),
                         "BUS": td_val[3].text.strip(),
                         "Memory": td_val[4].text.strip(),
                         "GPU.Clock": td_val[5].text.strip(),
                         "Memory.Clock": td_val[6].text.strip(),
                         "Shaders.TMUs.ROPs": td_val[7].text.strip(),
                         "Production.Status": prod
                         }
                df = df.append(dicst, ignore_index=True)
                df.to_csv("TechPowerUpEOL.csv")
        time.sleep(randint(30, 65))
    time.sleep(randint(40, 60))

driver.close()
