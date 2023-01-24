import requests, json, os, pickle, time
#from AuthorzationYT import credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from SP_Playlist_Songs import TitleSP, FullSongSP, SongDetails

credentials = None

"""flow = InstalledAppFlow.from_client_secrets_file(
            "secretsYT.json",
            scopes=[
                "https://www.googleapis.com/auth/youtube.force-ssl"   # Access The Secret.json File to get my ID's
            ]
        )

flow.run_local_server(
    port=8080, prompt="consent",    #Runs A server, in this case a local server
    authorization_prompt_message=""
)

credentials = flow.credentials
print(credentials.to_json())"""

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
        
        credentials = flow.credentials # Stores my credentials which consist off my token, refresh token, my ID's and scope + expire dates

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as f:
            print('Saving Credentials for Future Use...')
            pickle.dump(credentials, f)

youtube = build("youtube", "v3", credentials=credentials)

def SerachYTVids():
    print("Searching For The Songs!")
    query = FullSongSP[i]
    request = youtube.search().list(
    part="snippet",
    q=query
)
    response = request.execute()
    for item in response['items']:
        if item['id']['kind'] == 'youtube#video':

            video_title = item['snippet']['title']
            print("-------------------------------------------")
            print("Song:", video_title)
            video_id = item['id']['videoId']
            break
    return video_id

def YTPlaylsit():

    PlaylistContents = youtube.playlists().list(
        part="snippet,contentDetails",
        maxResults=50,
        mine=True
    )
    TitlesYT = []
    req = PlaylistContents.execute()
    for titles in req["items"]:
        TitlesYT.append(titles["snippet"]["title"]) #Gets all of the playlist names/titles
    
    if TitleSP in TitlesYT:  # Checks if playlist already exists
        print("Playlist Already Exist!")
        print("Playlist Is Being Updated...")
    else:
        PlaylistCreate = youtube.playlists().insert(
            part="snippet",
            body={
                "snippet": {
                    "title": f"{TitleSP}",
                    "description": "",
                    "status": "public"
                    }
                
                }
        )
        Playlist = PlaylistCreate.execute()
        playlist_id = Playlist["id"]
        print("Playlist Created!\nImporting Songs To YT...")

        #print(FullSongSP)
        global i
        if len(FullSongSP) > 200:
            max = 200
        else:
            max = len(FullSongSP)
        for i in range(0, max):
            video_id = SerachYTVids()
            AddVids = youtube.playlistItems().insert(
            part="snippet",
            body={
                'snippet': {
                    'playlistId': playlist_id,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id
                    }
                }
            }
        )
            AddVids.execute()

YTPlaylsit()
print("Playlist has been Converted to Youtube :)")