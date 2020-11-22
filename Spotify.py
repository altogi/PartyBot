import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import pandas as pd
import random
import pprint
from bottle import route, run, request

class Spotify:
    """A brief teston how to retrieve information from Spotify.
    Sources used:
        https://developer.spotify.com/documentation/web-api/reference-beta/#category-search
        https://morioh.com/p/31b8a607b2b0"""
    def __init__(self, client_id='0015dd2ff12d40b89e5818097516fa34', client_secret='6f19910581724c179df0e97f9abc0af0', user_id='alvaro0089', user_uri='http://google.com', scope='playlist-modify-public', cache_path='.cache'):
        # Creates a connection to the Spotify API

        # STEFFEN:
        # client_id = '358be15819664fa598bec77d802c89f0'
        # client_secret = '70dd13694c604426a25a91f5138d6d40'
        # user_id = '1134627099'
        # cache_path='.ste'

        OAuth_Manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=user_uri, username=user_id, scope=scope, cache_path=cache_path)
        # authorization_code = OAuth_Manager.get_authorization_code()
        # token = OAuth_Manager.get_access_token(code=authorization_code, check_cache=False, as_dict=False)
        self.sp = spotipy.Spotify(auth_manager=OAuth_Manager)
        self.user = self.sp.current_user()
        # self.device = self.sp.devices()
        print('Successfully connected to user ' + str(self.user['display_name']))
        self.reset_queue()


    def get_playlists(self):
        """Get user's playlists, indexed by their spotify id and their name"""
        stuff = self.sp.current_user_playlists()['items']
        self.playlists = []
        self.isPartyBot = -1
        for i, s in enumerate(stuff):
            info = {'name': s['name'], 'id': s['id']}
            self.playlists.append(info)
            if s['name'] == 'PartyBot':
                self.isPartyBot = i

    def reset_queue(self):
        """Reset the queue, expressed as a list called PartyBot"""
        # self.sp.pause_playback()
        self.get_playlists()
        if self.isPartyBot != -1:
            self.sp.current_user_unfollow_playlist(self.playlists[self.isPartyBot]['id'])

        self.sp.user_playlist_create(user=self.user['id'], name='PartyBot')
        self.get_playlists()

        self.empty = True
        self.queue_ids = []
        self.queue = None

    def add_ids_to_queue(self, ids, shuffle=True):
        if shuffle: #initial shuffle of songs to be added
            random.shuffle(ids)

        self.sp.user_playlist_add_tracks(self.user['id'], self.playlists[self.isPartyBot]['id'], ids)
        self.queue_ids.append(ids)

        informations = []
        for id in ids:
            information = self.getTrackFeatures(id)
            informations.append(information)
        toadd = pd.DataFrame(informations)

        if self.queue is None:
            self.queue = toadd
        else:
            self.queue.append(toadd, ignore_index=True)


    def add_playlist_to_queue(self, playlist_id):
        ids = self.getTrackIDs(playlist_id)
        self.add_ids_to_queue(ids)

    def shuffle(self):
        ids = self.queue_ids.copy()
        random.shuffle(ids)
        self.sp.user_playlist_replace_tracks(self.user['id'], self.playlists[self.isPartyBot]['id'], ids)

    def getTrackIDs(self, playlist_id):
        """Returns all the track ids for a user's playlist"""
        ids = []
        playlist = self.sp.user_playlist(self.user['id'], playlist_id)
        for item in playlist['tracks']['items']:
            track = item['track']
            ids.append(track['id'])
        return ids

    def getTrackFeatures(self, id=None, fromID=False):
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

    def getTrackInformationFromPlaylist(self, playlist_id):
        """Returns a data frame with track information for the specific playlist"""
        ids = self.getTrackIDs(playlist_id)

        informations = []
        for id in ids:
            information = self.getTrackFeatures(id)
            informations.append(information)

        return pd.DataFrame(informations)

    def getUserTopTracks(self, time_ranges=['short_term', 'medium_term', 'long_term'], limit=50):
        if type(time_ranges) is not list:
            time_ranges = [time_ranges]

        results = []
        for sp_range in time_ranges:
            print("range:", sp_range)
            results = self.sp.current_user_top_tracks(limit=limit)
            for i, item in enumerate(results['items']):
                print(i, item['name'], '//', item['artists'][0]['name'])
                results.append(item)

    def printUser(self, username):
        self.sp.trace = True
        user = self.sp.user(username)
        pprint.pprint(user)
        print(self.sp.current_user())



# spot = Spotify()
# spot.reset_queue()
# spot.add_playlist_to_queue('2zJS01uA6baDkuyd3bpD8J')