import json
import requests
from TokenRequestSP import token

playlist_id = input("What is the spotify playlist link? ")

playlist_id = playlist_id.strip("https://open.spotify.com/playlist/")

PlayListEndpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}"

def GetPlayListTracks(token, PlayListEndpoint):
    GetHeader = {
        "Authorization" : "Bearer " + token
    }

    res = requests.get(PlayListEndpoint, headers=GetHeader)
    global PlayListObject
    PlayListObject = res.json()    
    
    return PlayListObject

TrackList = GetPlayListTracks(token, PlayListEndpoint)

with open ("TrackList.json", "w") as f:
    json.dump(TrackList, f)

Num = 0
Tracks = []
FullSongSP = []
TitleSP = PlayListObject["name"]
print("Fetching Spotify Songs...")
for t in TrackList["tracks"]["items"]:
    Num = Num + 1
    print("-------------------------------------------")
    PlayListEndpoint = TrackList["tracks"]["next"]
    SongName = t["track"]["name"]
    print(Num, SongName, "\nBy ")

    for a in t["track"]["artists"]:
        print(a["name"])
        MainArtist = t['track']['artists'][0]['name']

    SongDetails = f"{SongName} By {MainArtist}"

    FullSongSP.append(SongDetails)
    Tracks.append(SongName)


while PlayListEndpoint != None:
    try:
        GetHeader = {
            "Authorization" : "Bearer " + token
        }
        res = requests.get(PlayListEndpoint, headers=GetHeader)
        
        PlayListObject = res.json()

        with open ("TrackList.json", "w") as f:
            json.dump(PlayListObject, f)
        
        Total = PlayListObject["total"]

        for t in PlayListObject["items"]:
            Num = Num + 1
            print("-------------------------------------------")
            SongName = t["track"]["name"]
            print(Num, SongName, "\nBy ")

            for a in t["track"]["artists"]:
                print(a["name"])
                MainArtist = t['track']['artists'][0]['name']

            SongDetails = f"{SongName} By {MainArtist}"

            FullSongSP.append(SongDetails)
            Tracks.append(SongName)
        PlayListEndpoint = PlayListObject["next"]

        if PlayListEndpoint == None:
            print("Total Of Songs In The Playlist: ", Total,"\n")
            break
    except:
        break
