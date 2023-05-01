from os import listdir
import csv
from datetime import datetime

def join(l):
    result = l[0]
    for s in l[1:]:
        result += ',' + s
    return result


def make_fina_data():
    card_names = []
    for filename in listdir('./cleaned_cards'):
        name = filename.replace('_', ' ')[0:-4]
        card_names.append((name, filename))
        

    # associate each filename in cleaned_cards with a line in features
    matches = {}
    with open('./features.csv', 'r') as feature_file:
        reader = csv.reader(feature_file)
        reader.__next__()

        for line in reader:
            for (name, filename) in card_names:
                if name in line[0]:
                    if name not in matches:
                        matches[name] = (filename, line)


    # append the matched line in features to each line in the associated filename
    lines = [['card','date','real_users','GPU_name','cores','tmus','rops','memory_size','bus_width','release_date']]
    for (filename, feature_line) in matches.values():
        with open('./cleaned_cards/' + filename) as file:
            reader = csv.reader(file)
            reader.__next__()

            for line in reader:
                newline = line + feature_line
                lines.append(newline)


    # put all these lines into a single csv
    with open('./final_data', 'w+') as file:
        writer = csv.writer(file)
        writer.writerows(lines)

def get_least_date():
    with open('./final_data', 'r') as file:
        reader = csv.reader(file)
        reader.__next__()

        least_date = datetime.strptime(reader.__next__()[-1], '%Y-%M-%d').date()

        for line in reader:
            current = datetime.strptime(line[-1], '%Y-%M-%d').date()
            if current < least_date:
                least_date = current

        print(least_date)

get_least_date()