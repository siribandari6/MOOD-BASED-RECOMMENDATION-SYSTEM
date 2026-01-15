import pandas as pd
import ast

# Load dataset
movies = pd.read_csv("data/tmdb_5000_movies.csv")

# Extract genre names
def extract_genre_names(genre_str):
    try:
        genres = ast.literal_eval(genre_str)
        return [g["name"] for g in genres]
    except:
        return []

movies["genre_names"] = movies["genres"].apply(extract_genre_names)

# Mood extraction (rule-based NLU)
def extract_mood_from_text(user_text):
    text = user_text.lower()

    mood_keywords = {
        "happy": ["happy", "joy", "fun", "cheerful", "excited"],
        "sad": ["sad", "lonely", "depressed", "down", "cry"],
        "angry": ["angry", "mad", "furious", "irritated"],
        "relaxed": ["calm", "relaxed", "peaceful", "chill", "stress"],
        "scared": ["scared", "afraid", "fear", "horror"],
        "excited": ["thrilled", "energetic"]
    }

    for mood, keywords in mood_keywords.items():
        for word in keywords:
            if word in text:
                return mood

    return "neutral"


mood_to_genres = {
    "happy": ["Comedy", "Family", "Animation"],
    "sad": ["Drama", "Romance"],
    "angry": ["Action", "Thriller"],
    "relaxed": ["Drama", "Fantasy"],
    "excited": ["Adventure", "Action", "Science Fiction"],
    "scared": ["Horror", "Thriller"],
    "neutral": ["Drama"]
}


def recommend_movies(user_text, top_n=5):
    mood = extract_mood_from_text(user_text)
    preferred_genres = mood_to_genres.get(mood, ["Drama"])

    filtered = movies[movies["genre_names"].apply(
        lambda genres: any(g in genres for g in preferred_genres)
    )]

    ranked = filtered.sort_values(
        by=["vote_average", "popularity"],
        ascending=False
    )

    return mood, ranked[["title", "vote_average", "popularity"]].head(top_n)


'''cd Desktop

cd "mood based recommendation system"
dir
dir data
python recomender.py
python -m pip install streamlit
python -m streamlit run app.py
'''