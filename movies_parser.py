import csv
import os


def load_env_file(env_path):
    if not os.path.exists(env_path):
        return
    with open(env_path, "r", encoding="utf-8") as env_file:
        for line in env_file:
            stripped = line.strip()
            key, value = stripped.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def main():
    load_env_file(os.path.join(os.path.dirname(__file__), ".env"))
    csv_path = os.getenv("MOVIES_CSV_PATH")
    # if not csv_path:
    #     csv_path = os.path.join(os.path.dirname(__file__), "MoviesDataset.csv")

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            print(row)


if __name__ == "__main__":
    main()