import time

from bs4 import BeautifulSoup
from selenium import webdriver
from random import randint
from time import sleep
import undetected_chromedriver as uc

# import sys

# direct_links_to_gpu_data.txt
link = 'https://www.techpowerup.com'
driver = uc.Chrome()
driver.delete_all_cookies()
driver.get(link)
cookie_value = "0e5c8760ffb9213d5e8efd43ad5c15bc"
driver.add_cookie({"name": "botcheck", "value": cookie_value})
# solve captcha?
time.sleep(40)

with open('./direct_links_to_gpu_data.txt', 'r') as extensions:
    line = 3626
    for a, extension in enumerate(extensions):
        if a >= line:
            print(a)
            url = link + extension[0:-1]
            driver.get(url)

            soup = BeautifulSoup(driver.page_source, 'lxml')
            header = soup.find('h1')

            if header != None and header.text == "Are you Human?":
                cookie_value = "0e5c8760ffb9213d5e8efd43ad5c15bc"
                driver.delete_all_cookies()
                driver.add_cookie({"name": "botcheck", "value": cookie_value})
                print("bot check")
                driver.get(url)
                time.sleep(2)

            if header != None and header.text == 'HTTP 429 - Too Many Requests' or header.text == "Are you Human?":
                # idk something
                print('found a 402 error')
                break
            else:
                with open('./gpu_specs/' + extension[11:-1] + '.html', 'w+') as file:
                    file.write(str(soup))
            sleep(randint(8, 12))

driver.close()
