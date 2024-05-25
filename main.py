from flask import request
import logging
from flask import Flask, render_template
import re
import os
from pytube import YouTube
from flask import send_file

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static')

@app.route("/", methods=["GET", "POST"])
def home_route():
    if request.method == "POST":
        youtube_url = request.form.get("youtube_url")
        if is_valid_youtube_url(youtube_url):
            try:
                yt = YouTube(youtube_url)
                video_title = yt.title
                video_streams = yt.streams.filter(progressive=True, file_extension='mp4')
                audio_streams = yt.streams.filter(only_audio=True)
                message = f"This is a valid YouTube link. Video title: {video_title}"
                return render_template("home.html", message=message, video_streams=video_streams, audio_streams=audio_streams, youtube_url=youtube_url)
            except Exception as e:
                message = f"Failed to fetch video details: {str(e)}"
        else:
            message = "Please enter a valid YouTube link."
        return render_template("home.html", message=message)
    return render_template("home.html")

def is_valid_youtube_url(url):
    youtube_regex = (
        r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$"
    )
    return re.match(youtube_regex, url) is not None

@app.route("/download")
def download():
    url = request.args.get('url')
    type = request.args.get('type')
    try:
        yt = YouTube(url)
        if type == 'video':
            stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        else:
            stream = yt.streams.filter(only_audio=True).first()
        output_path = stream.download()
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        logger.error(f"Error downloading the stream: {str(e)}")
        return f"Error downloading the stream: {str(e)}"
    except Exception as e:
        logger.error(f"Error downloading the stream: {str(e)}")
        return f"Error downloading the stream: {str(e)}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
