# !pip install -U yt-dlp
import yt_dlp

# 定义下载选项，只提取音频
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloaded_audio.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

# 下载音频
url = "https://www.youtube.com/watch?v=FicvGCYBbAQ"
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])


# 多声道转单声道
!ffmpeg -i audios/cr7.mp3 -ac 1 audios/'ronaldo.wav'