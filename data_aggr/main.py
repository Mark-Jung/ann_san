import os
from utils.spotify import Spotify


spotify = Spotify("fef9a71f9bac41a48155f3a4ac971f4f", os.environ['SPOTIFY'])
spotify.getToken()

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
        output: hashset of song ids
    """
    foo = open(filename, "r")
    playlists = foo.readlines()
    foo.close()
    tracks = set()
    for playlist in playlists:
        temp = spotify.getSongsFromPlaylist(playlist)
        print(temp)
        tracks.update(temp)
    return tracks

def averageKPOP(filename):
    """
        Gets the list of kpop playlists and averages the popularity
        input: file path
        output: double
    """

    tracks = tracksFromPlaylist(filename)

    song_popularities = spotify.getTracksInfo(tracks, 'popularity')
    
    avg = 0
    for each in song_popularities:
        avg += each

    return avg / len(song_popularities)

#avg_kpop = averageKPOP("kpop.txt")

tracksFromPlaylist('kpop.txt')

# training_songs = trainingSongs("train_playlist.txt")


