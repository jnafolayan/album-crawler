
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
        self.id = None
        self.file_path = ''

        if self.album is None:
            single_name = '{} - Single'.format(self.title)
            self.album = Album(name=single_name, artiste=self.artiste)
            self.album.add_track(self)

    def __str__(self):
        """
        creates a string representation in format:
        `id - title ft. features - artiste`
        """
        return '{} - {} - {}'.format(self.id, self.title_to_string,
                                     self.artiste_to_string)

    def __repr__(self):
        return '<Track: {}>'.format(self.title)

    @property
    def search_term(self):
        return '{} {}'.format(self.title, ' '.join(self.artiste))

    @property
    def artiste_to_string(self):
        return ', '.join(self.artiste)

    @property
    def title_to_string(self):

        try:
            for artiste in self.artiste:
                self.features.remove(artiste)
        except ValueError:
            pass

        if len([ft for ft in self.features if ft in self.title]) ==\
                len(self.features):
            return '{}'.format(self.title)

        elif len(self.features) == 0:
            return '{}'.format(self.title)

        else:
            features = 'ft. ' + ', '.join(self.features)
            return '{} {}'.format(self.title, features)


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
        self.cover_art_path = ''

    def __str__(self):
        return str(self.tracklist)

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise ValueError('Index must be an int')
        if index < len(self.tracklist):
            return self.tracklist[index]
        else:
            raise IndexError('Index out of range.')

    @property
    def to_string(self):
        return '{} - {}'.format(self.name, ', '.join(self.artiste))

    def add_track(self, track: Track):
        if not isinstance(track, Track):
            raise TypeError('Album class only accepts Track objects')
        track.id = len(self.tracklist) + 1
        self.tracklist.append(track)
