import pyttsx3
import datetime
import random
import threading
import speech_recognition as sr
import webbrowser
import yt_dlp
from Dlg import sentences
from mtranslate import translate
from colorama import Fore, Style, init
import pythoncom
import queue

USER = 'Bosse !'

init(autoreset=True)

pythoncom.CoInitialize()

engine = pyttsx3.init()
engine.setProperty('rate', 200)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[6].id)

speech_queue = queue.Queue()

def speak(audio):
    speech_queue.put(audio)

def speech_worker():
    while True:
        audio = speech_queue.get()
        if audio == "STOP":
            break
        engine.say(audio)
        engine.runAndWait()

speech_thread = threading.Thread(target=speech_worker, daemon=True)
speech_thread.start()

def greet_me():
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak(f"Good Morning {USER}")
    elif 12 <= hour < 16:
        speak(f"Good Afternoon {USER}")
    elif 16 <= hour < 19:
        speak(f"Good Evening {USER}")
    text = random.choice(sentences)
    speak(text)

greet_me()  # Ensure this function is called at the start

def print_loop():
    while True:
        print(Fore.LIGHTBLACK_EX + "", end="\r", flush=True)

def Trans_hindi_to_english(txt):
    return translate(txt, to_language="en-us")

def listen():
    recognizer = sr.Recognizer()
    
    recognizer.dynamic_energy_threshold = True
    recognizer.energy_threshold = 3000
    recognizer.dynamic_energy_adjustment_damping = 0.1
    recognizer.dynamic_energy_ratio = 0.2
    recognizer.pause_threshold = 0.4
    recognizer.non_speaking_duration = 0.2

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)

        try:
            print(Fore.LIGHTGREEN_EX + "Listening...", end="\r", flush=True)
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
            recognized_txt = recognizer.recognize_google(audio).lower()

            if recognized_txt:
                translated_txt = Trans_hindi_to_english(recognized_txt)
                print(Fore.BLUE + "\nYou said: " + translated_txt)
                return translated_txt
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            print(Fore.RED + "I’m unable to connect. Please check your internet connection.")
        except Exception as e:
            print(Fore.RED + f"Unexpected error: {e}")
            return None
    return ""

def get_first_youtube_link(query):
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
        print(f"YouTube Search Error: {e}")
        return None

def play_music():
    speak("What music would you like to play, Bosse?")
    search_query = listen()
    if search_query:
        speak(f"Searching for {search_query} on YouTube.")
        print(f"Searching for: {search_query}")
        video_link = get_first_youtube_link(search_query)
        if video_link:
            print(f"Playing video: {video_link}")
            webbrowser.open(video_link)
            speak("Enjoy Bosse!")
        else:
            speak("Sorry, I couldn't find the song on YouTube, Bosse.")
    else:
        speak("I didn't hear any song name, Bosse.")

def listen_for_music():
    while True:
        command = listen()
        if any(phrase in command for phrase in ["music", "play music", "lucky play song"]):
            play_music()

if __name__ == "__main__":
    listen_thread = threading.Thread(target=listen_for_music, daemon=True)
    print_thread = threading.Thread(target=print_loop, daemon=True)

    listen_thread.start()
    print_thread.start()

    listen_thread.join()
