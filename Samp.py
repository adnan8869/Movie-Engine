import argparse
import csv
import heapq
import os
import math


# Data structure for holding each movie's information
class Movie:
    """Class to hold individual movie information."""

    def __init__(self, movie_id, title_type, original_title, start_year,
                 runtime_minutes, genres, rating, num_votes):
        self.movie_id = movie_id
        self.title_type = title_type
        self.original_title = original_title
        self.start_year = start_year
        self.runtime_minutes = runtime_minutes
        self.genres = genres
        self.rating = rating
        self.num_votes = num_votes


# Class for parsing the file and populating the data structure
class MovieParser:
    """Class to parse CSV file and populate Movie objects."""

    def __init__(self, csv_path):
        self.csv_path = csv_path

    def load_movies(self):
        movies = []
        with open(self.csv_path, newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                start_year = None if row["startYear"] == "\\N" else int(row["startYear"])
                runtime_minutes = None if row["runtimeMinutes"] == "\\N" else int(row["runtimeMinutes"])
                rating = None if row["rating"] == "\\N" else float(row["rating"])
                num_votes = None if row["numVotes"] == "\\N" else int(row["numVotes"])
                
                movie = Movie(
                    movie_id=row["id"],
                    title_type=row["titleType"],
                    original_title=row["originalTitle"],
                    start_year=start_year,
                    runtime_minutes=runtime_minutes,
                    genres=row["genres"],
                    rating=rating,
                    num_votes=num_votes
                )
                movies.append(movie)
        return movies

# Data structures for holding the results of calculations
class YearReport:
    """Data structure for year-based report results."""

    def __init__(self, year, highest_rating, highest_movie,
                 lowest_rating, lowest_movie, avg_runtime):
        self.year = year
        self.highest_rating = highest_rating
        self.highest_movie = highest_movie
        self.lowest_rating = lowest_rating
        self.lowest_movie = lowest_movie
        self.avg_runtime = avg_runtime


class GenreReport:
    """Data structure for genre-based report results."""

    def __init__(self, genre, movies_count, avg_rating):
        self.genre = genre
        self.movies_count = movies_count
        self.avg_rating = avg_rating


class VotesReport:
    """Data structure for votes-based report results."""

    def __init__(self, year, top_movies):
        self.year = year
        self.top_movies = top_movies  # List of tuples (title, votes, likes)


# Class for creating the reports
class ReportBuilder:
    """Class to build various reports from movie data."""

    def __init__(self, movies):
        self.movies = movies

    def build_year_report(self, year):
        """Build report for a specific year."""
        # year_movies = [m for m in self.movies if m.start_year == year]
        year_movies = []
        for m in self.movies:
            if m.start_year == year:
                year_movies.append(m)
        if not year_movies:
            return None
                
        if not year_movies:
            return None
        highest_movie = max(year_movies, key=lambda x: x.rating)
        lowest_movie = min(year_movies, key=lambda x: x.rating)

        # Calculate average runtime
        # runtime_movies = [m for m in year_movies if m.runtime_minutes is not None]
        runtime_movies = []
        for m in year_movies:
            if m.runtime_minutes is not None:
                runtime_movies.append(m)

        avg_runtime = None
        if runtime_movies:
            total_runtime = 0
            for m in runtime_movies:
                minutes = m.runtime_minutes
                total_runtime += minutes
            avg_runtime = total_runtime / len(runtime_movies)

        return YearReport(
            year=year,
            highest_rating=highest_movie.rating,
            highest_movie=highest_movie.original_title,
            lowest_rating=lowest_movie.rating,
            lowest_movie=lowest_movie.original_title,
            avg_runtime=avg_runtime
        )

    def build_genre_report(self, genre):
        """Build report for a specific genre."""
        # genre_movies = [m for m in self.movies if genre in m.genres.split(',')]
        genre_movies = []
        for m in self.movies:
            if genre in m.genres.split(','):
                genre_movies.append(m)

        if not genre_movies:
            return None

        movies_count = len(genre_movies)

        
        avg_rating = None
        if genre_movies:
            total_rating = sum(m.rating for m in genre_movies)
            avg_rating = total_rating / len(genre_movies)

        return GenreReport(
            genre=genre,
            movies_count=movies_count,
            avg_rating=avg_rating
        )

    def build_votes_report(self, year):
        """Build votes report for a specific year."""
        # year_movies = [m for m in self.movies if m.start_year == year]
        year_movies = []
        for m in self.movies:
            if m.start_year == year and m.num_votes is not None:
                year_movies.append(m)

        if not year_movies:
            return None


        top_10 = heapq.nlargest(10, year_movies, key=lambda x: x.num_votes)

        # Calculate likes for top movie
        if top_10:
            max_votes =  math.ceil(top_10[0].num_votes / 80)
        else:
            max_votes = 0
        print(max_votes)

        top_movies = []
        for movie in top_10:
            likes = math.ceil(movie.num_votes / max_votes)
            print(likes)
            top_movies.append((movie.original_title, movie.num_votes, likes))

        return VotesReport(
            year=year,
            top_movies=top_movies
        )

    def print_year_report(self, report):
        """Print year report."""
        if report is None:
            print("No data found for the specified year.")
            return

        print(f"Highest rating:{report.highest_rating} - " f"{report.highest_movie}")
        print(f"Lowest rating:{report.lowest_rating} - " f"{report.lowest_movie}")
        if report.avg_runtime is None:
            print("Average mean minutes: N/A")
        else:
            print(f"Average mean minutes: {report.avg_runtime:.1f}")
            

    def print_genre_report(self, report):
        """Print genre report."""
        if report is None:
            print("No data found for the specified genre.")
            return

        print(f"Movies found: {report.movies_count}")
        if report.avg_rating is not None:
            print(f"Average mean rating: {report.avg_rating:.1f}")
        else:
            print("Average mean rating: N/A")

    def print_votes_report(self, report):
        """Print votes report."""
        if report is None:
            print("No data found for the specified year.")
            return

        for title, votes, likes in report.top_movies:
            like_symbols = "😀" * likes
            print(title)
            print(like_symbols, votes)


def load_env_file(env_path):
    """Load environment variables from .env file."""
    if not os.path.exists(env_path):
        return
    with open(env_path, "r", encoding="utf-8") as env_file:
        for line in env_file:
            stripped = line.strip()
            if "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Select report options to generate single or multiple reports."
    )
    parser.add_argument(
        "-r",
        type=int,
        metavar="YEAR",
        help="Generate year report: highest and lowest rating and average runtime"
    )
    parser.add_argument(
        "-g",
        type=str,
        metavar="GENRE",
        help="Generate genre report: number of movies and mean rating"
    )
    parser.add_argument(
        "-v",
        type=int,
        metavar="YEAR",
        help="Generate votes report: top 10 movies with vote visualization"
    )
    return parser.parse_args()


