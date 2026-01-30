# Movie Data Parser & Report Generator

A Python command-line tool for parsing and analyzing movie datasets. Generate comprehensive reports about movies by year, genre, or popularity votes.

## Dataset

This project uses the IMDb Movies Dataset. You can download it from:
- **Kaggle**: [IMDb Movies Dataset](https://www.kaggle.com/datasets/omarhanyy/imdb-top-1000)
- Or use your own dataset with the same CSV structure

Place the dataset as `MoviesDataset.csv` in the project directory, or configure a custom path using the `.env` file.

## Features

- **Year Report** (`-r`): Analyze movies by year
  - Highest rated movie
  - Lowest rated movie
  - Average runtime
  
- **Genre Report** (`-g`): Analyze movies by genre
  - Total number of movies in genre
  - Average rating for the genre
  
- **Votes Report** (`-v`): Top 10 most voted movies by year
  - Visual representation with emoji indicators
  - Vote counts

## Installation

1. Clone or download this repository
2. Ensure Python 3.6+ is installed
3. No external dependencies required (uses standard library only)

## Configuration

### Option 1: Using `.env` file (Recommended)

Create a `.env` file in the project directory:

```env
MOVIES_CSV_PATH=C:\path\to\your\MoviesDataset.csv
```

### Option 2: Default Path

Place `MoviesDataset.csv` in the same directory as `movies_parser.py`

## Usage

### Basic Syntax

```bash
python movies_parser.py [OPTIONS]
```

### Options

- `-r YEAR` - Generate year report for specified year
- `-g GENRE` - Generate genre report for specified genre
- `-v YEAR` - Generate votes report (top 10) for specified year

### Examples

**Year Report:**
```bash
python movies_parser.py -r 2010
```
Output:
```
Highest rating: 8.8 - Inception
Lowest rating: 5.2 - The Last Airbender
Average mean minutes: 118.5
```

**Genre Report:**
```bash
python movies_parser.py -g Action
```
Output:
```
Movies found: 245
Average mean rating: 6.8
```

**Votes Report:**
```bash
python movies_parser.py -v 2010
```
Output:
```
Inception
👍👍👍👍👍👍👍👍👍👍 2300000
Toy Story 3
👍👍👍👍👍👍👍 820000
...
```

**Multiple Reports:**
```bash
python movies_parser.py -r 2010 -g Action -v 2010
```

## CSV Format

The dataset should be a CSV file with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `id` | string | Movie ID |
| `titleType` | string | Type of title (movie, short, etc.) |
| `originalTitle` | string | Original movie title |
| `startYear` | int | Release year (or `\N` for null) |
| `runtimeMinutes` | int | Runtime in minutes (or `\N` for null) |
| `genres` | string | Comma-separated genres |
| `rating` | float | Average rating (or `\N` for null) |
| `numVotes` | int | Number of votes (or `\N` for null) |

## Architecture

### Classes

- **`Movie`**: Data structure for individual movie information
- **`MovieParser`**: Handles CSV parsing and data loading
- **`YearReport`**: Data structure for year-based reports
- **`GenreReport`**: Data structure for genre-based reports
- **`VotesReport`**: Data structure for votes-based reports
- **`ReportBuilder`**: Generates and prints all report types

### Performance

- **Time Complexity**: O(1) lookups for year and genre queries using pre-indexed data structures
- **Pre-indexing**: Movies are indexed by year and genre at initialization for fast queries
- **Memory Efficient**: Uses heapq for top-k selection

## Error Handling

- Missing CSV file: Error message with path
- No data for query: "No data found" message
- Missing arguments: Usage help displayed
- Invalid environment: Fallback to default path

