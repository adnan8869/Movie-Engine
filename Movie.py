import argparse
import csv
import os


class Movie:
	def __init__(self, title, org_title, year, duration, genre, rating, votes):
		self.title = title
		self.org_title = org_title
		self.year = year
		self.duration = duration
		self.genre = genre
		self.rating = rating
		self.votes = votes


class MovieParser:
	def __init__(self, csv_path):
		self.csv_path = csv_path

	def load_movies(self):
		movies = []
		with open(self.csv_path, newline="", encoding="utf-8") as csv_file:
			reader = csv.DictReader(csv_file)
			for row in reader:
				movies.append(self._parse_row(row))
		return movies

	def _parse_row(self, row):
		return Movie(
			title=self._clean_text(row.get("title")),
			org_title=self._clean_text(row.get("Orgtitle")),
			year=self._to_int(row.get("year")),
			duration=self._to_int(row.get("duration")),
			genre=self._clean_text(row.get("genre")),
			rating=self._to_float(row.get("rating")),
			votes=self._to_int(row.get("votes")),
		)

	def _clean_text(self, value):
		if value is None:
			return ""
		return value.strip()

	def _to_int(self, value):
		if value is None:
			return None
		value = value.strip()
		if not value or value == "\\N":
			return None
		return int(value)

	def _to_float(self, value):
		if value is None:
			return None
		value = value.strip()
		if not value or value == "\\N":
			return None
		return float(value)


class MovieReport:
	def __init__(self, total_movies, average_rating):
		self.total_movies = total_movies
		self.average_rating = average_rating


class ReportBuilder:
	def __init__(self, movies):
		self.movies = movies

	def build(self):
		ratings = []
		for movie in self.movies:
			if movie.rating is not None:
				ratings.append(movie.rating)

		average_rating = None
		if ratings:
			average_rating = sum(ratings) / len(ratings)

		return MovieReport(len(self.movies), average_rating)

	def print_report(self, report):
		print(f"Total movies: {report.total_movies}")
		if report.average_rating is None:
			print("Average rating: N/A")
		else:
			print(f"Average rating: {report.average_rating:.2f}")


def load_env_file(env_path):
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
	parser = argparse.ArgumentParser(description="Simple movie report.")
	parser.add_argument(
		"csv_path",
		nargs="?",
		help="Path to MoviesDataset.csv (optional).",
	)
	return parser.parse_args()


def resolve_csv_path(arg_path):
	if arg_path:
		if not os.path.isfile(arg_path):
			raise SystemExit("Provided CSV path does not exist.")
		return arg_path

	env_path = os.getenv("MOVIES_CSV_PATH")
	if not env_path:
		raise SystemExit(
			"Missing CSV path. Set MOVIES_CSV_PATH or pass a path."
		)
	if not os.path.isfile(env_path):
		raise SystemExit("MOVIES_CSV_PATH points to a missing file.")
	return env_path


def main():
	load_env_file(os.path.join(os.path.dirname(__file__), ".env"))
	args = parse_args()
	csv_path = resolve_csv_path(args.csv_path)

	parser = MovieParser(csv_path)
	movies = parser.load_movies()
	report_builder = ReportBuilder(movies)
	report = report_builder.build()
	report_builder.print_report(report)


if __name__ == "__main__":
	main()
