import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ApiException

class WatsonIntegrator:
    """This class contains all the commands involving connecting the Python script with a specific Watson chatbot given
    an API key, a version, a service URL, and an assistant ID.
    Source: https://cloud.ibm.com/apidocs/assistant/assistant-v2?code=python
    """
    def __init__(self, api_key='lshJQKVf5d1RavjB8iiZwMwPr7okluqeFUxXn9EO8ZO4', version='2020-09-24', service_url='https://api.eu-gb.assistant.watson.cloud.ibm.com', assistant_id='230a31fe-885f-4bb9-83d5-e67b1a40229d'):
        """
        {
          "apikey": "lshJQKVf5d1RavjB8iiZwMwPr7okluqeFUxXn9EO8ZO4",
          "iam_apikey_description": "Auto-generated for key e623bc62-063b-4aa1-b72b-b85712c86b57",
          "iam_apikey_name": "Auto-generated service credentials",
          "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager",
          "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/10684d87646946c898045f7a9f6afc91::serviceid:ServiceId-9a6335d0-9858-4a12-a024-a5bee8f93c9b",
          "url": "https://api.eu-gb.assistant.watson.cloud.ibm.com/instances/a144e2c0-1007-426e-a1d1-9f64e6e2e5d6"
        }
        """
        self.assistant_id = assistant_id
        authenticator = IAMAuthenticator(api_key)
        self.assistant = AssistantV2(version=version, authenticator=authenticator)
        self.assistant.set_service_url(service_url)

        # assistant_id changes everytime. can be found in API details when Assistant sessions is started
        # assistant.set_detailed_response(True)

        # Creates a session (=connection).
        # Connection persists until connection gets deleted or time out
        try:
            response = self.assistant.create_session(assistant_id=self.assistant_id).get_result()
            self.session_id = response['session_id']

            print(json.dumps(response, indent=2))

        except ApiException as ex:
            print("Method failed with status code " + str(ex.code) + ": " + ex.message)
            self.session_id = None

    def request(self, message='Hello'):
        # Sends a request (input message) to and receives a response from the assistant
        try:
            response = self.assistant.message(
                assistant_id=self.assistant_id,
                session_id=self.session_id,
                input={
                    'message_type': 'text',
                    'text': message
                }
            ).get_result()

            print(json.dumps(response, indent=2))

        except ApiException as ex:
            print("Method failed with status code " + str(ex.code) + ": " + ex.message)

    def close(self):
        # Deletes session
        self.assistant.delete_session(self.assistant_id, self.session_id)