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

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = ""
        self.auth_header = ""

    def getToken(self):
        if self.token != "":
            return self.token
        else:
            auth_header = base64.b64encode(six.text_type(self.client_id + ':' + self.client_secret).encode('ascii'))
            headers = {'Authorization': 'Basic %s' % auth_header.decode('ascii')}
            payload = { 'grant_type': 'client_credentials'}
            response = requests.post("https://accounts.spotify.com/api/token", data=payload,
            headers=headers, verify=True)
            if response.status_code != 200:
                raise Exception("Couldn't Login")
            token_info = response.json()
            token = token_info["access_token"]
            self.token = token
            self.auth_header = {'Authorization': "Bearer " + token}

        return token


    def getTracksInfo(self, tracks, target):
        """
            input: list of spotify id, field wanted
            output: dictionary of song ids: field wanted
        """
        spotify_ready = tracks.join(',')
        result = {}
        pass

    def getSongsFromPlaylist(self, playlist_id):
        response = requests.get("https://api.spotify.com/v1/playlists/" + playlist_id, headers=self.auth_header)
        if response.status_code != 200:
            print(response.status_code)
            raise Exception("Couldn't get playlist: " + playlist_id)
        playlist = response.json()
        print(playlist)
        return playlist['tracks']

    def getAudioAttr(self, tracks):
        pass


