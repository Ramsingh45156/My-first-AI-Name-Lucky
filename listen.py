import speech_recognition as sr
import threading
from mtranslate import translate
from colorama import Fore, Style, init
from speak import speak

init(autoreset=True)

def print_loop():
    while True:
        print(Fore.LIGHTBLACK_EX + "", end="\r", flush=True)

def Trans_hindi_to_english(txt):
    return translate(txt, to_language="en-us")

def listen():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 3400
    recognizer.dynamic_energy_adjustment_damping = 0.011
    recognizer.dynamic_energy_ratio = 0.2
    recognizer.pause_threshold = 0.3
    recognizer.non_speaking_duration = 0.1

    with sr.Microphone() as source:
        # print(Fore.LIGHTGREEN_EX + "Adjusting for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        while True:
            try:
                print(Fore.LIGHTGREEN_EX + "Listening...", end="\r", flush=True)
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
                
                # print(Fore.LIGHTBLUE_EX + "\nProcessing...", end="\r", flush=True)
                recognized_txt = recognizer.recognize_google(audio).lower()

                if recognized_txt:
                    translated_txt = Trans_hindi_to_english(recognized_txt)
                    print(Fore.BLUE + "\nYou said: " + translated_txt)
                    speak(translated_txt)
            except sr.UnknownValueError:
                # print(Fore.RED + "Sorry, I didn't catch that. Can you repeat?")
                pass
            except sr.RequestError:
                print(Fore.RED + "I’m unable to connect. Please check your internet connection.")
            except Exception as e:
                print(Fore.RED + f"Unexpected error: {e}")


    listen_thread = threading.Thread(target=listen, daemon=True)
    print_thread = threading.Thread(target=print_loop, daemon=True)

    listen_thread.start()
    print_thread.start()

    listen_thread.join()



