# Movie Picker

Movie Picker is a Python CLI application that recommends a movie from your Letterboxd watchlist based on your preferences.

The application synchronizes the Letterboxd watchlist, enriches movie data using the TMDb API, stores data locally, and selects a movie using weighted random recommendations.

## Features

- Import movies from a Letterboxd watchlist
- Support multi-page Letterboxd watchlists
- Fetch movie metadata from TMDb
- Match Letterboxd movies with TMDb entries
- Local caching of movie data
- Avoid repeated TMDb requests for already known movies
- Preserve movies removed from the Letterboxd watchlist
- Ignore unsupported TV shows without requesting them repeatedly
- Filter movies by:
  - genre
  - release year range
  - country
  - maximum runtime
  - minimum TMDb rating
- Weighted random recommendations
- Reduce the probability of repeatedly recommending the same movie
- Mark movies as watched
- Retry temporary TMDb network errors
- Use cached local data when synchronization is unavailable
- Automated tests with pytest
- GitHub Actions CI

## How it works

The application uses Letterboxd as the source of the user's watchlist and TMDb as the source of detailed movie metadata.

```text
Letterboxd Watchlist
        |
        v
Letterboxd Client
        |
        v
Synchronization Service
        |
        +------> Local JSON Storage
        |
        +------> TMDb API
                    |
                    v
              Movie Metadata
                    |
                    v
               Movie Filter
                    |
                    v
             Weighted Picker
                    |
                    v
            CLI Recommendation
```

During synchronization, movies already stored locally are reused. TMDb requests are made only for newly discovered movies.

If a movie is removed from the Letterboxd watchlist, its local history is preserved, but it is excluded from future recommendations.

## Requirements

- Python 3.12+
- Letterboxd account
- TMDb API Read Access Token

## Installation

1. Clone the repository:

```bash
git clone https://github.com/chumbitups/movie-picker.git
cd movie-picker
```

2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

For development and running tests:

```bash
pip install -r requirements-dev.txt
```

## Configuration

Create a .env file based on .env.example:

```bash
cp .env.example .env
```

Then configure:

```env
TMDB_TOKEN=your_tmdb_api_read_token
LETTERBOXD_USERNAME=your_letterboxd_username
```

The .env file contains local credentials and is excluded from Git.

## Usage

Run the application:

```bash
python3 main.py
```

On startup, the application synchronizes your Letterboxd watchlist with the local cache and fetches TMDb data only for newly discovered movies.

You can then specify optional filters:

```text
Genre (empty = any): drama
Year from (empty = any): 2000
Year to (empty = any): 2025
Country (empty = any): United States of America
Max runtime in minutes (empty = any): 130
Min rating 0-10 (empty = any): 7.0
```

The application will recommend a matching movie:

```text
Arrival (2016)

Rating: 7.6
Runtime: 116 Minutes
Genres: Drama, Science Fiction
Countries: United States of America
```

After receiving a recommendation, choose an action:

```text
1 - I watched this
2 - Recommend another with same filters
3 - Change filters
0 - Exit
```

If synchronization with Letterboxd or TMDb is temporarily unavailable, the application falls back to the locally cached movie data.

## Tests

The project uses `pytest` for automated testing.

Run all tests with:

```bash
python -m pytest -v
```

The test suite covers movie filtering, weighted recommendations, local storage, Letterboxd parsing and pagination, TMDb matching, synchronization logic, retry handling, and fallback behavior.

## CI

The repository uses GitHub Actions to run the test suite automatically on every push and pull request.

The CI workflow:

```text
Checkout repository
        |
        v
Set up Python 3.12
        |
        v
Install development dependencies
        |
        v
Run pytest
```

The workflow configuration is located at:

```text
.github/workflows/tests.yml
```

## Project structure
```text
movie-picker/
├── main.py
├── models.py
├── picker.py
├── sync_service.py
├── letterboxd_client.py
├── tmdb_client.py
├── storage.py
│
├── data/
│   ├── movies.json
│   └── unmatched.json
│
├── tests/
│   ├── test_picker.py
│   ├── test_storage.py
│   ├── test_tmdb_client.py
│   ├── test_letterboxd_client.py
│   └── test_sync_service.py
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
└── README.md
```
### Main modules

- `main.py` — CLI entry point, user input, application flow and offline fallback.
- `models.py` — domain models such as `Movie`, `WatchlistItem` and `MovieFilter`.
- `picker.py` — movie filtering, weighted random selection and recommendation logic.
- `letterboxd_client.py` — Letterboxd watchlist downloading, parsing and pagination.
- `tmdb_client.py` — TMDb API integration, movie matching and metadata retrieval.
- `sync_service.py` — synchronization between Letterboxd, TMDb and locally cached data.
- `storage.py` — JSON persistence for movies and unmatched watchlist entries.
- `tests/` — automated pytest test suite.
- `.github/workflows/tests.yml` — GitHub Actions CI workflow.
