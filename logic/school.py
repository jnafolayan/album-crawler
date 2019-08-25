
class Track:
    def __init__(self, title: str, artiste: list, features=[], album=None):
        """
        :params title: string containing track title
        :params artiste: list containing strings of artiste names as multiple
                         artistes may own a track.
        :params features: list of artistes featured on the track
        :params album: Album object that encapsulates track. If set to none,
                       an Album class will be instantiated with the name set to
                       `[track.name] - Single`
        :params download_link: string URI link for the track
        """
        self.title = title
        self.artiste = artiste
        self.features = features
        self.download_link = ''
        self.album = album

        if self.album is None:
            single_name = '{} - Single'.format(self.title)
            self.album = Album(name=single_name, artiste=self.artiste)
            self.album.add_track(self)

    def __str__(self):
        """
        creates a string representation in format:
        `title ft. features - artiste`
        """
        features = 'ft. ' + ', '.join(self.features) if self.features else ''
        artiste = ', '.join(self.artiste)
        return '{} {} - {}'.format(self.title, features, artiste)

    def __repr__(self):
        return '<Track: {}>'.format(self.title)


class Album:
    def __init__(self, name: str, artiste: list):
        """
        :params name: string name of the album
        :params artiste: list of strings of artiste names and more than one
                        artiste can own an album
        :params tracklist: an ordered list of tracks in the album
        :params cover_art_link: string URI for the cover art
        """
        self.name = name
        self.artiste = artiste
        self.tracklist = []
        self.cover_art_link = ''

    def __str__(self):
        return self.tracklist

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise ValueError('Index must be an int')
        if index < len(self.tracklist):
            return self.tracklist[index]
        else:
            raise IndexError('Index out of range.')

    def add_track(self, track: Track):
        if not isinstance(track, Track):
            raise TypeError('Album class only accepts Track objects')
        self.tracks.append(track)