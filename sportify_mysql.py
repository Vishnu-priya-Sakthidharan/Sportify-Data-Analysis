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

# Inserting the data to db
insert_query = '''
INSERT INTO spotify_tracks(track_name, artist, album, popularity, duration_minutes,country)
VALUES(%s,%s,%s,%s,%s,%s)
'''

print("Track Name:", track_data['Track Name'], type(track_data['Track Name']))
print("Artist:", track_data['Artist'], type(track_data['Artist']))
print("Album:", track_data['Album'], type(track_data['Album']))
print("Popularity:", track_data['Popularity'], type(track_data['Popularity']))
print("Duration (minutes):", track_data['Duration (minutes)'], type(track_data['Duration (minutes)']))
print("Country:", track_data['country'], type(track_data['country']))


cursor.execute(insert_query, (
    track_data['Track Name'],
    track_data['Artist'],
    track_data['Album'],
    track_data['Popularity'],
    track_data['Duration (minutes)'],
    track_data['country']
))

connection.commit() # at this point only, mysql stores the data

cursor.close()
connection.close()