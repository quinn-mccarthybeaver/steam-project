from bs4 import BeautifulSoup
from os import listdir
from sys import exit
import csv

with open('./gpu_specs.csv', 'w+') as file:
    # this list is used later to ensure that values are being writen in the same order for all gpus
    insert_order = ['GPU Name', 'Cores', 'TMUs', 'ROPs', 'Memory Size', 'Bus Width', 'Release Date']
    writer = csv.writer(file)
    writer.writerow(insert_order)
    for f in listdir('./gpu_specs'):
        with open('./gpu_specs/' + f) as file:
            soup = BeautifulSoup(file, 'lxml')

            # find the specs at the top of the page.
            # if this table doesn't exist the whole page is empty, so skip it
            table = soup.find('dl', attrs={'class': 'gpudb-specs-large'})
            if table == None:
                continue

            # empty line to be inserted into the csv
            values = {'GPU Name': '', 'Cores': 0, 'TMUs': 0, 'ROPs': 0, 'Memory Size': 0, 'Bus Width': 0, 'Release Date': ''}

            # find the release date
            # some cards are listed as 'Never Released', so we look here next to test if we should skip
            date = soup.find('dt', string='Release Date')
            parent = date.parent()
            if parent[1].text == 'Never Released':
                continue
            else:
                values['Release Date'] = parent[1].text

            # process the specs
            # not all specs are relevant, so we only keep the ones that are in the dictionary
            for entry in table.find_all('div', attrs={'class': 'gpudb-specs-large__entry'}):
                title = entry.find('dt').text
                value = entry.find('dd').text.split()[0]
                if value == 'N/A':
                    value = 0

                if title in values and value != 'System':
                    values[title] = float(value)

            # lastly get the name of the gpu
            values['GPU Name'] = soup.find('h1', attrs={'class': 'gpudb-name'}).text

            # this guarentees that the values are all inserted in the same order
            # the values method is not guarenteed to yield values in the same order for all files
            line = []
            for key in insert_order:
                line.append(values[key])

            writer.writerow(line)
