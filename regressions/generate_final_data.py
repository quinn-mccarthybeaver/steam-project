import csv
from pprint import pprint
from datetime import date

# original headers
# 0   card
# 1   date
# 2   real_users
# 3   GPU_name
# 4   cores
# 5   tmus
# 6   rops
# 7   memory_size
# 8   bus_width
# 9  release_date

# day0 = datetime.strptime('2002-01-06', '%Y-%M-%d').date()
day0 = date.fromisoformat('2002-01-06')

def make_csv(card=None):
    lines = [['date', 'cores', 'tmus', 'rops', 'memory_size', 'bus_width', 'release_date', 'real_users']]
    with open('./data_with_names.csv', 'r') as file:
        reader = csv.reader(file)
        reader.__next__()

        for line in reader:
            if card != None and line[0] != card:
                continue

            now = date.fromisoformat(line[1])
            now = (now - day0).days

            release = date.fromisoformat(line[-1])
            release = (release - day0).days

            new_line = [now] + line[4:-1] + [release] + [line[2]]
            new_line = list(map(lambda x: float(x), new_line))
            lines.append(new_line)

    return lines

def write_csv(filename):
    with open(filename, 'w+') as file:
        writer = csv.writer(file)
        writer.writerows(lines)

# lines = make_csv()
# write_csv('final_data.csv')

# lines = make_csv(card='Intel HD Graphics 3000')
# write_csv('Intel_graphing_data.csv')

# lines = make_csv(card='AMD Radeon RX 480')
# write_csv('AMD_graphing_data_480.csv')

lines = make_csv(card='Intel HD Graphics 4600')
write_csv('./Intel_HD_Graphics_4600.csv')
