# StreamPick — Movie Recommendation Engine using Item-Based Collaborative Filtering

## Project Overview

This project builds an item-based movie recommendation engine using collaborative filtering (K-Nearest Neighbors). The model finds movies that are similar based on how users have rated them (user behavior), rather than relying on genres or manual metadata.

This repository is a minimal, reproducible implementation aimed at a College-level project and includes an example `recommender.py` script that leverages the MovieLens small dataset. The project is also branded as **StreamPick** — a minimal movie recommender demo and UI to showcase item-based collaborative filtering.

---

## Problem Statement

Users face choice paralysis on streaming platforms with thousands of titles. A simple search is often insufficient to recommend movies a user will enjoy. The task is to predict a user's preference for an unseen movie using historical user ratings only (no content tags), using item-based collaborative filtering.

---

## Proposed Solution

We propose an item-based collaborative filtering K-Nearest Neighbors (KNN) approach with cosine similarity on a sparse movie-user matrix. The model identifies movies that have similar rating patterns across users.

Key idea: If users who rated Movie A highly also rate Movie B highly, then A and B are similar.

---

## Project Structure

- `README.md` - This file.
- `recommender.py` - The sample Python script implementing the item-based KNN recommender.
- `requirements.txt` - Python dependencies for quick setup.
- `movies.csv`, `ratings.csv` - CSV files from the MovieLens (ml-latest-small) dataset.

---

## Dataset

We recommend the MovieLens Small Dataset (ml-latest-small):
- Download: https://grouplens.org/datasets/movielens/latest/
- Extract and copy `movies.csv` and `ratings.csv` to the project root.

---

## Requirements

- Python 3.9+ (Python 3.8 also works)
- pip

Install dependencies using:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
```
Install dependencies using a virtual environment (recommended) or install globally if you prefer.

Virtual environment (recommended):
```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate
pip install -r requirements.txt
```

Without creating a virtual environment (install packages globally):
```powershell
pip install -r requirements.txt
pandas
scikit-learn
scipy
numpy
```

---

## How it works

# Quick dataset download (no environment required) - download and extract movieLens ml-latest-small to the current folder
$zipUrl = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"; Invoke-WebRequest -Uri $zipUrl -OutFile "ml-latest-small.zip"; Expand-Archive -Path "ml-latest-small.zip" -DestinationPath "." -Force; Move-Item -Path "./ml-latest-small/movies.csv" -Destination "./movies.csv" -Force; Move-Item -Path "./ml-latest-small/ratings.csv" -Destination "./ratings.csv" -Force; Remove-Item "ml-latest-small.zip"; Remove-Item -Recurse -Force "./ml-latest-small"

# (If you prefer to run w/ venv, activate it as shown in the installation section)
python recommender.py --movie "Iron Man" --n_neighbors 6
1. Load `movies.csv` and `ratings.csv`.
2. Pivot ratings into a movie-user matrix (rows=movies, columns=users).
You can modify the sample `input_movie` by passing `--movie` text to the script (e.g., `--movie "Toy Story"`) or change `--n_neighbors` to get more/less recommendations.
4. Build a KNN model on movie vectors with cosine similarity.
5. Provide recommendations for a given movie by finding nearest neighbors.

---

## Example Usage

Open PowerShell and run:

```powershell
# Activate environment (if you created one)
.\.venv\Scripts\Activate

# Simple run
python recommender.py
```

You can modify the sample `input_movie` variable in `recommender.py` or adapt the script to accept CLI args.

---

## Example Output

When using the sample script and inputting a movie like "Iron Man" you might see output similar to:

```
Because you liked 'Iron Man':
1: The Avengers (Match: 95.60%)
2: Captain America: The First Avenger (Match: 94.20%)
3: Thor (Match: 88.12%)
4: X-Men (Match: 85.89%)
5: Batman Begins (Match: 82.40%)
```

Numbers vary depending on dataset, pre-processing, and how many neighbors are requested.

---

## Notes & Tips

- This is an educational implementation. For production on large datasets:
  - Use optimized nearest-neighbor libraries (Faiss, Annoy) for large-scale, approximate NN search.
  - Parallelize processing and use partitioned data or a recommendation service.
  - Consider adding user-based collaborative filtering as a complement.

- The MovieLens dataset has explicit ratings (1-5). To handle implicit feedback (views, clicks), adapt the approach by weighting or transforming signals.

---

## Future Work / Extensions

- Build a web UI (Streamlit/Flask/React) and an API to serve recommendations.
- Add personalization by combining item-based and user-based scores.
- Use SVD or matrix factorization approaches for dimensionality reduction.
- Explore content-based filtering using movie metadata (genres, cast) for cold-start problems.

---

## License & Acknowledgements

This repository is free to use for educational purposes. The MovieLens dataset belongs to GroupLens research.

Acknowledgements: GroupLens for the dataset and scikit-learn/pandas for easy prototyping.

---

## Contact

If you use this for a project or GitHub repo, feel free to add your name and project details.

Happy building! 

``` 
# End of README
```

---

## Run the Web App (FastAPI + Static Frontend)

This repo includes a Netflix-like static frontend in the `frontend/` folder and a FastAPI backend in `api.py` that uses your recommender logic.

Install server dependencies (if not installed already):

```powershell
pip install -r requirements.txt
```

Run the server:

```powershell
uvicorn api:app --reload --port 8000
```

Open the page in a browser at: http://127.0.0.1:8000/

Type a movie name in the search box and click "Recommend" to see Netflix-like rows of recommendations.

---

## How to compile the LaTeX report

The project contains a detailed report `report/MovieRecommender_Report.tex`. To compile:

Windows PowerShell or Linux (assuming a TeX distribution is installed):
```powershell
cd report
pdflatex MovieRecommender_Report.tex
pdflatex MovieRecommender_Report.tex
```

This will produce `MovieRecommender_Report.pdf` containing the 10-page report with a pipeline diagram and placeholders for results.

