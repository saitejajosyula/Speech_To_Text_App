import speech_recognition as sr
import wavio
import librosa
from flask import logging, Flask, render_template, request, flash

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('Speech.html')


@app.route('/start', methods=["POST"])
def start():
    AUDIO_FILE = request.files['audio_data']
    with open('audio.wav', 'wb') as audio:
        AUDIO_FILE.save(audio)
    data, rate = librosa.load('audio.wav')
    s = wavio.write("audio.wav", data, rate, sampwidth=1)
    r = sr.Recognizer()
    with sr.AudioFile("audio.wav") as source:
        audio = r.record(source)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(e))
    return "Done"


if __name__ == "__main__":
    app.run(debug=True)
