# from pytube import YouTube
from pytube import YouTube

try:
    yt = YouTube("https://youtube.com/watch?v=sJBO7rMR8ks")
    print("Video Title:", yt.title)
except Exception as e:
    print("Error:", e)
