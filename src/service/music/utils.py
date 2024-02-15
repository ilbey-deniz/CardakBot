from ytmusicapi import YTMusic
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from service.music.song import Song
from service.music.playlist import Playlist
from spotipy.exceptions import SpotifyException
from urllib.parse import urlparse, parse_qs
import os

## GENERAL TODO: check for search match rate, if it is too low, return None

class YTMusicUtils:
    def __init__(self):
        oauth = os.getenv("YTMUSIC_OAUTH")
        self.ytmusic = YTMusic(oauth)
        auth_manager = SpotifyClientCredentials()
        self.sp = spotipy.Spotify(auth_manager= auth_manager)
        self.playlist_patterns = [
            "www.youtube.com/playlist?list=", 
            "open.spotify.com/playlist/",
            "music.youtube.com/playlist?list="
            ]

    #check if the query is a url: if it is a youtube url, simply return the song
    #if it is a spotify url, get the song name and search for it over ytmusic
    #if it is a search query, search for it over ytmusic
    def get_song_by_query(self, query) -> Song:
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
    
    def is_playlist(self, query) -> bool:
        if any(pattern in query for pattern in self.playlist_patterns):
            return True
        return False

    #if the link is a playlist, get the songs from the playlist
    #if the link is a song, get the song and get similar songs
    def get_playlist_by_query(self, query) -> Playlist:
        playlist = Playlist()
        if self.is_playlist(query):
            if "open.spotify.com/playlist/" in query:
                playlist = self.get_spotify_playlist(query)
            else:
                playlist = self.get_YT_playlist(query)
        return playlist
        
    
    #playlist url is in form "https://music.youtube.com/playlist?list=RDCLAK5uy_nkN2Fde5lIJN38ta7Tyvr8Uona03aHnRo&playnext=1&si=9HodbWDKf20frqIt"
    def get_YT_playlist(self, query) -> Playlist:
        playlist = Playlist()
        parsed_query = urlparse(query)
        playlist_id = parse_qs(parsed_query.query)["list"][0]
        playlist_info = self.ytmusic.get_playlist(playlist_id)
        for track in playlist_info["tracks"]:
            song = Song(track["title"], track["artists"][0]["name"], track["videoId"])
            playlist.add_song(song)
        return playlist
    
    def get_spotify_playlist(self, query) -> Playlist:
        #optimization is needed, 100 song playlist may take a while
        #some songs may not be found, need to handle that
        playlist = Playlist()
        parsed_query = urlparse(query)
        playlist_id = parsed_query.path.split("/")[2]
        playlist_info = self.sp.playlist_tracks(playlist_id)
        for track in playlist_info["items"]:
            song_name = track["track"]["name"]
            artist = track["track"]["artists"][0]["name"]
            search_results = self.ytmusic.search(query=song_name + " " + artist, filter="songs", limit=1)
            video_id =  search_results[0]["videoId"]
            song = Song(song_name, artist, video_id)
            playlist.add_song(song)
        return playlist