from bs4 import BeautifulSoup
from selenium import webdriver
from random import randint
from time import sleep
import sys

link = 'https://www.techpowerup.com/gpu-specs/'
driver = webdriver.Firefox()
# page_source = driver.page_source

# print(page_source)

with open('links.txt') as gen_names:
    count = 0
    if len(sys.argv) > 1:
        count = int(sys.argv[1])
        for i in range(0, count):
            gen_names.__next__()

    for gen in gen_names:
        extension = f'?generation={gen[0:-1]}&sort=name'
        url = link + extension
        driver.get(url)

        soup = BeautifulSoup(driver.page_source)

        with open('./scraped_pages/' + extension + ".html", 'w+') as saved_html:
            saved_html.write(str(soup))

        sleep(randint(5, 8))
