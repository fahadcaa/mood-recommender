import streamlit as st
import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from textblob import TextBlob
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenRouter
def get_deepseek_response(prompt):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "HTTP-Referer": "https://github.com/yourusername/mood-recommender",
            "X-Title": "Mood Recommender"
        },
        json={
            "model": "deepseek/deepseek-r1-distill-qwen-1.5b",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100
        }
    )
    return response.json()["choices"][0]["message"]["content"]

# Spotify setup
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="playlist-read-private"
))

# Mood mappings
MOOD_PLAYLISTS = {
    "happy": "37i9dQZF1DXdPec7aLTmlC",
    "sad": "37i9dQZF1DX7qK8ma5wgG1",
    # Add more moods as needed
}

# Streamlit UI
def main():
    st.title("🎵 Mood-Based Recommender")
    mood = st.selectbox("Select your mood", list(MOOD_PLAYLISTS.keys()))
    
    if st.button("Get Recommendation"):
        with st.spinner("Generating..."):
            # Get quote
            quote = get_deepseek_response(f"Give a short inspirational quote for someone feeling {mood}")
            st.success(quote)
            
            # Get playlist
            playlist = sp.playlist(MOOD_PLAYLISTS[mood])
            st.image(playlist["images"][0]["url"], width=200)
            st.markdown(f"[Open {playlist['name']} on Spotify]({playlist['external_urls']['spotify']})")

if __name__ == "__main__":
    main()
