from flask import Flask, request, render_template, redirect
import yt_dlp
import whisper
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'y_output'

def download_audio(youtube_url, output_path):
    filename = youtube_url[-6:]  # Get the last 6 characters from the youtube_url
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_path}/{filename}.%(ext)s',  # Use filename in the output template
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'mp3'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/youtube', methods=['GET', 'POST'])
def youtube_to_text():
    if request.method == 'POST':
        youtube_url = request.form.get('youtube_url')

        # Download the audio
        output_path = 'y_output'
        download_audio(youtube_url, output_path)

        # Transcribe the audio
        filename = youtube_url[-6:]  # Get the last 6 characters from the youtube_url
        model = whisper.load_model("base")
        result = model.transcribe(f'{output_path}/{filename}.mp3', language="en")

        # Display the transcribed text
        return render_template('youtube.html', text=result["text"])
    else:
        return render_template('youtube.html', text='')

@app.route('/audio', methods=['GET', 'POST'])
def audio_to_text():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Transcribe the audio
            model = whisper.load_model("base")
            result = model.transcribe(file_path, language="en")

            # Display the transcribed text
            return render_template('audio.html', text=result["text"])
    else:
        return render_template('audio.html', text='')

if __name__ == '__main__':
    app.run(debug=True)
