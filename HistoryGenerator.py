import requests
import base64
import time
import json

    #Global variables

URL = 'https://api.spotify.com/v1/me/player/currently-playing'
URLForPlaylist = 'https://api.spotify.com/v1/me/playlists'
timeElapsed = 0
target_length = 75
access_token = None
refresh_token = None
heads = None
string = None
payload = {
    'market' : 'ES'
}

    #Functions

def Initial_Authorization():
    global heads
    global string
    global access_token 
    global refresh_token 
    
    print("\nInitialization started..\n")
    client_id = input("Please paste your application's Client ID:\n")
    client_secret = input("\nPlease paste your application's Client Secret:\n")
    redirect_uri = 'https://example.com/'
    scopes = 'user-read-currently-playing%20playlist-modify-public%20playlist-modify-private%20playlist-read-private%20playlist-read-collaborative' 
    clickURL = 'https://accounts.spotify.com/authorize?client_id={}&response_type=code&redirect_uri={}&scope={}'.format(client_id, redirect_uri, scopes)

    print('\nClick the link below and sign-in:\n\n' + clickURL + '\n')
    redirectURL = input('After signing in, please copy the URL your browser redirected to and paste it here..\n\n')
    print('\nProcessing...')

    if '&' in redirectURL:
        posAmp = redirectURL.index('&')
        posEq  = redirectURL.index('=')
        code = redirectURL[posEq + 1 : posAmp]
        if('#' in code):
            posHash = code.index('#')
            code = code[:posHash]
    else:
        posEq  = redirectURL.index('=')
        code = redirectURL[posEq + 1 :]
        code.strip()
        if('#' in code):
            posHash = code.index('#')
            code = code[:posHash]

    URL = 'https://accounts.spotify.com/api/token'
    params = {
        'grant_type' : 'authorization_code',
        'code' : '{}'.format(code),
        'redirect_uri' : '{}'.format(redirect_uri)
    }

    string = client_id + ':' + client_secret
    string = base64.urlsafe_b64encode(string.encode()).decode()

    heads = {
        'Authorization' : 'Basic {}'.format(string)
    }
 
    response = requests.post(
        url= URL,
        data= params,
        headers=heads
    )
    response_json = response.json()

    access_token = response_json["access_token"]
    refresh_token = response_json["refresh_token"]

    print("History Generator Started!")

    MakeHistory()


def MakeHistory():
    global heads
    global timeElapsed

    while(timeElapsed < 3000):
        heads = {
            'Accept' : 'application/json',
            'Content-Type' : 'application/json',
            'Authorization' : 'Bearer {}'.format(access_token)
        }
        SongURI = getCurrentTrackInfo()
        PlaylistID = getPlaylistID()
        if(check(SongURI, PlaylistID)):
            addToPlaylist(SongURI, PlaylistID)
            if(checkLength(PlaylistID) == False):
                resizePlaylist(PlaylistID)
        else:
            print('Current song already added.')
        time.sleep(10)
        timeElapsed = timeElapsed + 15
    getRefreshedToken()


def getRefreshedToken():
    global string
    global timeElapsed
    global access_token
    global refresh_token

    print('Aquiring refreshed token...')

    URLrefresh = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type' : 'refresh_token',
        'refresh_token' : '{}'.format(refresh_token)
    }
    heads = {
        'Authorization' : 'Basic {}'.format(string)
    }

    response = requests.post(
        url= URLrefresh,
        headers= heads,
        data= payload
    )

    response = response.json()

    access_token = response['access_token']
    timeElapsed = 5

    MakeHistory()



def getCurrentTrackInfo():
    global heads
    global payload
    global timeElapsed

    response = requests.get(
        url= URL,
        params= payload,
        headers= heads
    )

    #ReqLimit = open('reqLimit.json','wb')
    #ReqLimit.writelines(response)
    #ReqLimit.close()

    if(response.status_code == 200): 
        response = response.json()
        if(response["item"] != None): 
            uri = response["item"]["uri"]
            return uri
        else: 
            print("Current track is a podcast, unable to add to History with current API limits.")
            timeElapsed = timeElapsed + 15
            time.sleep(10)
            MakeHistory()
    else:
        print('Nothing currently playing..')
        timeElapsed = timeElapsed + 15
        time.sleep(10)
        MakeHistory()



def getPlaylistID():
    response = requests.get(
        url= URLForPlaylist,
        headers=heads
    )

    response = response.json()

    for item in response['items']:
        if(item["name"] == 'History'):
            return item["id"]



def addToPlaylist(songURI, playlistID):
    payloadTwo = {
        'uris' : '{}'.format(songURI),
        'position' : '0'
    }
    URLForAdd = 'https://api.spotify.com/v1/playlists/{}/tracks'.format(playlistID)
    
    response = requests.post(
        url= URLForAdd,
        params= payloadTwo,
        headers= heads
    )

    if(response.status_code == 201):
        print("New song added to History.")


def check(songURI, playlistID):
    URLForAdd = 'https://api.spotify.com/v1/playlists/{}/tracks'.format(playlistID)
    payloadThree = {
        'market' : 'ES',
        'offset' : '0'
    }
    
    response = requests.get(
        url= URLForAdd,
        params= payloadThree,
        headers= heads
    )

    response = response.json()

    print('LAST SONG IN PLAYLIST NAME:\n' + response['items'][0]['track']['name'])

    if( response['items'][0]['track']['uri'] == songURI ):
        return False
    else:
        return True


def checkLength(playlistID):
    global target_length
    URLToFind = 'https://api.spotify.com/v1/playlists/{}'.format(playlistID)
    payloadFour = {
        'market' : 'ES'
    }

    response = requests.get(
        url= URLToFind,
        params= payloadFour,
        headers= heads
    )

    response = response.json()

    if(len(response['tracks']['items']) > target_length):
        return False
    else: 
        return True


def resizePlaylist(playlistID):
    global access_token
    global target_length

    print('Resizing playlist..')

    heads = {
        'Authorization' : 'Bearer {}'.format(access_token)
    }

    response = requests.get(
        url='https://api.spotify.com/v1/playlists/{}'.format(playlistID),
        headers = heads
    )

    response = response.json()

    playlistLength = len(response['tracks']['items'])
    print('Current size of History playlist: ' + str(playlistLength))

    uris = []

    for i in range(playlistLength - target_length):
        uris.append(response['tracks']['items'][target_length + i]['track']['uri'])
    
    print('Amount tracks to be removed for desired ' + '({})'.format(str(target_length)) + ' amount: ' + str(len(uris)))

    heads = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token)
    }

    songsArray = []
    for i in range(len(uris)):
        posArray = []
        posArray.clear()
        posArray.append(target_length + i)
        dic = {"uri" : "{}".format(uris[i]), "positions" : posArray}
        songsArray.append(dic)

    songsArray = json.dumps(songsArray)

    data = '{ \"tracks\":' + songsArray + '}'

    response = requests.delete(
        url= 'https://api.spotify.com/v1/playlists/{}/tracks'.format(playlistID),
        headers= heads,
        data= data
    )

    print(response)
    if(response.status_code == 200):
        print("Playlist resized to " + str(target_length) + ".")
    else:
        print("Error when trying to resize the playlist..")

if __name__ == '__main__':
    Initial_Authorization()