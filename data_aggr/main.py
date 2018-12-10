import csv
import os
from utils.spotify import Spotify


spotify = Spotify()

"""
    1. average the popularities of the top kpop popularities, 3 max
        a. 
    2. read all the songs of the playlist from the playlist.txt 10~
    3. store a hashset of song ids 
    4. With 3, get audio features and track information 2
    5. turn the return object of 3 into rows of train.csv 
"""
def tracksFromPlaylist(filename):
    """
        Read all the songs of the playlist from the playlist.txt 10~
        input: file path  
        output: dictionary. key = song ids, value = song popularity
    """
    foo = open(filename, "r")
    playlists = foo.readlines()
    foo.close()
    tracks = {}
    all_artists = {}
    for playlist in playlists:
        popularity, artists = spotify.getSongsFromPlaylist(playlist.strip())
        tracks.update(popularity)
        all_artists.update(artists)
    return tracks, all_artists

def averagePlaylists(filename):
    """
        Gets the list of kpop playlists and averages the popularity
        input: file path
        output: double
    """
    tracks = tracksFromPlaylist(filename)
    avg = 0
    for key, value in tracks.items():
        avg += value 

    return avg / len(tracks.items())

def retrieveAudioData(training_songs_ids):
    return spotify.getAudioInfo(training_songs_ids)

def recordAudioDataFromPlaylists(filename, popularity_standard, location):
    training_songs, all_artists = tracksFromPlaylist(filename)

    audio_data = retrieveAudioData(list(training_songs.keys()))

    recording_data = {}

    for _id, popularity in training_songs.items():
        attributes = audio_data[_id]
        classifier = avg_pop >= popularity
        recording_data[_id] = {
                'popularity': classifier,
                'popularity_num': popularity,
                'danceability': attributes['danceability'],
                'energy': attributes['energy'],
                'key': attributes['key'],
                'loudness': attributes['loudness'],
                'mode': attributes['mode'],
                'speechiness': attributes['speechiness'],
                'acousticness': attributes['acousticness'],
                'instrumentalness': attributes['instrumentalness'],
                'liveness': attributes['liveness'],
                'valence': attributes['valence'],
                'tempo': attributes['tempo'],
                'time_signature': attributes['time_signature'],
                }

    # record this shit
    with open(location, 'w', newline='') as csvfile:
        fieldnames = ['popularity', 'popularity_num', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo','time_signature']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for key, value in recording_data.items():
            writer.writerow(value)
def getKpopPlaylists(filename):
    playlists = spotify.getPlaylists('kpop', 'US', str(50))
    destination = open(filename, 'w')
    for each in playlists:
        destination.write(each + '\n')
    destination.close()


getKpopPlaylists('train_kpop.txt')

avg_pop = averagePlaylists("train_kpop.txt")

recordAudioDataFromPlaylists("train_kpop.txt", avg_pop, 'train.csv')

recordAudioDataFromPlaylists('kpop.txt', avg_pop, 'test.csv')
