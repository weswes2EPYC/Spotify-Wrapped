import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def summarize(artists, songs):
    model = genai.GenerativeModel('gemini-1.5-flash')
    song1_name = songs[0]['name']
    song1_artist = songs[0]['artist']
    song2_name = songs[1]['name']
    song2_artist = songs[1]['artist']
    song3_name = songs[2]['name']
    song3_artist = songs[2]['artist']

    artist1_name = artists[0]['name']
    artist2_name = artists[1]['name']
    artist3_name = artists[2]['name']

    prompt = f"""
    Generate me a 100 word or less summary of my Spotify Wrapped. You should include any highlights and other relevant information. Here are my top three songs:
    1) {song1_name} by {song1_artist}
    2) {song2_name} by {song2_artist}
    3) {song3_name} by {song3_artist}
    Here are my top three artists:
    1) {artist1_name}
    2) {artist2_name}
    3) {artist3_name}
    """
    response = model.generate_content(
            prompt
        )
    print(response.text)
    return response.text