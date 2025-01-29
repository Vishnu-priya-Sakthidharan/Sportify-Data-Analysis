from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import re
import matplotlib.pyplot as plt
import mysql.connector
from dotenv import load_dotenv
import os
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


#MySQL database connection
db_config = {
    'host' : os.getenv('DB_HOST'),
    'user' : os.getenv('DB_USER'),
    'password' : os.getenv('DB_PASSWORD'),
    'database' : os.getenv('DB_DATABASE')
}

#Connecting to Database

# ** is a operator that unpacks the dictionary so keys become argument nameand values become argument values
# and is equivalent to mysql.connector.connect(
                                #host="localhost",
                                #user="root"  so on..
connection = mysql.connector.connect(**db_config) 

# cursor - helps to excute the statement(eg: insert) in runtime
cursor = connection.cursor()

#reading the track url from the txt file
file_path = 'spotify_track_URLs.txt'
with open(file_path,'r') as txt:
    track_urls = txt.readlines()

#looping through each url
for track_url in track_urls:
    try:
        track_id = re.search(r'track/([a-zA-Z0-9]+)',track_url).group(1)

        #fetching track details
        track = sp.track(track_id=track_id)
        #print(track) # we will get metadata as a JSON obj

        #fetching track metadata
        track_data = {
            'Track Name' : track['name'],
            'Popularity' : track['popularity'],
            'Duration (minutes)' : track['duration_ms'] /60000 ,# in JSON, duration is in milliseconds
            'Artist' : track['album']['artists'][0]['name'],
            'Album' : track['album']['name']
        }

        # Inserting the data to db
        insert_query = '''
        INSERT INTO sportify_tracks(track_name, artist, album, popularity, duration_minutes)
        VALUES(%s,%s,%s,%s,%s)
        '''
        cursor.execute(insert_query, (
            track_data['Track Name'],
            track_data['Artist'],
            track_data['Album'],
            track_data['Popularity'],
            track_data['Duration (minutes)']
        ))

        
        connection.commit() 
        print(f'Inserted : {track_data['Track Name']} by {track_data['Artist']}')
    
    except Exception as e:
        print(f"Error Processing URL : {track_url}, Error {e} ")

cursor.close()
connection.close()

print('Tracks mentioned in the txt file have been inserted into DB!')