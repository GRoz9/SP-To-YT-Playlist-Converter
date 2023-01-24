import requests, base64, json
from secrets import ClientID, ClientSecret
authURL = "https://accounts.spotify.com/api/token"

authHeader = {}

authData = {}

# Base64 Encode Client ID & Client Secret
def GetAccessToekn(ClientID, ClientSecret):
    message = f"{ClientID}:{ClientSecret}"
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    authHeader["Authorization"] = "Basic " + base64_message
    authData["grant_type"] = "client_credentials"
    res = requests.post(authURL, headers=authHeader, data=authData)

    responseObject = res.json()

    accessToken = responseObject["access_token"]

    return accessToken

# API Requests

token = GetAccessToekn(ClientID, ClientSecret)