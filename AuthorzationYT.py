import os, pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def Authorize():
    global credentials
    credentials = None

    # If Their is a file called token.pickle and if their is, it will read the file as token
    if os.path.exists('token.pickle'):
        print('Loading Credentials From File...')
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)

    # If there are no valid credentials available, then either refresh the token or log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print("Refreshing Access Token...")
            credentials.refresh(Request())
        else:
            print("Fetching New Tokens...")
            flow = InstalledAppFlow.from_client_secrets_file(
                "secretsYT.json",
                scopes=[
                    "https://www.googleapis.com/auth/youtube.force-ssl"   # Access The Secret.json File to get my ID's
                ]
            )

            flow.run_local_server(
                port=8080, prompt="consent",    #Runs A server, in this case a local server
                authorization_prompt_message=""
            )
            
            credentials = flow.credentials# Stores my credentials which consist off my token, refresh token, my ID's and scope + expire dates

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as f:
                print('Saving Credentials for Future Use...')
                pickle.dump(credentials, f)

            return credentials

credentials = Authorize()

