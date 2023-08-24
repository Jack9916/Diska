import pandas as pd
import DiskaScraping
import os

def is_json_dataframe_empty(json_file):
    try:
        df = pd.read_json(json_file)
        return df.empty
    except (FileNotFoundError, ValueError):
        return True  # File doesn't exist, so it's considered empty


if is_json_dataframe_empty('hikes_df.json'):
    DiskaScraping.compute_df()
    hikes_df = pd.read_json('hikes_df.json')
else:
    hikes_df = pd.read_json('hikes_df.json')
print(hikes_df.to_string())
def custom_sorting_key(hike):
    # Define your ranking criteria here
    return hike["rating"]  # Change this to your preferred ranking criteria


sorted_hikes = sorted(hikes_info, key=custom_sorting_key, reverse=True)

# Step 5: Displaying Results
for rank, hike in enumerate(sorted_hikes, start=1):
    print(f"Rank {rank}: {hike['name']} - Rating: {hike['rating']:.2f}")

# You can further enhance and customize each step as per your needs.
