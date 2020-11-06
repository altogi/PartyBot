import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

class Spotify:
    """A brief teston how to retrieve information from Spotify.
    Sources used:
        https://developer.spotify.com/documentation/web-api/reference-beta/#category-search
        https://morioh.com/p/31b8a607b2b0"""
    def __init__(self, client_id='358be15819664fa598bec77d802c89f0', client_secret='70dd13694c604426a25a91f5138d6d40'):
        # Creates a connection to the Spotify API
        client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def getTrackIDs(self, user, playlist_id):
        """Returns all the track ids for a user's playlist"""
        ids = []
        playlist = self.sp.user_playlist(user, playlist_id)
        for item in playlist['tracks']['items']:
            track = item['track']
            ids.append(track['id'])
        return ids

    def getTrackFeatures(self, id):
        """Returns several infomation for a track id"""
        meta = self.sp.track(id)
        features = self.sp.audio_features(id)

        # meta
        name = meta['name']
        album = meta['album']['name']
        artist = meta['album']['artists'][0]['name']
        release_date = meta['album']['release_date']
        length = meta['duration_ms']
        popularity = meta['popularity']

        # features
        acousticness = features[0]['acousticness']
        danceability = features[0]['danceability']
        energy = features[0]['energy']
        instrumentalness = features[0]['instrumentalness']
        liveness = features[0]['liveness']
        loudness = features[0]['loudness']
        speechiness = features[0]['speechiness']
        tempo = features[0]['tempo']
        time_signature = features[0]['time_signature']

        track = {'name': name,
                 'album': album,
                 'artist': artist,
                 'release_date': release_date,
                 'length': length,
                 'popularity': popularity,
                 'danceability': danceability,
                 'acousticness': acousticness,
                 'energy': energy,
                 'instrumentalness': instrumentalness,
                 'liveness': liveness,
                 'loudness': loudness,
                 'speechiness': speechiness,
                 'tempo': tempo,
                 'time_signature': time_signature}

        return track

    def getTrackInformationFromPlaylist(self, user, playlist_id):
        """Returns a data frame with track information for the specific playlist"""
        ids = self.getTrackIDs(user, playlist_id)

        informations = []
        for id in ids:
            information = self.getTrackFeatures(id)
            informations.append(information)

        return pd.DataFrame(informations)

steffen_user_id = '1134627099'
steffen_rap_playlist_id = '7shzVjgaJdeO3euWSrNE3w'

spot = Spotify()
result = spot.getTrackInformationFromPlaylist(steffen_user_id, steffen_rap_playlist_id)
print(result)