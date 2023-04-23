import pandas as pd

# read input CSV file
df = pd.read_csv('card_users_real.csv')

# group the data by card and aggregate the dates as a list
grouped = df.groupby('name')['date', 'real_users'].agg(list)

# create a new dataframe with the unique cards and their associated dates
output_df = pd.DataFrame({'card': grouped.index, 'dates': grouped['date'], 'real_users': grouped['real_users']})

for index, row in output_df.iterrows():
    card = row['card']
    dates = row['dates']
    users = row['real_users']
    card_df = pd.DataFrame({'card':card, 'date': dates, 'real_users': users})
    card_df.to_csv(f'cards/{card.replace(" ","_").replace("/","_")}.csv', index=False)

