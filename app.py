import pyttsx3
import speech_recognition as sr
import time
import sys
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


def activatejarvis():
    global command
    command = listen_jarvis()
    speak(command)


def callback(recognizer, audio):  # this is called from the background thread
    global stop_it
    global statusJarvis
    global voice
    try:
        text = recognizer.recognize_google(audio)
        print("You said " + text)
        if 'jarvis' in text.lower() or 'jarvis' == text.lower():
            statusJarvis = True
            activatejarvis()
        elif text.lower() == 'terminate':
            voice(wait_for_stop=False)

    except:
        pass


def listen_jarvis():
    listener = sr.Recognizer()
    op = " "
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)
            print('Listening You:   ')
            voice = listener.listen(source, timeout=3)
            op = listener.recognize_google(voice)
    except Exception as e:
        print(e)
        return 'error'
    return op


def speak(data):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 170)
    if data == '0':
        engine.say("Yes Abhishek, How can I help you")
        engine.runAndWait()
    else:
        engine.say(data)
        engine.runAndWait()


@app.route("/", methods=["GET", "POST"])
def index(name="", data=""):
    global stop_it
    global statusJarvis
    global command
    global voice
    if request.method == "POST" and name == "":
        print("listening now: ")
        voice = listener.listen_in_background(source, callback)
        while True:
            if statusJarvis:
                return render_template('index.html',
                                       name='activate',
                                       data="I can Listening Whole Day, I Am Captain Jarvis: ")

            time.sleep(0.1)

    return render_template('index.html', name=name)


if __name__ == "__main__":
    stop_it = False
    statusJarvis = False
    command = ""
    listener = sr.Recognizer()
    source = sr.Microphone()
    app.run(debug=True, threaded=True)
    # print("listening now: ")
    # voice = listener.listen_in_background(source, callback)
    # while True:
    #     if speakJarvis:
    #         speakJarvis = False
    #         speak('0')
    #         k = listen_jarvis()
    #         print(k)
    #     if stop_it:
    #         voice(wait_for_stop=False)
    #         break
    #     time.sleep(0.1)
