import os
import base64
import requests
import six

"""
    Spotify Class:
        1. 
        Get info of tracks
            input: list of spotify id, field wanted
            output: dictionary of song ids: field wanted
        2.
        Get spotify id of songs of a playlist
            input: playlist link
            output: list of song ids
        3.
        Get audio features of tracks
            input: list of spotify id
            output: dictionary of song ids: dictionary of audio data
"""

class Spotify():

    def __init__(self):
        self.token = 'Bearer ' + os.environ['SPOTIFY']

    def getAudioInfo(self, tracks):
        """
            input: list of spotify id, field wanted
            output: dictionary of song ids: field wanted
        """
        result = {}
        cnter = 0
        while cnter < len(tracks):
            if cnter + 100 <= len(tracks):
                reach = cnter + 100
            else:
                reach = len(tracks)
            payload = tracks[cnter:reach]
            spotify_ready = ','.join(payload)
            url = "https://api.spotify.com/v1/audio-features/?ids=" + spotify_ready 
            headers = {
                'authorization': self.token,
                'content-type': "application/json",
                'cache-control': "no-cache",
                'postman-token': "828d920f-cf71-b0c6-697e-7fa1759d9c27"
                }
            response = requests.request("GET", url, headers=headers)
            if not response.ok:
                print(response.status_code)
                print(response.json())
                print(response.content)
                raise Exception("Couldn't get playlist: " + playlist_id)
            playlist = response.json()
            for each in playlist['audio_features']:
                result[each['id']] = each
            cnter = reach
        return result

    def getSongsFromPlaylist(self, playlist_id):
        url = "https://api.spotify.com/v1/playlists/" + playlist_id
        headers = {
            'authorization': self.token,
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "828d920f-cf71-b0c6-697e-7fa1759d9c27"
            }

        response = requests.request("GET", url, headers=headers)

        if not response.ok:
            print(response.status_code)
            print(response.json())
            print(response.content)
            raise Exception("Couldn't get playlist: " + playlist_id)
        playlist = response.json()
        result = {}
        artists = {}

        for track in playlist['tracks']['items']:
            result[track['track']['id']] = track['track']['popularity']
            artist_ids = []
            for artist in track['track']['artists']:
                artist_ids.append(artist['id'])
            artists[track['track']['id']] = artist_ids
        
        return result, artists

    def getPlaylists(self, category, country, limit):
        url = "https://api.spotify.com/v1/browse/categories/" + category +'/playlists?country='+country+'&limit='+limit 
        headers = {
            'authorization': self.token,
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "828d920f-cf71-b0c6-697e-7fa1759d9c27"
            }

        response = requests.request("GET", url, headers=headers)

        if not response.ok:
            print(response.status_code)
            print(response.json())
            print(response.content)
            raise Exception("Couldn't get playlist: " + response.status_code)
        playlists = response.json()
        result = set()
        for playlist in playlists['playlists']['items']:
            result.add(playlist['id'])

        return result

    def getArtists(self, track_artists):
        all_artists = set()
        for artists in track_artists.values():
            all_artists.update(artists)
        
        result = {}
        cnter = 0
        all_artists = list(all_artists)

        while cnter < len(all_artists):
            if cnter + 48 <= len(all_artists):
                reach = cnter + 48
            else:
                reach = len(all_artists)
            names = ','.join(all_artists[cnter:reach])
            url = "https://api.spotify.com/v1/artists?ids=" + names
            headers = {
            'authorization': self.token,
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "828d920f-cf71-b0c6-697e-7fa1759d9c27"
            }
            response = requests.request("GET", url, headers=headers)
            if not response.ok:
                print(response.status_code)
                print(response.json())
                print(response.content)
                raise Exception("Couldn't get artists: " + response.status_code)
            artists_sth = response.json()
            for each in artists_sth['artists']:
                result.update({each['id']:[each['followers']['total'],each['popularity']]})
            cnter = reach

        updated_track_artists = {}

        for _id, artists in track_artists.items():
            maxfol = 0
            maxpop = 0

            for artist in artists:
                fol_pop = result[artist]
                maxfol = max(maxfol, fol_pop[0])
                maxpop = max(maxpop, fol_pop[1])
            updated_track_artists[_id] = [maxfol, maxpop]
        return updated_track_artists