from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import urllib.parse

from recommender import get_recommendations

# A small util to provide poster URLs (placeholder images)
def poster_url(movie_id, width=300, height=450):
    # deterministic placeholder using picsum.photos seed
    return f"https://picsum.photos/seed/{movie_id}/{width}/{height}"

app = FastAPI(title="StreamPick — Movie Recommender API")

# Serve the static frontend directory at root
app.mount("/static", StaticFiles(directory="frontend"), name="static")

class RecRequest(BaseModel):
    movie: str
    k: int = 6

class RecItem(BaseModel):
    movieId: int
    title: str
    score: float
    poster: str

class RecResponse(BaseModel):
    query: str
    recommendations: List[RecItem]

@app.get('/')
def index():
    # Return the frontend index file
    return FileResponse('frontend/index.html')

@app.get('/api/recommend', response_model=RecResponse)
def recommend(movie: str, k: int = 6):
    if not movie:
        raise HTTPException(status_code=400, detail='Missing movie query parameter')
    title, items = get_recommendations(movie, n_neighbors=k)
    if isinstance(items, list) and len(items) > 0:
        results = []
        for r in items:
            results.append({
                'movieId': r['movieId'],
                'title': r['title'],
                'score': r['score'],
                'poster': poster_url(r['movieId'])
            })
        return { 'query': title, 'recommendations': results }
    else:
        # return empty recommendation list, convey message via 'query' if title is a message
        if isinstance(title, str):
            return { 'query': title, 'recommendations': [] }
        return { 'query': movie, 'recommendations': [] }

# Health check
@app.get('/api/health')
def health():
    return { 'status': 'ok' }
