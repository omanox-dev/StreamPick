import argparse
import os
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

# --- STEP 1: LOAD DATA ---
print("Loading dataset...")

# --- DATASET DISCOVERY ---
def find_file(name):
    candidates = [name, os.path.join('ml-latest-small', name)]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

movies_path = find_file('movies.csv')
ratings_path = find_file('ratings.csv')

if movies_path is None or ratings_path is None:
    raise FileNotFoundError('Could not find movies.csv or ratings.csv in the project root or ml-latest-small folder. Please download the MovieLens ml-latest-small dataset and place the CSVs in the project root.')

movies = pd.read_csv(movies_path)  # Contains movieId, title
ratings = pd.read_csv(ratings_path) # Contains userId, movieId, rating

# --- STEP 2: PREPROCESSING (The Pivot) ---
# We create a matrix where rows are movies and columns are users.
# This matrix tells us HOW users rated specific movies.
movie_user_matrix = ratings.pivot(index='movieId', columns='userId', values='rating')

# Fill NaN with 0 (0 indicates the user hasn't watched/rated the movie)
movie_user_matrix.fillna(0, inplace=True)

# Convert to Compressed Sparse Row (CSR) matrix to save memory and speed up math
movie_csr = csr_matrix(movie_user_matrix.values)

# --- STEP 3: MODEL TRAINING (KNN) ---
# Metric = cosine (calculates angle between vectors)
# Algorithm = brute (compares every vector against every other vector)
model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20)
model_knn.fit(movie_csr)

print("Model Trained successfully!")


def get_recommendations(movie_name, movie_user_matrix_local=None, model_local=None, movies_df=None, n_neighbors=6):
    """Return the movie title and list of recommendation dicts for the given movie name.

    The returned structure is (movie_title or error_message, list_of_recs)
    Each rec is a dict: {movieId, title, score}
    """
    if movie_user_matrix_local is None:
        movie_user_matrix_local = movie_user_matrix
    if model_local is None:
        model_local = model_knn
    if movies_df is None:
        movies_df = movies
    movie_list = movies_df[movies_df['title'].str.contains(movie_name, case=False, na=False)]
    if len(movie_list) == 0:
        return "Movie not found. Please check the spelling.", []
    movie_idx = movie_list.iloc[0]['movieId']
    movie_title = movie_list.iloc[0]['title']
    try:
        query_index = movie_user_matrix_local.index.get_loc(movie_idx)
        distances, indices = model_local.kneighbors(
            movie_user_matrix_local.iloc[query_index, :].values.reshape(1, -1),
            n_neighbors=n_neighbors,
        )
        recs = []
        for i in range(1, len(distances.flatten())):
            result_movie_id = movie_user_matrix_local.index[indices.flatten()[i]]
            result_title = movies_df[movies_df['movieId'] == result_movie_id]['title'].values[0]
            similarity = (1 - distances.flatten()[i]) * 100
            recs.append({"movieId": int(result_movie_id), "title": result_title, "score": float(similarity)})
        return movie_title, recs
    except KeyError:
        return "Movie ID found in list but not in matrix (likely not enough ratings).", []

# --- STEP 4: RECOMMENDATION FUNCTION ---
def recommend_movie(movie_name, n_neighbors=6):
    # 1. Find the Movie ID from the string name
    movie_list = movies[movies['title'].str.contains(movie_name, case=False, na=False)]

    if len(movie_list) == 0:
        return "Movie not found. Please check the spelling."

    # Get the index and ID of the first match
    movie_idx = movie_list.iloc[0]['movieId']
    movie_title = movie_list.iloc[0]['title']

    try:
        # Get the row location in the matrix for this movieId
        query_index = movie_user_matrix.index.get_loc(movie_idx)

        # 2. Ask the Model for Neighbors
        distances, indices = model_knn.kneighbors(
            movie_user_matrix.iloc[query_index,:].values.reshape(1, -1), 
            n_neighbors=n_neighbors
        )

        # 3. Format Output
        print(f"\nBecause you liked '{movie_title}':")
        for i in range(1, len(distances.flatten())):
            result_movie_id = movie_user_matrix.index[indices.flatten()[i]]
            result_title = movies[movies['movieId'] == result_movie_id]['title'].values[0]
            similarity = (1 - distances.flatten()[i]) * 100
            print(f"{i}: {result_title} (Match: {similarity:.2f}%)")

    except KeyError:
        return "Movie ID found in list but not in matrix (likely not enough ratings)."

# --- CLI and TEST RUN ---
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Item-based movie recommender (KNN)')
    parser.add_argument('--movie', '-m', type=str, default='Iron Man', help='Movie title (or part of it) to query for recommendations')
    parser.add_argument('--n_neighbors', '-k', type=int, default=6, help='Number of neighbors to return')
    args = parser.parse_args()

    print(f"Movies dataset: {movies_path}")
    print(f"Ratings dataset: {ratings_path}")
    print(f"Movies total: {len(movies)} | Ratings total: {len(ratings)}")
    recommend_movie(args.movie, n_neighbors=args.n_neighbors)
