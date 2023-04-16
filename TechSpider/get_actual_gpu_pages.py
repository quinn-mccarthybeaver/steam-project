from bs4 import BeautifulSoup
from selenium import webdriver
from random import randint
from time import sleep
# import sys

# direct_links_to_gpu_data.txt
link = 'https://www.techpowerup.com'
driver = webdriver.Firefox()

with open('./direct_links_to_gpu_data.txt', 'r') as extensions:
    for extension in extensions:
        url = link + extension[0:-1]
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'lxml')
        header = soup.find('h1')
        if header != None and header.text == 'HTTP 429 - Too Many Requests':
            # idk something
            print('found a 402 error')
            break
        else:
            with open('./gpu_specs/' + extension[11:-1] + '.html', 'w+') as file:
                file.write(str(soup))

        sleep(randint(8,12))

driver.close()
