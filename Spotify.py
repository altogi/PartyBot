import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import pandas as pd
import random
import pprint
from bottle import route, run, request

class Spotify:
    """A brief class on how to retrieve information from Spotify.
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

        #API AUTHORIZATION
        OAuth_Manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=user_uri, username=user_id, scope=scope, cache_path=cache_path)
        # authorization_code = OAuth_Manager.get_authorization_code()
        # token = OAuth_Manager.get_access_token(code=authorization_code, check_cache=False, as_dict=False)
        self.sp = spotipy.Spotify(auth_manager=OAuth_Manager)
        self.user = self.sp.current_user()
        # self.device = self.sp.devices()
        print('Successfully connected to user ' + str(self.user['display_name']))

        #INITIALIZATION
        self.reset_queue()

    def get_playlists(self):
        """Get user's playlists, indexed by their spotify id and their name"""
        stuff = self.sp.current_user_playlists()['items']
        self.playlists = []
        self.isPartyBot = -1 #Index of PartyBot queue in Spotify
        for i, s in enumerate(stuff):
            info = {'name': s['name'], 'id': s['id']}
            self.playlists.append(info)
            if s['name'] == 'DJ Chatty':
                self.isPartyBot = i

    def reset_queue(self):
        """Reset the queue. Index of user list corresponding to queue is PartyBot"""
        # self.sp.pause_playback()
        self.get_playlists()
        if self.isPartyBot != -1:
            self.sp.current_user_unfollow_playlist(self.playlists[self.isPartyBot]['id'])

        self.sp.user_playlist_create(user=self.user['id'], name='DJ Chatty')
        self.get_playlists()

        self.empty = True
        self.queue_ids = []
        self.queue = None
        
    def get_track_features(self, id):
        """Returns infomation for a track id"""
        meta = self.sp.track(id)

        # meta
        name = meta['name']
        album = meta['album']['name']
        artist = meta['album']['artists'][0]['name']
        release_date = meta['album']['release_date']
        length = meta['duration_ms']
        popularity = meta['popularity']

        # features
        # features = self.sp.audio_features(id)
        # acousticness = features[0]['acousticness']
        # danceability = features[0]['danceability']
        # energy = features[0]['energy']
        # instrumentalness = features[0]['instrumentalness']
        # liveness = features[0]['liveness']
        # loudness = features[0]['loudness']
        # speechiness = features[0]['speechiness']
        # tempo = features[0]['tempo']
        # time_signature = features[0]['time_signature']

        track = {'name': name,
                 'album': album,
                 'artist': artist,
                 'release_date': release_date,
                 'length': length,
                 'popularity': popularity,
                 # 'danceability': danceability,
                 # 'acousticness': acousticness,
                 # 'energy': energy,
                 # 'instrumentalness': instrumentalness,
                 # 'liveness': liveness,
                 # 'loudness': loudness,
                 # 'speechiness': speechiness,
                 # 'tempo': tempo,
                 # 'time_signature': time_signature
                 }

        return track
        
    def add_songs_to_queue(self, ids, shuffle=True):
        """Add info from songs identified in list ids to queue"""
        if shuffle: #initial shuffle of songs to be added
            random.shuffle(ids)

        #Add to Spotify Playlist
        self.sp.user_playlist_add_tracks(self.user['id'], self.playlists[self.isPartyBot]['id'], ids)

        if type(ids) == list:
            self.queue_ids = self.queue_ids + ids
        else:
            self.queue_ids.append(ids)

        #Add info to self.queue
        informations = []
        for id in ids:
            information = self.get_track_features(id)
            informations.append(information)
        toadd = pd.DataFrame(informations)

        if self.queue is None:
            self.queue = toadd
        else:
            self.queue.append(toadd, ignore_index=True)

    def shuffle(self):
        """Does a complete shuffle of the existing queue"""
        # Shuffle list of ids
        ids = self.queue_ids.copy()

        #Reset queue based on shuffled ids
        self.reset_queue()
        self.add_songs_to_queue(ids)

    def get_track_ids(self, playlist_id):
        """Returns all the track ids for a user's playlist"""
        ids = []
        playlist = self.sp.user_playlist(self.user['id'], playlist_id)
        for item in playlist['tracks']['items']:
            track = item['track']
            ids.append(track['id'])
        return ids

    def add_playlist_to_queue(self, playlist_ids):
        """Extract song ids from a playlist identified via playlist_id and add them to queue"""
        ids = []
        for pids in playlist_ids:
            ids = ids + self.get_track_ids(pids)
        self.add_songs_to_queue(ids)

    #UNUSED FUNCTIONS
    def get_track_info_from_playlist(self, playlist_id):
        """Returns a data frame with track information for the specific playlist"""
        ids = self.get_track_ids(playlist_id)

        informations = []
        for id in ids:
            information = self.get_track_features(id)
            informations.append(information)

        return pd.DataFrame(informations)

    def get_user_top_tracks(self, time_ranges=['short_term', 'medium_term', 'long_term'], limit=50):
        """Gets the current user's top tracks in a specified time frame"""
        if type(time_ranges) is not list:
            time_ranges = [time_ranges]

        results = []
        for sp_range in time_ranges:
            print("range:", sp_range)
            results = self.sp.current_user_top_tracks(limit=limit)
            for i, item in enumerate(results['items']):
                print(i, item['name'], '//', item['artists'][0]['name'])
                results.append(item)

    def print_user(self, username):
        """Outputs the current user"""
        self.sp.trace = True
        user = self.sp.user(username)
        pprint.pprint(user)
        print(self.sp.current_user())



# spot = Spotify()
# spot.reset_queue()
# spot.add_playlist_to_queue('2zJS01uA6baDkuyd3bpD8J')