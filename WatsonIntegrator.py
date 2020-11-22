import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ApiException

class WatsonIntegrator:
    """This class contains all the commands involving connecting the Python script with a specific Watson chatbot given
    an API key, a version, a service URL, and an assistant ID.
    Source: https://cloud.ibm.com/apidocs/assistant/assistant-v2?code=python
    """
    def __init__(self, api_key='6QwkLfZzI3h-Jq0nSDFwLTLucDKwD4WXu_cYSmzHp0IR', version='2020-09-24', service_url='https://api.eu-de.assistant.watson.cloud.ibm.com', assistant_id='49257b13-bd2b-405a-89ed-1e0e45f1f05e'):
        """This class contains all interaction with a pre-built IBM Watson assistant. It takes as input:
        api_key: The assistant's API key
        version: The versopn of the API to be used, in yyyy-mm-dd format
        service_url: The desired service URL
        assistant_id: The assistant's ID. Changes with every login.
        """
        self.assistant_id = assistant_id
        authenticator = IAMAuthenticator(api_key)
        self.assistant = AssistantV2(version=version, authenticator=authenticator)
        self.assistant.set_service_url(service_url)

        # Creates a session (=connection).
        # Connection persists until connection gets deleted or time out
        try:
            response = self.assistant.create_session(assistant_id=self.assistant_id).get_result()
            self.session_id = response['session_id']
            # self.assistant.set_detailed_response(True)

            print('Successfully connected to the assistant. Session ID: ' + str(self.session_id))

        except ApiException as ex:
            print("Method failed with status code " + str(ex.code) + ": " + ex.message)
            self.session_id = None

    def request(self, message='hello'):
        """ This function sends a request (input message) to and receives a response from the assistant"""
        response = None
        try:
            input = {'message_type': 'text', 'text': message}
            response = self.assistant.message(assistant_id=self.assistant_id, session_id=self.session_id, input=input).get_result()
        except ApiException as ex:
            print("Method failed with status code " + str(ex.code) + ": " + ex.message)
        return response

    def print_response(self, response, functionkey='function:', numeric=True):
        """This function prints the standard json response in the console, so it is nice and tidy.
        functionkey is a string indicating the keyword to be detected to execute functions"""
        possibles = []  # List of possible answers
        functions = [] #List of called functions
        response = response['output']['generic']
        for r in response:
            if r['response_type'] == 'option':
                print(r['title'])
                options = r['options']
                if numeric:
                    print('Type the number corresponding to the corresponding option:')
                for i, o in enumerate(options):
                    if numeric:
                        print('   ' + str(i + 1) + '. ' + o['label'])
                    else:
                        print('   ' + o['label'])
                    possibles.append(o['value']['input']['text'])
            elif r['response_type'] == 'text':
                if r['text'].find(functionkey) == -1:
                    print(r['text'])
                else:
                    cut = r['text'].find(functionkey) + len(functionkey)
                    functions.append(r['text'][cut:])

        return possibles, functions

    def close(self):
        # Deletes session
        self.assistant.delete_session(self.assistant_id, self.session_id)

# w = WatsonIntegrator()
# r = w.request('new queue')
# w.print_response(r)
# r = w.request('top 100')
# w.print_response(r)