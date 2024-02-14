from ytmusicapi import YTMusic
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from service.music.song import Song
from spotipy.exceptions import SpotifyException
import os

class YTMusicUtils:
    def __init__(self):
        oauth = os.getenv("YTMUSIC_OAUTH")
        self.ytmusic = YTMusic(oauth)
        auth_manager = SpotifyClientCredentials()
        self.sp = spotipy.Spotify(auth_manager= auth_manager)

    #check if the query is a url: if it is a youtube url, simply return the song
    #if it is a spotify url, get the song name and search for it over ytmusic
    #if it is a search query, search for it over ytmusic
    def getSongByQuery(self, query) -> Song:
        song = None
        if "https://www.youtube.com/watch?v=" in query:
            video_id = query.split("watch?v=")[1]
            song_info = self.ytmusic.get_song(video_id)
            song = Song(song_info["title"], song_info["artists"][0]["name"], video_id)

        elif "open.spotify.com/track/" in query:
            try:
                track = self.sp.track(query)
                song_name = track["name"]
                artist = track["artists"][0]["name"]
                search_results = self.ytmusic.search(query=song_name + " " + artist, filter="songs")
                video_id =  search_results[0]["videoId"]
                song = Song(song_name, artist, video_id)
            except SpotifyException as e:
                print("spotipy exception: " + e)
            
        else:
            search_results = self.ytmusic.search(query=query, filter="songs")
            song = Song(search_results[0]["title"], search_results[0]["artists"][0]["name"], search_results[0]["videoId"])

        return song