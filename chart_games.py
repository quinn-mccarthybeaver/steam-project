import pandas
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("./data/playerdata/games_steam_all.csv")

df['release'] = pd.to_datetime(df['release'])  # convert date column to datetime type
print(df)

# plot the DataFrame with a scatter plot
ax = df.plot(x='release', y='peak_players', kind='scatter')
ax.set_xlabel('Date')
ax.set_ylabel('peak_players')
ax.set_yticks(range(0, 100000, 10000))
ax.set_ylim(bottom=0, top=100000)
plt.show()
