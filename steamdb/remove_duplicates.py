import pandas as pd
from fuzzywuzzy import fuzz

# Load the dataframe from a CSV file
df = pd.read_csv('card_users_dup_remove.csv', index_col='id')
features_frame = pd.read_csv("../data/features.csv")

save_df = pd.DataFrame()

matching_names = {}

match_dicts = []

for name in df["name"]:
    # Set the initial best match and score to None
    best_match = None
    best_score = None
    match_list = []
    for GPU_name in features_frame["GPU Name"]:
        try:
            score = fuzz.ratio(GPU_name,name)
            if score >= 97:
                match_list.append(GPU_name)
                print(f"Matched {name} with GPU_name: {GPU_name} with score {score}")
                disct = {
                    "steam_name": name,
                    "TechPowerUpName": GPU_name,
                    "MatchScore": score
                }
                match_dicts.append(disct)
            if match_list is not None:
                matching_names[name] = match_list
        except:
            continue
print(matching_names)

# Create a new dataframe from the list of dictionaries
save_df = pd.DataFrame.from_dict(match_dicts)

# Save the dataframe to a CSV file
save_df.to_csv("../data/features_steam.csv", index=False)
