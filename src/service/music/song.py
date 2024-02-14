
class Song():
    def __init__(self):
        self._title = None
        self._artist = None
        self._id = None

    def __init__(self, title, artist, id) -> None:
        self._title = title
        self._artist = artist
        self._id = id

    @property
    def title(self):
        return self._title
    
    @property
    def artist(self):
        return self._artist
    
    @property
    def id(self):
        return self._id
    
    @property
    def url(self):
        return "https://www.youtube.com/watch?v=" + self._id
    