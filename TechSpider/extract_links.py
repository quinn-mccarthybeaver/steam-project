from os import listdir
from bs4 import BeautifulSoup

for page in listdir('./scraped_pages'):
    with open('./scraped_pages/' + page, 'r') as file:
        soup = BeautifulSoup(file, 'lxml')
        print(page)
        for a in soup.find('table').find_all('a'):
            print(a.get('href'))
