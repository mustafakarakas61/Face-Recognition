# import pytube
#
# from Environments import pathTrain, pathTest
# from utils.Utils import randomInt
#
#
# def downloadYouTubeVideo(url, name):
#     try:
#         youtubeVideo = pytube.YouTube(url)
#
#         # En yüksek kaliteyi seçin
#         video_stream = youtubeVideo.streams.get_highest_resolution()
#
#         # Videoyu indirin
#         video_stream.download(output_path=pathTrain + name, filename=name + ".mp4")
#
#         return pathTrain + name + "/" + name + ".mp4"
#     except Exception as e:
#         print("Video indirilemiyor : ", e)
#
#
# def downloadYouTubeVideoToTest(url):
#     try:
#         youtubeVideo = pytube.YouTube(url)
#
#         # En yüksek kaliteyi seçin
#         video_stream = youtubeVideo.streams.get_highest_resolution()
#
#         # Videoyu indirin
#         randomFileName = "test_" + str(randomInt(4)) + ".mp4"
#         video_stream.download(output_path=pathTest, filename=randomFileName)
#
#         return pathTest + + randomFileName
#     except Exception as e:
#         print("Video indirilemiyor : ", e)
