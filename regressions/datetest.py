import csv
from datetime import datetime

months = {'Jan': '1', 'Feb': '2', 'Mar': '3', 'Apr': '4', 'May': '5', 'Jun': '6', 'Jul': '7', 'Aug': '8', 'Sep': '9', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
def format_date_str(s):
    date = s.split()
    if len(date) == 3:
        month = months[date[0]]
        day = date[1][0:-3]
        year = date[2]
    elif len(date) == 2:
        month = months[date[0]]
        day = '1'
        year = date[1]
    else:
        day = '1'
        month = '1'
        year = date[0]
    result = year + '-' + month + '-' + day
    return result

lines = []
with open('./gpu_specs.csv') as file:
    reader = csv.reader(file)
    lines.append(reader.__next__())
    for line in reader:
        date = format_date_str(line[6])
        try:
            d = datetime.strptime(date, '%Y-%M-%d')
        except Exception as e:
            print(e)
            print(line)
            break
        newline = line[0:6]
        newline.append(date)
        lines.append(newline)
print(lines[0])
with open('./features.csv', 'w+') as file:
    writer = csv.writer(file)
    writer.writerows(lines)

