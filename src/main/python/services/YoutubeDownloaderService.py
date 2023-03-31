import subprocess
import os
from yt_dlp import YoutubeDL

from src.resources.Environments import pathTempFolder, pathClippedVideos
from utils.Utils import checkFolder, getMp4FileList


# {"name":"Recep Tayyip Erdoğan","url":"https://www.youtube.com/watch?v=fxUox86xQGc&t=7s","ss":"00:00:30","t":"45"}
def createClippedVideo(url, ss, t, name):
    pathName = pathClippedVideos + name
    checkFolder(pathName)

    fileList = getMp4FileList(pathName)
    i = len(fileList)
    fileName = name + "_" + str(int(i + 1)) + ".mp4"

    while True:
        if fileName in fileList:
            i += 1
            fileName = name + "_" + str(int(i + 1)) + ".mp4"
        else:
            break

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
        'outtmpl': pathTempFolder + "temp_" + fileName,
        'merge_output_format': 'mp4',
        'nooverwrites': True,
        'quiet': False,
        'writethumbnail': False,
    }
    ydl = YoutubeDL(ydl_opts)

    ydl.download([url])

    cmd = f"ffmpeg -y -loglevel fatal -ss {ss} -i \"{pathTempFolder}temp_{fileName}\" -t {t} -c copy \"{pathName}/{fileName}\""

    print("Klip Başlıyor : " + cmd)
    subprocess.call(
        cmd,
        shell=True)

    os.remove(pathTempFolder + "temp_" + fileName)

    return pathName + "/" + fileName
