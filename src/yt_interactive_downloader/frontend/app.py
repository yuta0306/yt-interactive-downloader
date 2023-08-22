import os
import shutil
import subprocess
from pathlib import Path

from dotenv.main import load_dotenv
from flask import Flask, jsonify, render_template, request, session

from src.yt_interactive_downloader.backend import YouTube

app = Flask(__name__)
app.secret_key = "secret!"

load_dotenv(".env")

youtube = YouTube(key=os.environ.get("YOUTUBE_API"))

TOPIC_IDS = {
    "any": None,
    "music": "/m/04rlf",
    "game": "/m/0bzvm2",
    "sport": "/m/06ntj",
    "entertainment": "/m/02jjt",
    "lifestyle": "/m/019_rr",
    "social": "/m/098wr",
    "knowledge": "/m/01k8wb",
}


@app.route("/", methods=["GET", "POST"])
def index():
    status = "search"
    res = None
    server = os.environ.get("EXTERNAL_SERVER", "")
    path_to_download = os.environ.get("PATH_TO_DOWNLOAD", "")
    if request.method == "POST":
        for key, value in request.form.items():
            session[key] = value
        query = request.form.get("query", "")
        channel_id = request.form.get("channelId", "")
        topic = request.form.get("topic", "any")
        max_results = int(request.form.get("maxResults", 30))
        caption = request.form.get("caption", "any")
        order = request.form.get("order")
        topic_id = TOPIC_IDS[topic]
        if order == "unset":
            order = None
        if channel_id == "":
            channel_id = None

        res, status_code = youtube.search(
            part="snippet",
            filter="forDeveloper",
            q=query,
            channelId=channel_id,
            maxResults=max_results,
            order=order,
            videoCaption=caption,
            type="video",
            topicId=topic_id,
        )
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
        history=session,
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
                    "--sub-langs",
                    "ja",
                    "--embed-subs",
                    "--embed-thumbnail",
                    "--embed-metadata",
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
