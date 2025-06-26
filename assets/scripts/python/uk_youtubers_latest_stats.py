import os
import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv() 

API_KEY = os.getenv("YOUTUBE_API_KEY")
API_VERSION = 'v3'

youtube = build('youtube', API_VERSION, developerKey=API_KEY, static_discovery=False)

def get_channel_stats(youtube, channel_id):
    request = youtube.channels().list(
        part='snippet,statistics',
        id=channel_id
    )
    response = request.execute()
    # Defensive coding: check if 'items' key exists
    if 'items' in response and response['items']:
        data = dict(
            channel_name=response['items'][0]['snippet']['title'],
            total_subscribers=response['items'][0]['statistics']['subscriberCount'],
            total_views=response['items'][0]['statistics']['viewCount'],
            total_videos=response['items'][0]['statistics']['videoCount'],
        )
        return data
    else:
        print("No 'items' found in response. Possibly invalid channel ID or restricted key.")
        return None



# channel_id = "UC_aEa8K-EOJ3D6gOs7HcyNg" 
channel_id = "UCsooa4yRKGN_zEE8iknghZA"
print(get_channel_stats(youtube, channel_id))


# Read CSV into dataframe 
df = pd.read_csv("youtube_data_united-kingdom.csv")


# Extract channel IDs and remove potential duplicates
channel_ids = df['NOMBRE'].str.split('@').str[-1].unique()

def get_channel_id(youtube, query):
    """
    Given a channel handle, username, or partial name, 
    search and return the channel ID.
    """
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='channel',
        maxResults=1
    )
    response = request.execute()
    if response['items']:
        return response['items'][0]['snippet']['channelId']
    else:
        print(f"Channel not found for query: {query}")
        return None

# Initialize a list to keep track of channel stats
channel_stats = []

# Loop over the channel IDs and get stats for each
for channel_id in channel_ids:
    if not channel_id.startswith("UC"):
        query = channel_id
        channel_id = get_channel_id(youtube, query)

    stats = get_channel_stats(youtube, channel_id)
    if stats is not None:
        channel_stats.append(stats)
    else:
        # Append placeholder values to preserve alignment
        channel_stats.append({
            'channel_name': None,
            'total_subscribers': None,
            'total_views': None,
            'total_videos': None
        })

# Convert the list of stats to a DataFrame
stats_df = pd.DataFrame(channel_stats)

# Reset index to ensure alignment
df.reset_index(drop=True, inplace=True)
stats_df.reset_index(drop=True, inplace=True)

# Concatenate the dataframes horizontally
combined_df = pd.concat([df, stats_df], axis=1)



# Drop the 'channel_name' column from stats_df (since 'NOMBRE' already exists)
# combined_df.drop('channel_name', axis=1, inplace=True)


# Save the merged dataframe back into a CSV file
combined_df.to_csv('updated_youtube_data_uk.csv', index=False)


combined_df.head(10) 