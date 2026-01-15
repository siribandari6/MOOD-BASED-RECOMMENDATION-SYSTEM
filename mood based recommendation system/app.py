import streamlit as st
from recomender import recommend_movies

st.set_page_config(page_title="🎬 Mood-Based Movie Recommender", layout="centered")

st.title("🎭 Mood-Based Movie Recommendation System")
st.write("Tell me how you're feeling, and I’ll suggest movies for you 🎥✨")

user_input = st.text_input("How are you feeling today?")

if st.button("Get Recommendations"):
    if user_input.strip() == "":
        st.warning("Please enter your mood or feelings.")
    else:
        mood, recommendations = recommend_movies(user_input)
        st.success(f"Detected mood: **{mood}**")

        for _, row in recommendations.iterrows():
            st.markdown(
                f"**🎬 {row['title']}**  \n⭐ Rating: {row['vote_average']}  \n🔥 Popularity: {row['popularity']}"
            )



