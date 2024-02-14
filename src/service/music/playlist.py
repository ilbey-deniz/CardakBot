from service.music.song import Song

class Playlist():
    def __init__(self) -> None:
        self._playlist = []
        self._current_song = None

    @property
    def playlist(self) -> list:
        return self._playlist
    
    @property
    def current_song(self) -> Song:
        return self._current_song

    def add_song(self, song: Song) -> None:
        self._playlist.append(song)

    def remove_song(self, song: Song) -> None:
        self._playlist.remove(song)

    def next_song(self) -> Song:
        self._current_song = self._playlist.pop(0)
        return self._current_song
    
    def is_empty(self) -> bool:
        return len(self._playlist) == 0
    
    def clear(self) -> None:
        self._playlist = []
        self._current_song = None

    def insert_after_current(self, song: Song) -> None:
        self._playlist.insert(1, song)

        
        

