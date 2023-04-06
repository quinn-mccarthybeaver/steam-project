import psycopg2
import csv

conn = psycopg2.connect('host=localhost dbname=steam user=postgres')
curr = conn.cursor()

def make_table():
    stmt = '''
        CREATE TABLE IF NOT EXISTS shws (
        date DATE,
        category TEXT,
        name TEXT,
        change REAL,
        percentage REAL,
        PRIMARY KEY (date, category, name)
    )
    '''

    curr.execute(stmt)
    conn.commit()

def add_rows(dates, categories, names, changes, percentages):
    stmt = '''
        INSERT INTO shws VALUES (%s, %s, %s, %s, %s)
    '''

    for (date, category, name, change, percentage) in zip(dates, categories, names, changes, percentages):
        curr.execute(stmt, vars=[date, category, name, change, percentage])

    conn.commit()

def read_file():
    make_table()
    file = open('shws.csv')
    reader = csv.reader(file)
    reader.__next__()

    dates, categories, names, changes, percentages = [], [], [], [], []
    for line in reader:
        if len(line) != 5:
            print(line)
            continue

        dates.append(line[0])
        categories.append(line[1])
        names.append(line[2])
        changes.append(line[3])
        percentages.append(line[4])

    add_rows(dates, categories, names, changes, percentages)

if __name__ == '__main__':
    read_file()
