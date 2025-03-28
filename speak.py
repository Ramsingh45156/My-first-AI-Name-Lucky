import pyttsx3
import datetime
import random
import threading

USER = 'Bosse !'

def speak(audio):
    """हर बार नया pyttsx3 इनिशियलाइज़ होगा ताकि कोई थ्रेडिंग एरर न आए"""
    engine = pyttsx3.init()
    engine.setProperty('rate', 200) 
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[6].id)  

    engine.say(audio)
    engine.runAndWait()
    
def speak_async(audio):
    """स्पीच को बैकग्राउंड में चलाने के लिए एक थ्रेड बनाएगा"""
    threading.Thread(target=speak, args=(audio,), daemon=True).start()

def greet_me():
    """समय के हिसाब से ग्रीटिंग बोलेगा"""
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak_async(f"Good Morning {USER}")
    elif 12 <= hour < 16:
        speak_async(f"Good Afternoon {USER}")
    elif 16 <= hour < 19:
        speak_async(f"Good Evening {USER}")

    sentences = ["How can I assist you today?", "Hope you're having a great day!", "What can I do for you?"]
    speak_async(random.choice(sentences))


