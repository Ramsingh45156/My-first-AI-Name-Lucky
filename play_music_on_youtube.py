import webbrowser
import time
import threading
import yt_dlp
from speak import speak
from listen import listen

def get_first_youtube_link(query):
    """यूट्यूब से पहला वीडियो लिंक निकालने का फंक्शन"""
    try:
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'force_generic_extractor': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_url = f"ytsearch1:{query}"
            info = ydl.extract_info(search_url, download=False)

            if 'entries' in info and len(info['entries']) > 0:
                return info['entries'][0]['url']
            return None
    except Exception as e:
        print(f"🔴 YouTube Search Error: {e}")
        return None

def play():
    """थ्रेड में म्यूजिक प्ले करेगा"""
    def run():
        speak("What music would you like to play, Bosse?")
        search_query = listen()
        if search_query:
            speak(f"Playing {search_query} on YouTube.")
            video_link = get_first_youtube_link(search_query)
            if video_link:
                webbrowser.open(video_link)
                speak("Enjoy Bosse!")
            else:
                speak("Sorry, I couldn't find the song on YouTube, Bosse.")
        else:
            speak("I didn't hear any song name, Bosse.")

    # अब यह अलग थ्रेड में चलेगा और मेन प्रोग्राम ब्लॉक नहीं होगा
    music_thread = threading.Thread(target=run, daemon=True)
    music_thread.start()

# अब जब यूजर "play music" बोलेगा, तब ही प्ले होगा
def listen_for_music():
    """म्यूजिक कमांड सुनने के लिए लूप में चलने वाला फंक्शन"""
    while True:
        command = listen()
        if any(phrase in command for phrase in ["music", "play music", "lucky play song"]):
            play()

# **अब यह हमेशा सुनता रहेगा और म्यूजिक प्ले करेगा** 🎶
listen_for_music()
