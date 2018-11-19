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
        for track in playlist['tracks']['items']:
            result[track['track']['id']] = track['track']['popularity']

        return result 

    def getAudioAttr(self, tracks):
        pass

