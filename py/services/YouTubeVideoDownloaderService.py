import os
import pytube
from moviepy.video.io.VideoFileClip import VideoFileClip

from Environments import pathTrain
from py.services.ExtractFaceService import extractFacesFromVideo, extractFaces


def downloadYouTubeVideo(url, name, firstSecond, duration):
    folder = pathTrain + name
    try:
        # İndirilecek dosyanın konumu
        # YouTube video nesnesini oluşturun
        youtube_video = pytube.YouTube(url)

        # En yüksek kaliteyi seçin
        video_stream = youtube_video.streams.get_highest_resolution()

        # Videoyu indirin
        video_path = os.path.join(folder, video_stream.default_filename)
        video_stream.download(output_path=folder)

        # İlk 10 saniye videoyu kesin ve kaydedin
        video_clip = VideoFileClip(video_path).subclip(firstSecond, duration)
        output_path = os.path.join(folder, "video_first_10_seconds.mp4")
        video_clip.write_videofile(output_path)

        # Video nesnesini kapatın ve dosya adında geçerli olmayan karakterleri kaldırın
        video_clip.close()
        os.remove(video_path)
        # os.rename(output_path, os.path.join(download_path, "video_first_10_seconds.mp4"))

        return True
    except Exception as e:
        print(e)
        return False


if downloadYouTubeVideo("https://www.youtube.com/shorts/lxl-B1tDSrY", "Recep Deneme 1", 0, 50):
    print("Video indirildi ve kesildi.")
    folder = pathTrain + "Recep Deneme 1"
    extractFacesFromVideo(folder + "/video_first_10_seconds.mp4", 100, "Recep Deneme 1", folder)
    extractFaces("Recep Deneme 1", folder)
else:
    print("Video indirilemedi veya kesilemedi.")
