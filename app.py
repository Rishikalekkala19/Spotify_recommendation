import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up your Spotify API credentials
CLIENT_ID = 'baaf315196db4203957f5f51959fe11a'
CLIENT_SECRET = '3e1e5763c1144be0859959eb761b8ea6'
REDIRECT_URI = 'http://localhost:8501'  # This should match your Streamlit app's URL

# Initialize the Spotify API client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope='user-library-read'))

# Streamlit app title
st.title("Spotify Song Recommendation System")

# User login
if st.button('Login to Spotify'):
    st.write("You are now logged in!")

# Function to fetch user's saved tracks
def get_user_tracks():
    results = sp.current_user_saved_tracks()
    tracks = results['items']
    track_list = []
    for item in tracks:
        track = item['track']
        track_list.append({
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'uri': track['uri']
        })
    return pd.DataFrame(track_list)

# Function to recommend songs based on the selected artist
def recommend_songs(preferred_artist):
    recommended_tracks = []
    
    # Search for tracks by the selected artist
    results = sp.search(q=f'artist:{preferred_artist}', type='track', limit=10)
    
    # Collect recommended tracks
    for track in results['tracks']['items']:
        recommended_tracks.append({
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'uri': track['uri']
        })

    # Convert the list of recommended tracks to a DataFrame
    recommended_tracks_df = pd.DataFrame(recommended_tracks)

    return recommended_tracks_df



if st.button('Fetch My Tracks'):
    user_tracks = get_user_tracks()
    st.write("Your Saved Tracks:")
    st.write(user_tracks)


# User input for artist preference
preferred_artist = st.text_input("Enter a Favorite Artist", "")

# Button to recommend songs
if st.button('Recommend Songs'):
    if preferred_artist:
        recommended_songs_df = recommend_songs(preferred_artist)
        if not recommended_songs_df.empty:
            st.write("Recommended Songs:")
            st.write(recommended_songs_df)
        else:
            st.write("No recommendations found. Try a different artist!")
    else:
        st.write("Please enter a favorite artist to get recommendations.")
