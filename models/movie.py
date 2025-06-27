class MovieModel:
    def __init__(self, id, title, director, year, genre, synopsis):
        self.id = id
        self.title = title
        self.director = director
        self.year = year
        self.genre = genre
        self.synopsis = synopsis

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'director': self.director,
            'year': self.year,
            'genre': self.genre,
            'synopsis': self.synopsis
        }

    @classmethod
    def from_dict(cls, data):    
        return cls(
            id=data.get('id'),
            title=data.get('title'),
            director=data.get('director'),
            year=data.get('year'),
            genre=data.get('genre'),
            synopsis=data.get('synopsi')
        )