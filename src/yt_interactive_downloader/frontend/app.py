import os
import shutil
import subprocess
from pathlib import Path

from dotenv.main import load_dotenv
from flask import Flask, jsonify, render_template, request

from src.yt_interactive_downloader.backend import YouTube

app = Flask(__name__)

load_dotenv(".env")

youtube = YouTube(key=os.environ.get("YOUTUBE_API"))


@app.route("/", methods=["GET", "POST"])
def index():
    status = "search"
    res = None
    server = os.environ.get("EXTERNAL_SERVER", "")
    path_to_download = os.environ.get("PATH_TO_DOWNLOAD", "")
    if request.method == "POST":
        query = request.form.get("query", "")
        res, status_code = youtube.search(part="snippet", q=query, maxResults=30)
        if 200 <= status_code < 300:
            status = "success"
        else:
            status = "fail"

    return render_template(
        "index.html",
        status=status,
        response=res,
        server=server,
        path_to_download=path_to_download,
    )


@app.route("/download/<videoId>", methods=["POST"])
def download(videoId: str):
    server = request.form.get("server")
    path_to_download = request.form.get("path_to_download")
    if path_to_download == "":
        path_to_download = "."
    path = Path(path_to_download)
    try:
        if server == "":
            path.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                [
                    "yt-dlp",
                    f"https://www.youtube.com/watch?v={videoId}",
                    "-f",
                    "mp4",
                    "-o",
                    rf"{path/videoId}.mp4",
                ],
            )
        else:
            temp = Path("./tmp/")
            temp.mkdir(exist_ok=True)
            subprocess.run(
                [
                    "yt-dlp",
                    f"https://www.youtube.com/watch?v={videoId}",
                    "-f",
                    "mp4",
                    "-o",
                    rf"{temp/videoId}.mp4",
                ],
            )
            subprocess.run(
                ["scp", f"{temp/videoId}.mp4", f"{server}:{path_to_download}"]
            )
            shutil.rmtree(temp)

        return jsonify({"message": "ダウンロードに成功しました！"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "ダウンロードに失敗しました"}), 500


def run():
    app.run(debug=True, port=8888)
