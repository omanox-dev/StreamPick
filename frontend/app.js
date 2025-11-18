const API_BASE = '/api';

async function fetchRecommendations(movie, k=6) {
  const url = `${API_BASE}/recommend?movie=${encodeURIComponent(movie)}&k=${k}`;
  const res = await fetch(url);
  if (!res.ok) {
    const data = await res.json();
    return { error: data.detail || 'API error' };
  }
  return res.json();
}

function setHero(title, poster) {
  document.getElementById('hero-title').innerText = title;
  const posterDiv = document.getElementById('hero-poster');
  posterDiv.style.backgroundImage = `url('${poster}')`;
}

function createCard(item) {
  const card = document.createElement('div');
  card.className = 'card';
  const poster = document.createElement('div');
  poster.className = 'card-poster';
  poster.style.backgroundImage = `url('${item.poster}')`;
  const title = document.createElement('div');
  title.className = 'card-title';
  title.innerText = item.title;
  const score = document.createElement('div');
  score.className = 'card-score';
  score.innerText = `Match: ${item.score.toFixed(2)}%`;
  card.appendChild(poster);
  card.appendChild(title);
  card.appendChild(score);
  return card;
}

function renderRecommendations(responseJson) {
  const rows = document.getElementById('rows');
  rows.innerHTML = '';
  const heroTitle = responseJson.query || 'Results';
  const recommendations = responseJson.recommendations || [];
  if (recommendations.length === 0) {
    rows.innerHTML = '<div class="row"><div class="row-title">No recommendations found. Try another movie title.</div></div>';
    setHero('Try a different title', 'https://picsum.photos/seed/default/300/450');
    return;
  }
  // use first recommendation as hero
  setHero(heroTitle, recommendations[0].poster);
  // create a row with cards
  const rowDiv = document.createElement('div');
  rowDiv.className = 'row';
  const title = document.createElement('div');
  title.className = 'row-title';
  title.innerText = `Because you liked ${heroTitle}`;
  rowDiv.appendChild(title);
  const cards = document.createElement('div');
  cards.className = 'row-cards';
  recommendations.forEach(item => {
    const c = createCard(item);
    c.addEventListener('click', () => {
      // when clicking on a recommended card, fetch recommendations for that movie
      document.getElementById('movie-input').value = item.title;
      doSearch(item.title, parseInt(document.getElementById('k-select').value));
    });
    cards.appendChild(c);
  });
  rowDiv.appendChild(cards);
  rows.appendChild(rowDiv);
}

async function doSearch(movie, k) {
  const data = await fetchRecommendations(movie, k);
  if (data.error) {
    alert('API error: ' + data.error);
    return;
  }
  renderRecommendations(data);
}

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('search-btn').addEventListener('click', () => {
    const movie = document.getElementById('movie-input').value;
    const k = parseInt(document.getElementById('k-select').value);
    if (!movie) { alert('Type a movie name'); return; }
    doSearch(movie, k);
  });

  // run a default demo
  doSearch('Toy Story', 6);
});
