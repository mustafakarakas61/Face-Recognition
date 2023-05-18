import subprocess

from moviepy.video.io.VideoFileClip import VideoFileClip
from yt_dlp import YoutubeDL

from src.resources.Environments import pathTempFolder, pathClippedVideos
from utils.Utils import randomString


def downloadYoutubeVideo(url, startTime, durationStartTime, durationEndTime):
    name = randomString(12)

    fileName = name + ".mp4"

    videoPath = pathTempFolder + "temp_" + fileName

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
        'outtmpl': videoPath,
        'merge_output_format': 'mp4',
        'nooverwrites': True,
        'quiet': False,
        'writethumbnail': False,
    }
    ydl = YoutubeDL(ydl_opts)

    ydl.download([url])

    clip = VideoFileClip(videoPath)

    maxDuration = clip.duration

    if int(durationEndTime) > int(maxDuration):
        durationEndTime = maxDuration

    duration = int(durationEndTime - durationStartTime)

    cmd = f"ffmpeg -y -loglevel fatal -ss {startTime} -i \"{videoPath}\" -t {duration} -vf scale=w=854:h=480 -c copy \"{pathClippedVideos}/{fileName}\""

    print("Klip Başlıyor : " + cmd)
    subprocess.call(
        cmd,
        shell=True)

    return pathClippedVideos + "/" + fileName
