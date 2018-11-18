# Ann and San

EECS 349 project to predict if a kpop song will be popular

## Main Plain

    1. average the popularities of the top kpop popularities, 3 max
        a. 
    2. read all the songs of the playlist from the playlist.txt 10~
    3. store a hashset of song ids 
    4. With 3, get audio features and track information 2
    5. turn the return object of 3 into rows of train.csv 


## Helpers
### Spotify Class:
'
    1. getTrackInfo
        Description: Get info of tracks
        Input: list of spotify id, field wanted
        Output: dictionary of song ids: field wanted
    2. getSongsFromPlaylist
        Description: Get spotify id of songs of a playlist
        Input: playlist link
        Output: list of song ids
    3. getAudioAttr
        Description: Get audio features of tracks
        Input: list of spotify id
        Output: dictionary of song ids: dictionary of audio data
'


