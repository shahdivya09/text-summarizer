import tensorflow as tf

from flask import Flask, render_template, request
from text_summarizer import summarizer
from text_summarizer import absummarizer
from transformers import pipeline 
from flask import send_file, render_template
from gtts import gTTS # type: ignore
from flask import jsonify
from pydub import AudioSegment
import speech_recognition as sr
import os
import io

app = Flask(__name__, template_folder='templates')

@app.route('/')
def inddiv():
    return render_template('inddiv.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if (request.method == 'POST'): 
        rawtext = request.form['rawtext']
        summary, ogtext, len1, len2 = summarizer(rawtext)
    
    return render_template('inddiv.html', summaryy=summary, og= ogtext, l1=len1, l2=len2)


@app.route('/analyze2', methods=['GET', 'POST'])
def analyze2():
    if (request.method == 'POST'): 
        raw = request.form['raw']
        summ, ogtext2, len11, len22 = absummarizer(raw)
    
    return render_template('inddiv.html', summaryy=summ, og= ogtext2, l1=len11, l2=len22)


@app.route('/tts', methods=['POST'])
def tts():
    data = request.json
    text = data.get('text', '')
    if not text:
        return 'Text is required', 400

    tts = gTTS(text)
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    return send_file(mp3_fp, mimetype='audio/mpeg')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        # Convert mp3 to wav
        audio = AudioSegment.from_mp3(file_path)
        wav_path = file_path.replace('.mp3', '.wav')
        audio.export(wav_path, format='wav')

        # Use speech recognition to convert speech to text
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                return jsonify({'text': text})
            except sr.UnknownValueError:
                return jsonify({'error': 'Speech recognition could not understand audio'}), 400
            except sr.RequestError:
                return jsonify({'error': 'Could not request results from speech recognition service'}), 500

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)

