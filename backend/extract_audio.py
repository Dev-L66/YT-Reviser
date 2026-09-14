import yt_dlp

URLS = ['https://www.youtube.com/watch?v=kIk8tj0rbo0']

ydl_opts= {
    'format': 'm4a/bestaudio/best',
    'noplaylist': True,
    "outtmpl": "audio/%(title)s.%(ext)s",
    'postprocessors':[{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a'
    }]

}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    error_code = ydl.download(URLS)