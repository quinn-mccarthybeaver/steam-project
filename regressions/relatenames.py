from os import listdir
import csv

names = []
for name in listdir('./cleaned_cards'):
    names.append(name[0:-4].replace('_', ' '))

matches = {}
with open('./features.csv') as file:
    reader = csv.reader(file)
    reader.__next__()
    
    for line in reader:
        feature_name = line[0]
        for name in names:
            if name in feature_name:
                if name in matches:
                    matches[name].append(line[0])
                else:
                    matches[name] = [line[0]]
                break

with open('./matches', 'w+') as file:
    for (key, val) in matches.items():
        file.write(str(key) + ' ' + str(val) + '\n')

unmatched = []
for name in names:
    if name not in matches:
        unmatched.append(name)

with open('./unmatched', 'w+') as file:
    for line in unmatched:
        line = line.replace(' ', '_')
        line += '.csv'
        file.write(str(line) + '\n')
