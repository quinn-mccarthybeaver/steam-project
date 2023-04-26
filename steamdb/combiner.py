import pandas as pd
import re

# pd1 = pd.read_csv("../data/games-release-steamdb.csv")
# pd2 = pd.read_csv("../data/games-release-steamdb2.csv")
# pd1 = pd1.drop('id',axis=1)
# pd2 = pd2.drop('id',axis=1)
# out = pd1.append(pd2,ignore_index=True)
#
# out.to_csv("../data/games-release-steamdbALL.csv")


# survey = pd.read_csv("../shws.csv", parse_dates=True)
# users_df = pd.read_csv("../data/users-year-steamdb.csv", parse_dates=True)
#
# merged_df = pd.merge(survey, users_df, on="date")
# merged_df['real_users'] = (merged_df['percentage'] * merged_df['Users']).astype(int)
#
# rows = merged_df['category'] == 'Video Card Description'
# merged_df = merged_df.loc[rows]
#
# print(merged_df.head())
#
# merged_df.to_csv("card_users_real.csv")

english_pattern = re.compile(r'^[a-zA-Z0-9\s]+$')

convert = pd.read_csv("../data/games-release-ALL.csv")
convert['peak_players'] = convert['peak_players'].str.replace(",", "").astype(int)
# convert = convert.dropna()
# convert['all-time peak'] = convert['all-time peak'].str.replace(",", "").astype(int)
# convert['24-hour peak'] = convert['24-hour peak'].str.replace(",", "").astype(int)
# convert['players right now'] = convert['players right now'].str.replace(",", "").astype(int)
convert['release'] = pd.to_datetime(convert['release']).dt.strftime('%Y-%m-%d')
convert['peak_players'] = convert['peak_players'].astype(str).str.replace(",", "").astype(int)
convert['positive_reviews'] = convert['positive_reviews'].astype(str).str.replace(",", "").astype(int)
convert['negative_reviews'] = convert['negative_reviews'].astype(str).str.replace(",", "").astype(int)
convert['total_reviews'] = convert['total_reviews'].astype(str).str.replace(",", "").astype(int)


add_df = pd.read_csv("../data/steamdb-info.csv", index_col=0)
add_df.dropna()
add_df["Detected Technologies"] = add_df["Detected Technologies"].astype(str).str.replace(",", ";")
add_df['all-time date'] = pd.to_datetime(add_df['all-time date']).dt.strftime('%Y-%m-%d')
add_df['all-time peak'] = add_df['all-time peak'].astype(str).str.replace(",", "").replace("nan", "0").astype(int)
add_df = add_df.drop('id', axis=1)
add_df = add_df.drop('link', axis=1)
convert['rating'] = convert['rating'].str.replace("%", "").astype(float)
convert = convert.drop('link', axis=1)
convert = convert.drop('id', axis=1)
convert = convert.drop('negative_reviews', axis=1)
convert = convert.drop('positive_reviews', axis=1)
convert = convert[convert['game'].apply(lambda x: bool(english_pattern.match(x)))]
convert.to_csv("../data/playerdata/games_english_all.csv")
merged_df = pd.merge(convert, add_df, on="game")
print(merged_df.head())

convert = convert.reset_index(drop=True)
convert['game'] = convert['game'].str.replace(",", " ")
merged_df["game"] = merged_df["game"].astype(str).str.replace(",", "")
merged_df["Publisher"] = merged_df["Publisher"].astype(str).str.replace(",", "")
merged_df["Developer"] = merged_df["Developer"].astype(str).str.replace(",", "")
merged_df = merged_df[merged_df['Publisher'].apply(lambda x: bool(english_pattern.match(x)))]
merged_df = merged_df[merged_df['Developer'].apply(lambda x: bool(english_pattern.match(x)))]
merged_df = merged_df.dropna()
merged_df = merged_df.drop(['Detected Technologies', 'Store Asset Modification Time',
                            'review_percentage', 'players right now', '24-hour peak',
                            'Store Genres', 'Primary Genre',
                            ], axis=1)
merged_df.to_csv("../data/playerdata/test.csv")
