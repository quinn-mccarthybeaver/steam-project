from os import listdir
from bs4 import BeautifulSoup

for page in listdir('./scraped_pages'):
    with open('./scraped_pages/' + page, 'r') as file:
        soup = BeautifulSoup(file, 'lxml')
        for a in soup.find('table', attrs={'class': 'processors'}).find_all('a'):
            print(a.get('href'))
