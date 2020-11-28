from Spotify import Spotify
from WatsonIntegrator import WatsonIntegrator
import pandas as pd

class PartyBot:
    def __init__(self, numeric=False):
        """This class interacts with the spotify app and the integrated IBM Watson Assistant in order to display assistant
        responses in the console, receive user input, and translate requests to Spotify commands."""

        self.spotify = Spotify()
        self.console = FakeConsole()
        self.watson = WatsonIntegrator(self.console)
        self.running = True
        self.numeric = numeric #Boolean stating whether the user is supposed to answer the requests with options via numbers

        self.functionCodes = ['login', 'NewQueue', 'AddArtists', 'AddFromPlaylist', 'ShowUpcoming', 'Shuffle']
        # self.listIDs = {'mood:party': '2zJS01uA6baDkuyd3bpD8J', 'mood:motivation': '09S8u5CfsqNykVe4PS7y5x', 'mood:chill': '2gSm5ak3xfip096FV2MutF',
        #                 'top:dea': '2pnMZd3r7IrqQVRBxe9CCj', 'top:ignacio': '1J7sfsybA99F8w2UOpQJlM', 'top:alejandro': '5iN04uNssYaPDtgrHCaYUY',
        #                 'top:steffen': '1M4nNxSs4748wpBiufTan8', 'playlist:paolo': '1YGHkKQfOpEQHIO06j71Dy',
        #                 'playlist:alvaro': '1FTlyHI9BQfiPgINi1zR7a', 'playlist:professor': '78sVdD9qWLWGwJZnioJ6xX'}
        self.listIDs = {'playlist:Alvaro:Christmas': '1hwDrMP1y3fn6QgDUmFysl', "playlist:Paolo's Playlists": '3Oev8yETOHlczbqhmURedk', 'artist:Mariah Carey': '5VfX5baCsv3QV5y3Z9W2s9'}

    def fake_login(self):
        """Simple function simulating a normal user login."""
        self.username = self.console.input('Please type your username here:')
        self.password = self.console.input('Please type your password here:')

    def add_playlist(self, names, printQueue=False):
        idtoadd = [self.listIDs[n] for n in names]
        self.spotify.add_playlist_to_queue(idtoadd)

        if printQueue:
            self.console.print('This is your current queue: ')
            self.console.print(self.spotify.queue.loc[:10, ['name', 'album', 'artist']])

    def new_queue(self, params, maxUsers=1):
        self.spotify.reset_queue()

        #Extract parameters
        mood = params[0]
        users = []
        for i in range(maxUsers):
            if len(params[i + 1]) > 0:
                users.append(params[i + 1])

        #Add default host if only one guest is present
        # if len(users) == 1:
        #     users.append('Paolo')

        #Lists to load
        names = []
        for n in self.listIDs.keys():
            for u in users:
                if u + ':' + mood in n:
                    names.append(n)

        self.add_playlist(names)

    def add_artists(self, params):
        artists = params

        # Lists to load
        names = []
        for n in self.listIDs.keys():
            for a in artists:
                if 'artist:' + a in n:
                    names.append(n)

        self.add_playlist(names)

    def add_from_playlist(self, params):
        lists = params

        # Lists to load
        names = []
        for n in self.listIDs.keys():
            for l in lists:
                if 'playlist:' + l in n:
                    names.append(n)

        self.add_playlist(names)

    def show_upcoming(self):
        queue = self.spotify.queue
        self.console.print('These are youre upcoming tracks:')
        for i, s in queue[:10].iterrows():
            self.console.print('    ' + str(i + 1) + '. ' + s['name'] + ' by ' + s['artist'] + '. Album: ' + s['album'])

    def shuffle_queue(self):
        self.spotify.shuffle()

    def interpret_assistant_order(self, functions):
        for i, f in enumerate(functions):
            byparts = f.split(',')
            if byparts[0] in self.functionCodes:
                if byparts[0] == 'login':
                    self.fake_login()
                elif byparts[0] == 'NewQueue':
                    self.new_queue(byparts[1:])
                elif byparts[0] == 'AddArtists':
                    self.add_artists(byparts[1:])
                elif byparts[0] == 'AddFromPlaylist':
                    self.add_from_playlist(byparts[1:])
                elif byparts[0] == 'ShowUpcoming':
                    self.show_upcoming()
                elif byparts[0] == 'Shuffle':
                    self.shuffle_queue()
            else:
                self.console.print('ERROR: Unidentified command from assistant.')
                self.running = False

    def request_input(self, possibles):
        answer = self.console.input('Type your request here:')
        if len(possibles) > 0 and self.numeric:
            invalid = True
            while invalid:
                try:
                    answer = int(answer)
                    invalid = False
                    break
                except:
                    answer = self.console.input('Type your request here (numbers only):')

                answer = possibles[answer - 1]
            else:
                if answer.find('quit') != -1:
                    self.running = False
        else:
            if answer.find('quit') != -1:
                self.running = False
        return answer

    def run(self):
        """This is the main loop of the chatbot, which for every iteration requests user input, obtains the corresponding
        response from the assistant, and presents that response to the user."""
        response = self.watson.request()
        possibles, functions = self.watson.print_response(response, numeric=self.numeric)
        while self.running:
            answer = self.request_input(possibles)
            response = self.watson.request(answer)
            possibles, functions = self.watson.print_response(response, numeric=self.numeric)
            self.interpret_assistant_order(functions)

class FakeConsole:
    def __init__(self, data=None):
        self.data = data

    def input(self, prompt):
        #FILL UP WITH COMMUNICATION WITH MESSENGER, TAKING USER INPUT
        answer = input(prompt + ' \n')
        return answer

    def print(self, string):
        #FILL UP WITH COMMUNICATION WITH MESSENGER, PRINTING PROMPTS
        print(string)


pb = PartyBot()
pb.run()
