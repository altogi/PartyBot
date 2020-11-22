from Spotify import Spotify
from WatsonIntegrator import WatsonIntegrator
import pandas as pd

class PartyBot:
    def __init__(self, numeric=False):
        """This class interacts with the spotify app and the integrated IBM Watson Assistant in order to display assistant
        responses in the console, receive user input, and translate requests to Spotify commands."""

        self.spotify = Spotify()
        self.watson = WatsonIntegrator()
        self.running = True
        self.numeric = numeric

        self.functionCodes = ['login', 'newQueue', 'playlist:alvaro', 'playlist:paolo', 'playlist:professor', 'mood:party',
                              'mood:motivation', 'mood:chill', 'shuffle']
        self.listIDs = {'mood:party': '2zJS01uA6baDkuyd3bpD8J', 'mood:motivation': '09S8u5CfsqNykVe4PS7y5x', 'mood:chill': '2gSm5ak3xfip096FV2MutF',
                        'top:dea': '2pnMZd3r7IrqQVRBxe9CCj', 'top:ignacio': '1J7sfsybA99F8w2UOpQJlM', 'top:alejandro': '5iN04uNssYaPDtgrHCaYUY',
                        'top:steffen': '1M4nNxSs4748wpBiufTan8', 'playlist:paolo': '1YGHkKQfOpEQHIO06j71Dy',
                        'playlist:alvaro': '1FTlyHI9BQfiPgINi1zR7a', 'playlist:professor': '78sVdD9qWLWGwJZnioJ6xX'}



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


    def request_input(self, possibles):
        answer = input('Type your request here: \n')
        if len(possibles) > 0:
            if self.numeric:
                invalid = True
                while invalid:
                    try:
                        answer = int(answer)
                        invalid = False
                        break
                    except:
                        answer = input('Type your request here (numbers only): \n')

                answer = possibles[answer - 1]
            else:
                if answer.find('quit') != -1:
                    self.running = False
        else:
            if answer.find('quit') != -1:
                self.running = False
        return answer

    def interpret_assistant_order(self, functions):
        for i, f in enumerate(functions):
            if f in self.functionCodes:
                if f == 'login':
                    self.fake_login()
                elif f == 'newQueue':
                    self.new_queue()
                elif f.find('playlist') != -1:
                    self.add_playlist(f)
                elif f.find('mood') != -1:
                    self.add_playlist(f)
                elif f == 'shuffle':
                    self.shuffle_queue()
            else:
                print('ERROR: Unidentified command from assistant.')
                self.running = False

    def fake_login(self):
        """Simple function simulating a normal user login."""
        self.username = input('Please type your username here: \n')
        self.password = input('Please type your password here: \n')

    def new_queue(self):
        self.spotify.reset_queue()

    def shuffle_queue(self):
        self.spotify.shuffle()

    def add_playlist(self, name):
        idtoadd = self.listIDs[name]
        self.spotify.add_playlist_to_queue(idtoadd)
        print('This is your current queue: ')
        print(self.spotify.queue.loc[:10, ['name', 'album', 'artist']])


pb = PartyBot()
pb.run()
