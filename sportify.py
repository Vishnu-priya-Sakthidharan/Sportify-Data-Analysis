from spotipy.oauth2 import SpotifyClientCredentials 
import spotipy
from dotenv import load_dotenv
import os
import pandas as pd
import matplotlib.pyplot as plt
import re
from pathlib import Path


#loading the custom .env file which we created
env_path = Path('.') / 'credentials.env'
load_dotenv(dotenv_path=env_path)

# accessing the env variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

print(f'client_id : {CLIENT_ID}')
print(f'client_secret : {CLIENT_SECRET}')

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret= CLIENT_SECRET
))

#Track URL in which we fetch the datas from
track_url = 'https://open.spotify.com/track/3MxLT7m4BjAA0lQl9lVBcM'

#fetching the track id from track_url using regex
track_id = re.search(r'track/([a-zA-Z0-9]+)',track_url).group(1)
print(f'Track ID : {track_id}')

#fetching track details
track = sp.track(track_id=track_id)
# print(track) # we will get metadata as a JSON obj

#fetching track metadata
track_data = {
    'Track Name' : track['name'],
    'Popularity' : track['popularity'],
    'Duration (minutes)' : track['duration_ms'] /60000 ,# in JSON, duration is in milliseconds
    'Artist' : track['album']['artists'][0]['name'],
    'country' : track['available_markets'],
    'Album' : track['album']['name']
}

# converting metadata into dataframe
df= pd.DataFrame(track_data)
print(df)

#storing the data frame in csv file
df.to_csv(path_or_buf='sportify_track.csv',index=False)

#visualize the data
features = ['Popularity','Duration (minutes)']
values = [track_data['Popularity'],track_data['Duration (minutes)']]

plt.figure(figsize=(8,5))
plt.title(f"Track Metadata for '{track_data['Track Name']}'")
plt.bar(features,values,color = 'skyblue',edgecolor = 'black')
plt.ylabel('Values')
plt.show()