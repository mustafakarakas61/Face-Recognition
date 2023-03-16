import pytube

from Environments import pathTrain


def downloadYouTubeVideo(url, name):
    try:
        youtubeVideo = pytube.YouTube(url)

        # En yüksek kaliteyi seçin
        video_stream = youtubeVideo.streams.get_highest_resolution()

        # Videoyu indirin
        video_stream.download(output_path=pathTrain + name, filename=name + ".mp4")

        return pathTrain + name + "/" + name + ".mp4"
    except Exception as e:
        print(e)
