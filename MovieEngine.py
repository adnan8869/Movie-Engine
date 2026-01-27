class MovieEngine:
    def __init__(self):
        self.movies = []

    def add_movie(self, titleType, originalTitel, startYear, runtimeMinutes=None, genres=None, rating=None, numVotes=None):
        movie = {
            'titleType': titleType,
            'originalTitel': originalTitel,
            'startYear': startYear,
            'runtimeMinutes': runtimeMinutes,
            'genres': genres,
            'rating': rating,
            'numVotes': numVotes
        }
        self.movies.append(movie)
    def get_movies(self):
        return self.movies
    

Movie = MovieEngine()
Movie.add_movie("movie", "Miss Jerry", 1894, 45, "Romance", 5.9, 156)
Movie.add_movie("short", "Carmentica", 1894, 1, "Documentary,Short", 5.6, 1652)


print(Movie.get_movies())