from bs4 import BeautifulSoup
from selenium import webdriver
from random import randint
from time import sleep
from os import listdir
# import sys



link = 'https://www.techpowerup.com/gpu-specs/'
# driver = webdriver.Firefox()

for filename in listdir('./scraped_pages'):
    file = open('./scraped_pages/' + filename, 'r')
    local_soup = BeautifulSoup(file, 'lxml')
    header = local_soup.find('h1')
    if header != None and header.text == 'HTTP 429 - Too Many Requests':
        # url = link + file.name[16:-5]
        # driver.get(url)
        # file.close()
        # file = open('./scraped_pages/' + filename, 'w')
        # soup = BeautifulSoup(driver.page_source, 'lxml')
        # x = file.write(str(soup))
        # file.close()
        # sleep(randint(8, 12))
        print(filename)
    else:
        file.close()

# driver.close()