def validate_args(args):
    """Validate command line arguments."""
    if not args.r and not args.g and not args.v:
        raise SystemExit(
            "Error: At least one report option (-r, -g, or -v) is required."
        )


def resolve_csv_path():
    """Resolve CSV file path from environment variable."""
    env_path = os.getenv("MOVIES_CSV_PATH")
    if not env_path:
        # Fallback to default path
        default_path = os.path.join(
            os.path.dirname(__file__),
            "movies_dataset.csv"
        )
        if os.path.isfile(default_path):
            return default_path
        raise SystemExit(
            "Error: MOVIES_CSV_PATH environment variable not set."
        )
    if not os.path.isfile(env_path):
        raise SystemExit(
            f"Error: File not found at MOVIES_CSV_PATH: {env_path}"
        )
    return env_path


def main():
    # Load environment variables
    load_env_file(os.path.join(os.path.dirname(__file__), ".env"))

   
    args = parse_args()
    validate_args(args)

   
    csv_path = resolve_csv_path()

    parser = MovieParser(csv_path)
    movies = parser.load_movies()

    report_builder = ReportBuilder(movies)

    report_count = 0
    if args.r:
        if report_count > 0:
            print() 
        report = report_builder.build_year_report(args.r)
        report_builder.print_year_report(report)
        report_count += 1

    if args.g:
        if report_count > 0:
            print()  
        report = report_builder.build_genre_report(args.g)
        report_builder.print_genre_report(report)
        report_count += 1

    if args.v:
        if report_count > 0:
            print()  
        report = report_builder.build_votes_report(args.v)
        report_builder.print_votes_report(report)
        report_count += 1


if __name__ == "__main__":
    main()