# Spotify-History-Generator 🎵
A Python project utilizing Spotify's Web API to create your very own easily accessable History playlist.

## What the generator does:
After all setup has been complete and the below dependencies fulfilled, the generator should consistently update a playlist named "History" under your own personal playlists on Spotify. 

## Dependencies: 📃
* A Spotify account (it does not have to be a premium account).
* Something to continuously run the Python script. 
* A constant internet connection, including any devices playing music from Spotify and the device running the Python script. 
* A registered application on the Spotify developer dashboard (don't worry, its easy and free).
* A playlist named "History" in which you have made on your Spotify account. It can be either public or private.
* Assurance you are not in a "private listening session" on Spotify.

## Setup: 🏃‍♀️💨
* Code Dependencies:

The first thing you should check is that you have Python installed along with a few dependencies used by the script. These depenndencies include:
  Python requests.
* Developer Dashboard Application:

On https://developer.spotify.com/dashboard/ , sign into your Spotify account and create a new application. After creation, add "https://example.com/" to the list of Redirect URIs after clicking "edit settings" in your new dashboard application. 
Now, on the main page of your application, take note of the "client ID" and "client secret" as you will need these when starting up the generator. 

* Spotify playlist:

Create a playlist called exactly "History" (without the double quotes). 

WARNING: If you already have a playlist named "History" and have songs which you have added, the playlist will be manipulated by the generator and songs might be removed.

* Start the Python script!

Open the Python file and follow the text-based commands of the script. Keep it open in order for the history to be generated and close the script window when you want it to stop.
 
 
 
 
## Future changes and community contributions ✨👨‍💻

You are more than welcome to submit a push request if you feel you can add a useful change to the code!

Some possible improvements I will be working towards for future implementation are:
* Cleaner variable names
* Independent generation of the "History" playlist by the generator
* Better user interface
* Possibility to run as a background process
* A Python executable to skip most of the code setup process
* Podcast support (not currently available in the normal Spotify API)
